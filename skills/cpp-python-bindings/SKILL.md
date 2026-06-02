---
name: cpp-python-bindings
description: 将 C++ 代码打包为带 Python 接口的原生 Python 模块（类似 NumPy / PyTorch 的内部 _core 模式）。涵盖项目结构设计、CMake 构建配置、Python 包布局、.pyi 类型存根生成、多配置生成器适配、常见 Windows/Linux 构建陷阱及解决方案。当用户提到 C++ 扩展、Python 绑定、C 扩展模块、pybind11、nanobind、SWIG、Cython、CFFI/ctypes、Python 模块打包、.pyd 或 .so 文件时，使用此技能。
---

# C++ 到 Python 原生包 构建指南

将 C++ 底层引擎暴露为 Python 原生包的标准做法。覆盖 5 种主流绑定方案（pybind11、nanobind、SWIG、Cython、CFFI），输出符合 NumPy/PyTorch 标准（`_core.pyd` + `__init__.py`）的包结构。

## 总体设计原则

### 定为目标结构

```
<output_dir>/<Config>/               # Config = Debug|Release (多配置) 或空 (单配置)
├── engine_pybind/                   # 每个方案是一个 Python 包
│   ├── __init__.py                  # 重导出公开 API: from ._core import *
│   ├── _core.cp312-win_amd64.pyd   # 内部 C 扩展模块（以下划线前缀隐藏）
│   ├── _core.pyi                    # 类型存根
│   └── py.typed                     # PEP 561 标记
├── engine_nanobind/
│   ├── __init__.py
│   └── ...
├── engine_swig/                     # SWIG 特殊：_engine_swig.pyd 在包内
│   ├── __init__.py                  # SWIG 生成的包装器
│   └── _engine_swig.pyd
└── engine_cffi/
    ├── __init__.py
    ├── cffi_bridge.py               # 手写 Pythonic 包装
    └── engine_c.dll                 # 纯 C DLL
```

### 核心设计模式

- **内部模块下划线前缀**：`_core`、`_C` 标记为内部实现，用户不应直接导入
- **`__init__.py` 重导出**：公开 API 显式列出，控制暴露面：
  ```python
  from ._core import Engine, Scene, GameObject
  ```
- **`py.typed` 标记**：PEP 561 标准，告知类型检查器

### 业界对标

| 项目    | 内部模块              | CppPy 对标                                 |
|---------|-----------------------|-------------------------------------------|
| NumPy   | `numpy/_core`         | `engine_pybind/_core`                     |
| PyTorch | `torch/_C`            | `engine_nanobind/_core`                   |
| Pydantic| `pydantic_core`       | `engine_cffi/cffi_bridge`                 |

---

## 项目目录结构

```
MyProject/
├── CMakeLists.txt                       # 顶层：find_package(Python3)，add_subdirectory
├── engine/                              # 共享 C++ 库
│   ├── CMakeLists.txt                   # add_library(engine STATIC ...)
│   ├── include/engine/
│   │   ├── c_api.h                      # 纯 C extern "C" API（供 SWIG/CFFI）
│   │   └── facade.h                     # C++ 公开 API（供 pybind11/nanobind）
│   └── src/
│       ├── facade.cpp
│       └── c_api.cpp
├── bindings/
│   ├── pybind11/
│   │   ├── CMakeLists.txt               # pybind11_add_module → _core_pybind11
│   │   ├── python/__init__.py           # from ._core import *
│   │   └── src/pybind11_bindings.cpp    # PYBIND11_MODULE(_core, m)
│   ├── nanobind/
│   │   ├── CMakeLists.txt               # nanobind_add_module → _core_nanobind
│   │   ├── python/__init__.py
│   │   └── src/nanobind_bindings.cpp    # NB_MODULE(_core, m)
│   ├── swig/
│   │   ├── CMakeLists.txt               # swig_add_library
│   │   ├── python/__init__.py           # （构建时由 SWIG 生成的 .py 覆盖）
│   │   └── src/engine.i                 # SWIG 接口文件
│   ├── cython/
│   │   ├── CMakeLists.txt               # Cython custom_command → add_library
│   │   ├── cmake/patch_cython_debug.cmake
│   │   ├── python/__init__.py
│   │   └── src/
│   │       ├── _core.pyx                # Cython 实现
│   │       └── _core.pxd                # Cython 声明
│   └── cffi/
│       ├── CMakeLists.txt               # add_library(engine_c SHARED ...)
│       ├── python/
│       │   ├── __init__.py              # from .cffi_bridge import ...
│       │   ├── cffi_bridge.py           # Pythonic 包装（ctypes.CDLL）
│       │   └── cffi_bridge.pyi          # 手写类型存根
│       └── src/cffi_c_impl.cpp          # extern "C" 实现
├── scripts/
│   ├── manage.py                        # 构建编排：setup / build / run / lint
│   └── generate_stubs.py                # 统一 .pyi 存根生成调度器
└── examples/
    └── pybind11/demo.py
```

---

## CMake 构建配置

### 顶层 CMakeLists.txt 模板

```cmake
cmake_minimum_required(VERSION 3.15)
project(MyEngine LANGUAGES CXX C)

# 只调用一次 Python3
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

option(BUILD_PYBIND11 "Build pybind11 bindings" ON)
option(BUILD_NANOBIND "Build nanobind bindings" ON)
option(BUILD_SWIG     "Build SWIG bindings"     ON)
option(BUILD_CYTHON   "Build Cython bindings"   ON)
option(BUILD_CFFI     "Build CFFI bindings"     ON)

add_subdirectory(engine)

if(BUILD_PYBIND11)
  add_subdirectory(3rdparty/pybind11)
  add_subdirectory(bindings/pybind11)
endif()
# ... 其他方案同样处理
```

### 关键：目标名冲突避免

多个绑定方案都会产生 `_core.pyd`。**目标名必须唯一**，使用 `OUTPUT_NAME` 设置最终文件名：

```cmake
# pybind11
pybind11_add_module(_core_pybind11 src/...)   # CMake target name: _core_pybind11
set_target_properties(_core_pybind11 PROPERTIES
  OUTPUT_NAME "_core"                          # 磁盘文件名: _core.pyd
)

# nanobind
nanobind_add_module(_core_nanobind src/...)
set_target_properties(_core_nanobind PROPERTIES OUTPUT_NAME "_core")

# Cython
add_library(_core_cython MODULE ...)
set_target_properties(_core_cython PROPERTIES OUTPUT_NAME "_core")
```

### 各方案 POST_BUILD 模式

**所有方案共用**：编译到临时目录 `_build/<scheme>/`，POST_BUILD 组装到 `bindings_output/$<CONFIG>/engine_<scheme>/`：

```cmake
# 临时输出（避免 _core 文件名冲突）
set_target_properties(_core_pybind11 PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bindings_output/_build/pybind11"
  OUTPUT_NAME "_core_pybind11"
)

# 最终包目录
set(_pkg "${CMAKE_BINARY_DIR}/bindings_output/$<CONFIG>/engine_pybind")

add_custom_command(TARGET _core_pybind11 POST_BUILD
  # 1) 创建包目录
  COMMAND ${CMAKE_COMMAND} -E make_directory "${_pkg}"
  # 2) 将临时 .pyd 重命名并移入包内
  COMMAND ${CMAKE_COMMAND} -E rename
    "$<TARGET_FILE:_core_pybind11>"
    "${_pkg}/_core$<TARGET_FILE_SUFFIX:_core_pybind11>"
  # 3) 复制 __init__.py
  COMMAND ${CMAKE_COMMAND} -E copy_if_different
    "${CMAKE_CURRENT_SOURCE_DIR}/python/__init__.py"
    "${_pkg}/"
  # 4) 生成存根
  COMMAND ${Python3_EXECUTABLE}
    ${CMAKE_SOURCE_DIR}/scripts/generate_stubs.py
    --scheme pybind11 --module-dir "${_pkg}"
)
```

**SWIG 特殊处理**：SWIG 4.4+ 生成的包装器检测到自己在包内时会用 `from . import _engine_swig`，所以 `.pyd` 也必须放在包内：

```cmake
add_custom_command(TARGET engine_swig POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E rename
    "$<TARGET_FILE:engine_swig>"
    "${_pkg}/_engine_swig$<TARGET_FILE_SUFFIX:engine_swig>"
  COMMAND ${CMAKE_COMMAND} -E copy_if_different
    "${CMAKE_CURRENT_BINARY_DIR}/engine_swig.py"
    "${_pkg}/__init__.py"
)
```

---

## .pyi 类型存根生成

### 存根生成工具选型

| 方案 | 工具 | 命令 | 质量 |
|------|------|------|------|
| nanobind | 内置 `nanobind.stubgen` | `python -m nanobind.stubgen -m _core -O <dir>` | 优秀 — 读 `__nb_signature__` |
| pybind11 | `pybind11-stubgen` | `pybind11-stubgen _core -o <dir>` | 中等 — docstring 解析 |
| Cython | `stubgen-pyx` | `stubgen-pyx <src_dir> --output-dir <dir>` | 良好 — AST 解析 |
| SWIG | mypy `stubgen` + py.typed | `stubgen -m engine_swig -o <dir>` | 差 — 经常失败 |
| CFFI | 手写 `.pyi` | 无自动化 | 手动维护 |

### 统一存根生成脚本

创建 `scripts/generate_stubs.py`，对所有方案提供统一接口：

```python
def gen_nanobind(module_dir):
    subprocess.run([sys.executable, "-m", "nanobind.stubgen",
        "-m", "_core", "-O", module_dir],
        env={**os.environ, "PYTHONPATH": module_dir})

def gen_pybind11(module_dir):
    subprocess.run([sys.executable, "-m", "pybind11_stubgen",
        "_core", "-o", module_dir],
        env={**os.environ, "PYTHONPATH": module_dir})
```

**关键**：存根生成的 PYTHONPATH 必须包含 `.pyd` 所在目录（即包的目录），因为存根工具需要导入模块进行内省。

---

## 常见构建陷阱及解决方案

### 1. Windows Debug 构建：python3xx_d.lib 找不到

**现象**：`LNK1104: cannot open file 'python312_d.lib'`

**根因**：`pyconfig.h` `#pragma comment(lib, "python3xx_d.lib")` 在 Debug 构建中自动链接 debug 版 Python 库，但标准 Python 发行版不提供。

**修复**：
```cmake
if(WIN32)
  set(_py_lib "${Python3_ROOT_DIR}/libs/python${Python3_VERSION_MAJOR}${Python3_VERSION_MINOR}.lib")
  target_link_libraries(target PRIVATE "${_py_lib}")
  target_link_options(target PRIVATE
    $<$<CONFIG:Debug>:/NODEFAULTLIB:python${Python3_VERSION_MAJOR}${Python3_VERSION_MINOR}_d.lib>
  )
endif()
```

### 2. Py_REF_DEBUG 符号无法解析

**现象**：`LNK2019: unresolved external symbol __imp__Py_NegativeRefcount` 等

**根因链**：`_DEBUG (MSVC /MDd) → pyconfig.h #define Py_DEBUG → object.h #define Py_REF_DEBUG → Py_INCREF/Py_DECREF 调用仅 debug Python 中存在的函数`

**SWIG 修复**：SWIG 4.4+ 内置机制，只需加 flag：
```cmake
target_compile_definitions(target PRIVATE
  $<$<AND:$<CONFIG:Debug>,$<PLATFORM_ID:Windows>>:SWIG_PYTHON_INTERPRETER_NO_DEBUG>
)
```

**Cython 修复**：后处理补丁脚本，在 `#include "Python.h"` 周围插入 `_DEBUG` guard：
```cmake
# CMake custom_command 链
COMMAND ${CMAKE_COMMAND}
  "-DGENERATED_FILE=${OUTPUT}.cxx"
  -P ${CMAKE_CURRENT_SOURCE_DIR}/cmake/patch_cython_debug.cmake
```

补丁脚本内容：
```cmake
# 找到 #include "Python.h"，在其前后插入 guard
file(READ "${GENERATED_FILE}" CONTENT)
string(FIND "${CONTENT}" "#include \"Python.h\"" PYTHON_H_POS)
# ... 拆分字符串 ...
set(PATCHED
"${BEFORE}
#if defined(_DEBUG) && defined(_MSC_VER) && _MSC_VER >= 1929
# include <corecrt.h>
#endif
#undef _DEBUG
${INCLUDE_LINE}
#define _DEBUG 1
${AFTER}")
```

**注意**：必须在 undef `_DEBUG` 之前预包含 `<corecrt.h>`（MSVC 14.38+ 需要，否则 `<atomic>` 中的 `_invalid_parameter` 无法解析）。

### 3. 多配置生成器路径问题

**现象**：`ModuleNotFoundError` — Visual Studio 将 `.pyd` 放到 `Debug/` 子目录

**修复**：
- 使用 `$<CONFIG>` 生成器表达式：`"${CMAKE_BINARY_DIR}/bindings_output/$<CONFIG>/engine_pybind"`
- `_find_packages_root()` 函数自动探测配置子目录

### 4. 方案间 _core.pyd 文件名冲突

**根因**：多个 CMake target 都输出 `_core.pyd` 到同一目录

**修复**：使用 `_build/<scheme>/` 临时目录，POST_BUILD 中 rename 到最终位置。

### 5. VS 解决方案缺少头文件

**现象**：IDE 中只显示 `.cpp` 文件

**修复**：将 `.h` 添加到 target 的 SOURCES：
```cmake
target_sources(target PRIVATE ${ENGINE_HEADERS})
```

### 6. SWIG 未安装

**修复**：在 setup 脚本中自动下载 swigwin 预编译包：
```python
url = "https://sourceforge.net/projects/swig/files/swigwin/swigwin-4.4.0/swigwin-4.4.0.zip/download"
# 下载 → 解压 → 设置 SWIG_EXECUTABLE
```

---

## 构建编排脚本

### manage.py 设计

```python
# commands: setup | build | run | lint | tidy
# --scheme: pybind11 | nanobind | swig | cython | cffi

def cmd_setup(args):
    # 1) 创建 venv
    # 2) pip install 依赖（pybind11, nanobind, cffi, cython + stub tools）
    # 3) 3rdparty/ 依赖（git clone / download）
    # 4) cmake configure（自动检测 VS 生成器）

def cmd_build(args):
    # cmake --build build/ --config <config>

def cmd_run(args):
    # PYTHONPATH = _find_packages_root()
    # subprocess.run 各 demo

def _find_packages_root():
    """探测包含 engine_* 包目录的实际输出路径。
    单配置生成器 → bindings_output/
    多配置生成器 → bindings_output/Debug/ 等"""
```

### PYTHONPATH 探测

```python
def _find_packages_root():
    base = "build/bindings_output/"
    # 检查基础目录是否包含 engine_*/__init__.py
    for entry in os.listdir(base):
        if (entry.startswith("engine_")
            and os.path.isfile(os.path.join(base, entry, "__init__.py"))):
            return base
    # 否则搜索配置子目录 Debug / Release
    for entry in os.listdir(base):
        sub = os.path.join(base, entry)
        if os.path.isdir(sub):
            for sub_entry in os.listdir(sub):
                if (sub_entry.startswith("engine_")
                    and os.path.isfile(os.path.join(sub, sub_entry, "__init__.py"))):
                    return sub
    # 回退
    for cfg in ("Release", "Debug", "RelWithDebInfo"):
        if os.path.isdir(os.path.join(base, cfg)):
            return os.path.join(base, cfg)
    return base
```

---

## 包创建检查清单

构建完成后确认以下文件都存在：

```
bindings_output/<Config>/
├── engine_pybind/__init__.py, _core.*.pyd, _core.pyi, py.typed
├── engine_nanobind/__init__.py, _core.*.pyd, _core.pyi, py.typed
├── engine_swig/__init__.py, _engine_swig.pyd, py.typed
├── engine_cython/__init__.py, _core.pyd, _core.pyi, py.typed
└── engine_cffi/__init__.py, cffi_bridge.py, cffi_bridge.pyi, engine_c.dll, py.typed
```

验证：
```bash
PYTHONPATH=build/bindings_output/Debug python -c "import engine_pybind; print(engine_pybind.Engine)"
```

---

## 参考资源

查阅 `references/troubleshooting.md` 获取 9 个已解决构建问题的完整根因分析和解决方案。
