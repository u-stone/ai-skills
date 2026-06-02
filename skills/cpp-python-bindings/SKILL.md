---
name: cpp-python-native-package
description: >
  将 C++ 代码封装为标准 Python 原生扩展包，并通过 editable install 与 wheel 进行开发和交付。
  当用户提到 C++ 扩展、Python 绑定、pybind11、nanobind、Cython、SWIG、CFFI/ctypes、
  .pyd、.so、.dylib、Python 模块打包、pip install -e .、wheel、scikit-build-core、CMake 时使用。
---

# Skill: C++ 原生扩展的 Python 包化与 Wheel 交付

## 0. 执行目标

帮助用户把 C++ 代码封装成可 `pip install` 的 Python 包。

最终目标不是生成一个裸 `.pyd` / `.so`，而是生成标准 Python package：

```text
开发期：pip install -e .
发布期：python -m build --wheel
验证期：干净虚拟环境 pip install dist/*.whl 后 import 成功
```

默认产物形态：

```text
<package>/
├── __init__.py
├── runtime.py              # 可选，Python facade
├── _core.*.pyd / *.so      # C++ 原生扩展
├── 依赖 dll/so/dylib       # 如有
├── _core.pyi               # 可选
└── py.typed                # 可选
```

---

## 1. 何时使用本 Skill

当用户需求包含以下任一关键词或意图时使用：

- C++ 封装 Python 模块
- Python 原生扩展
- pybind11 / nanobind / Cython / SWIG / CFFI / ctypes
- `.pyd` / `.so` / `.dylib`
- `PYBIND11_MODULE`
- Python/C API
- `pip install -e .`
- `wheel`
- `scikit-build-core`
- CMake 构建 Python 扩展
- C++ SDK 暴露给 Python
- 游戏引擎 C++ Runtime 暴露给 Python 工具链

---

## 2. 先判断用户当前阶段

根据用户描述，把任务归入一个阶段。

### A. 从零创建项目

用户通常会说：

```text
我要把 C++ 库封装成 Python 包
帮我搭 pybind11 项目
帮我写 CMake / pyproject.toml
```

执行：

1. 选择绑定方案。
2. 创建 `src/<package>` 包布局。
3. 写 `pyproject.toml`。
4. 写 `CMakeLists.txt`。
5. 写最小绑定代码。
6. 添加 import 测试。
7. 执行 `pip install -e .`。
8. 执行 `python -m build --wheel`。
9. 干净环境安装 wheel 验证。

### B. 已有 `.pyd` / `.so`，不知道放哪

用户通常会说：

```text
编译出的 .pyd 放到哪里？
Python 怎么 import？
要不要设置 PYTHONPATH？
```

执行：

1. 建议放进 `src/<package>/`。
2. 创建 `__init__.py` 作为 facade。
3. 检查 native 模块名是否和初始化函数一致。
4. 引导改成 `pip install -e .`。
5. 不把 `PYTHONPATH` 作为正式方案。
6. 如需分发，打 wheel。

### C. 已有 CMake 构建，想接入 Python 包

用户通常会说：

```text
CMake 已经能编译 C++，怎么生成 Python 包？
怎么 install 到 package 里？
怎么打 wheel？
```

执行：

1. 保留已有 C++ target。
2. 增加 `_core` binding target。
3. `target_link_libraries(_core PRIVATE <cpp_lib>)`。
4. `install(TARGETS _core ... DESTINATION <package>)`。
5. 如有动态库，安装进同一 package 目录。
6. 配置 rpath / DLL 搜索路径。
7. 用 `scikit-build-core` 接入 wheel。

### D. import 失败或 wheel 失败

用户通常会贴错误：

```text
ModuleNotFoundError
DLL load failed
cannot open shared object file
dynamic module does not define module export function
unresolved Py_NegativeRefcount
```

执行：

1. 根据错误类型进入“错误处理决策树”。
2. 先检查 wheel 内容。
3. 再检查模块名、ABI、动态库路径。
4. 最后检查构建配置和平台差异。

---

## 3. 默认技术选型

除非用户明确指定，否则按以下顺序推荐：

| 场景 | 推荐方案 | 原因 |
|---|---|---|
| 普通 C++ 类/函数暴露给 Python | `pybind11` | 生态成熟，文档丰富，适合大多数项目 |
| 新项目、大量绑定、追求更轻编译 | `nanobind` | 现代、轻量、生成绑定代码效率高 |
| Python-first、NumPy/Buffer 深度集成 | `Cython` | 适合 Python 语义和数据处理 |
| 遗留 C/C++ 大接口快速导出 | `SWIG` | 自动化程度高，但 Python 风格较弱 |
| 只有稳定 C ABI | `CFFI` / `ctypes` | 简单，但不适合复杂 C++ 所有权模型 |

默认推荐：

```text
pybind11 + scikit-build-core + CMake
```

---

## 4. 必须遵守的设计规则

### 4.1 包布局规则

必须使用标准 Python package：

```text
my_project/
├── pyproject.toml
├── CMakeLists.txt
├── cpp/
│   ├── engine.cpp
│   ├── engine.h
│   └── bindings.cpp
├── src/
│   └── myengine/
│       ├── __init__.py
│       ├── runtime.py
│       └── py.typed
└── tests/
    └── test_import.py
```

### 4.2 命名规则

| 对象 | 规则 | 示例 |
|---|---|---|
| Python import 包名 | 小写，PEP 8 | `myengine` |
| PyPI/wheel 项目名 | 可与 import 名略有差异，但建议一致 | `myengine` |
| C++ 扩展模块名 | 以下划线开头，表示内部实现 | `_core` |
| CMake target 名 | 可带后缀保证唯一 | `_core_pybind11` |
| 磁盘输出模块名 | 必须和 import 名一致 | `_core.*.pyd` / `_core.*.so` |
| `PYBIND11_MODULE` 名 | 必须和 import 名一致 | `PYBIND11_MODULE(_core, m)` |

正确：

```cpp
PYBIND11_MODULE(_core, m) {
    m.def("init", []() {});
}
```

```python
from myengine import _core
```

错误：

```cpp
PYBIND11_MODULE(engine_core, m)
```

```python
from myengine import _core
```

### 4.3 交付规则

默认：

```text
开发期：pip install -e .
发布期：python -m build --wheel
```

禁止把以下方式作为正式交付主线：

```text
手动复制 .pyd/.so
长期依赖 PYTHONPATH
zip + PYTHONPATH
让用户手动改 sys.path
```

这些只能作为临时 smoke test。

---

## 5. 标准实现模板

### 5.1 pyproject.toml

```toml
[build-system]
requires = ["scikit-build-core>=0.10", "pybind11>=2.12"]
build-backend = "scikit_build_core.build"

[project]
name = "myengine"
version = "0.1.0"
description = "Python bindings for MyEngine"
requires-python = ">=3.9"

[tool.scikit-build]
wheel.packages = ["src/myengine"]
build-dir = "build/{wheel_tag}"
```

有 Python 依赖时：

```toml
[project]
name = "myengine"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = [
    "numpy>=1.24"
]
```

---

### 5.2 顶层 CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.20)

project(myengine LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)

add_library(engine SHARED
    cpp/engine.cpp
)
target_include_directories(engine PUBLIC cpp)

pybind11_add_module(_core
    cpp/bindings.cpp
)
target_link_libraries(_core PRIVATE engine)

if(APPLE)
  set_target_properties(_core PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "@loader_path"
  )
elseif(UNIX)
  set_target_properties(_core PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "$ORIGIN"
  )
endif()

install(TARGETS _core
    LIBRARY DESTINATION myengine
    RUNTIME DESTINATION myengine
)

install(TARGETS engine
    LIBRARY DESTINATION myengine
    RUNTIME DESTINATION myengine
)
```

说明：

- `_core` 是 Python 扩展模块。
- `engine` 是底层 C++ 动态库。
- 如果不需要独立动态库，也可以把 C++ 源码直接编进 `_core`。
- 如果 `engine` 是动态库，必须安装进 wheel。
- Linux/macOS 必须处理 rpath。
- Windows 必须处理 DLL 搜索路径。

---

### 5.3 绑定代码模板

```cpp
#include <pybind11/pybind11.h>

namespace py = pybind11;

void engine_init();
void engine_shutdown();
void engine_tick(float dt);

PYBIND11_MODULE(_core, m) {
    m.doc() = "Native bindings for myengine";

    m.def("init", &engine_init);
    m.def("shutdown", &engine_shutdown);
    m.def("tick", &engine_tick);
}
```

---

### 5.4 Python facade 模板

`src/myengine/__init__.py`：

```python
import os
import sys

if sys.platform == "win32":
    os.add_dll_directory(os.path.dirname(__file__))

from ._core import init, shutdown, tick
from .runtime import Engine

__all__ = ["Engine", "init", "shutdown", "tick"]
```

`src/myengine/runtime.py`：

```python
from . import _core


class Engine:
    def __init__(self, config_path: str):
        self._handle = _core.create_engine(config_path)

    def tick(self, delta_time: float) -> None:
        _core.tick(self._handle, delta_time)

    def shutdown(self) -> None:
        _core.destroy_engine(self._handle)
```

---

## 6. 标准执行步骤

### 6.1 开发期

执行：

```bash
pip install -e .
```

验证：

```bash
python -c "import myengine; print(myengine)"
python -c "from myengine import _core; print(_core)"
```

运行测试：

```bash
pytest
```

如果 editable install 失败，不要继续做 wheel 分发，先修开发安装。

---

### 6.2 构建 wheel

执行：

```bash
pip install build
python -m build --wheel
```

产物：

```text
dist/myengine-0.1.0-cp311-cp311-<platform>.whl
```

---

### 6.3 干净环境验证 wheel

Linux / macOS：

```bash
python -m venv .venv-test
source .venv-test/bin/activate
pip install dist/*.whl
python -c "import myengine"
python -c "from myengine import _core"
```

Windows PowerShell：

```powershell
python -m venv .venv-test
.venv-test\Scripts\Activate.ps1
pip install dist\*.whl
python -c "import myengine"
python -c "from myengine import _core"
```

---

### 6.4 检查 wheel 内容

执行：

```bash
python -m zipfile -l dist/*.whl
```

必须包含：

```text
myengine/__init__.py
myengine/_core.*.pyd 或 myengine/_core.*.so
```

如果有动态库依赖，还必须包含：

```text
myengine/engine.dll
myengine/libengine.so
myengine/libengine.dylib
```

---

## 7. 动态库加载规则

### 7.1 Windows

如果 `_core.pyd` 依赖 `engine.dll`，必须让 Python 能找到 DLL。

推荐在 `__init__.py` 顶部：

```python
import os
import sys

if sys.platform == "win32":
    os.add_dll_directory(os.path.dirname(__file__))
```

并确保 `engine.dll` 被安装到 package 目录：

```cmake
install(TARGETS engine
    RUNTIME DESTINATION myengine
)
```

### 7.2 Linux

设置 `_core` 的 rpath：

```cmake
set_target_properties(_core PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "$ORIGIN"
)
```

并确保依赖库安装到同目录：

```cmake
install(TARGETS engine
    LIBRARY DESTINATION myengine
)
```

### 7.3 macOS

设置 `_core` 的 rpath：

```cmake
set_target_properties(_core PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "@loader_path"
)
```

并确保依赖库安装到同目录：

```cmake
install(TARGETS engine
    LIBRARY DESTINATION myengine
)
```

---

## 8. 多平台 wheel

原生扩展 wheel 是平台和 Python ABI 相关的。

需要分别构建：

```text
Windows x64 + cp39/cp310/cp311/cp312
Linux x86_64 + cp39/cp310/cp311/cp312
macOS x86_64/arm64 + cp39/cp310/cp311/cp312
```

推荐使用 `cibuildwheel`。

### pyproject.toml 配置

```toml
[tool.cibuildwheel]
build = "cp39-* cp310-* cp311-* cp312-*"
test-command = "python -c \"import myengine; from myengine import _core\""
```

### 构建

```bash
pip install cibuildwheel
python -m cibuildwheel --output-dir wheelhouse
```

Linux 正式分发应生成 `manylinux` wheel，而不是只生成本机 `linux_x86_64.whl`。

---

## 9. 绑定方案替换指南

### 9.1 nanobind

替换 `pybind11` 相关配置：

```cmake
find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(_core
    cpp/bindings.cpp
)
target_link_libraries(_core PRIVATE engine)
```

其他包布局、install 规则、wheel 流程不变。

---

### 9.2 Cython

适用场景：

```text
Python-first API
NumPy / buffer protocol
已有 .pyx 代码
```

规则：

- 不要手工修改生成后的 `.cxx` 作为长期方案。
- 如果必须修补生成代码，必须在 CMake 中自动执行补丁。
- Windows Debug 下要特别处理 `_DEBUG` 和 Python Debug ABI 问题。

示例：

```cmake
set(CYTHON_OUTPUT_DIR "${CMAKE_CURRENT_BINARY_DIR}/cython_gen")

add_custom_command(
  OUTPUT ${CYTHON_OUTPUT_DIR}/_core.cxx
  COMMAND ${CYTHON_EXECUTABLE} --cplus -3
    -o ${CYTHON_OUTPUT_DIR}/_core.cxx
    ${CMAKE_CURRENT_SOURCE_DIR}/src/_core.pyx
  COMMAND ${CMAKE_COMMAND}
    -DGENERATED_FILE=${CYTHON_OUTPUT_DIR}/_core.cxx
    -P ${CMAKE_CURRENT_SOURCE_DIR}/cmake/patch_debug.cmake
  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/_core.pyx
)
```

Windows Debug 补丁原则：

```c
#if defined(_DEBUG) && defined(_MSC_VER) && _MSC_VER >= 1929
# include <corecrt.h>
#endif
#undef _DEBUG
#include "Python.h"
#define _DEBUG 1
```

注意：每次重新生成 Cython `.cxx` 后，都必须自动重新应用补丁。

---

### 9.3 SWIG

适用场景：

```text
遗留 C/C++ 大接口
多语言绑定
快速导出已有头文件
```

建议：

- SWIG 输出的 Python API 通常不够 Pythonic，应再包一层 facade。
- Windows Debug 下，如遇 Python Debug 符号问题，添加：

```cmake
target_compile_definitions(<target> PRIVATE
  $<$<AND:$<CONFIG:Debug>,$<PLATFORM_ID:Windows>>:SWIG_PYTHON_INTERPRETER_NO_DEBUG>
)
```

---

### 9.4 CFFI / ctypes

适用场景：

```text
只有稳定 C ABI
函数数量少
不暴露复杂 C++ 类所有权
```

规则：

- C++ 层必须导出 `extern "C"` C ABI。
- Python 侧负责对象生命周期包装。
- `.pyi` 通常需要手写。

---

## 10. 类型存根 `.pyi`

如果用户要求 IDE 补全、mypy、pyright 支持，可以生成 `.pyi`。

| 方案 | 工具 | 命令 |
|---|---|---|
| nanobind | 内置 | `python -m nanobind.stubgen -m _core -O src/myengine` |
| pybind11 | pybind11-stubgen | `pybind11-stubgen myengine._core -o src` |
| Cython | stubgen-pyx | `stubgen-pyx src --output-dir src/myengine` |
| SWIG | mypy stubgen | `stubgen -m myengine._core -o src` |
| CFFI / ctypes | 手写 | 无通用自动化 |

注意：

- 生成存根前，模块必须能 import。
- 存根不是构建成功的必要条件。
- 如果发布类型信息，应包含 `py.typed`。

---

## 11. 错误处理决策树

### 11.1 `ModuleNotFoundError: No module named '<package>'`

优先检查：

```bash
python -c "import sys; print(sys.executable)"
pip show <package>
```

判断：

- 没安装：执行 `pip install -e .`
- 安装到错的虚拟环境：切换解释器
- 包布局错误：检查 `src/<package>/__init__.py`
- wheel 没包含包：检查 `wheel.packages`

---

### 11.2 `dynamic module does not define module export function`

判断为 native 模块初始化函数名不匹配。

检查：

- `PYBIND11_MODULE(_core, m)`
- 生成文件名是否为 `_core.*.pyd` / `_core.*.so`
- Python 是否导入 `myengine._core`

修复：

```cpp
PYBIND11_MODULE(_core, m)
```

---

### 11.3 `DLL load failed while importing _core`

Windows 常见。

检查：

- `engine.dll` 是否在 wheel 的 `myengine/` 目录
- `__init__.py` 是否调用 `os.add_dll_directory`
- 是否混用了 Debug/Release CRT
- 是否安装了 VC++ runtime

---

### 11.4 `cannot open shared object file`

Linux 常见。

检查：

```bash
python -m zipfile -l dist/*.whl
```

确认 `.so` 是否存在。

修复：

```cmake
set_target_properties(_core PROPERTIES
    INSTALL_RPATH "$ORIGIN"
)
```

并安装依赖库到同目录。

---

### 11.5 macOS `Library not loaded`

检查：

- 依赖 `.dylib` 是否在 package 目录
- `_core` 是否设置 `@loader_path`
- 是否需要修复 install name

修复：

```cmake
set_target_properties(_core PROPERTIES
    INSTALL_RPATH "@loader_path"
)
```

---

### 11.6 Windows Debug 下 `Py_NegativeRefcount` / `Py_REF_DEBUG`

常见于 Cython / SWIG。

根因：

```text
MSVC /MDd 定义 _DEBUG
Python.h 因 _DEBUG 打开 Py_DEBUG / Py_REF_DEBUG
标准发行版 Python 没有 debug 符号
```

修复：

- pybind11 / nanobind：通常已内置处理
- SWIG：使用 `SWIG_PYTHON_INTERPRETER_NO_DEBUG`
- Cython：生成 `.cxx` 后自动补丁，不要手工补一次了事

---

## 12. 验收清单

完成任务前必须检查：

```text
[ ] 使用标准 src/<package> 包布局
[ ] 有 pyproject.toml
[ ] 有 CMakeLists.txt 或等价构建脚本
[ ] native 模块在 package 内，而不是项目根目录
[ ] C++ 模块名和 Python import 名一致
[ ] pip install -e . 成功
[ ] import <package> 成功
[ ] import <package>._core 成功
[ ] python -m build --wheel 成功
[ ] 干净虚拟环境安装 wheel 成功
[ ] wheel 内容包含 __init__.py 和 _core
[ ] 若有动态库依赖，依赖库已打进 wheel
[ ] Windows/Linux/macOS 动态库加载路径已处理
[ ] 至少有一个 import 测试
```

如果不能全部完成，在最终回复中明确说明未完成项和原因。

---

## 13. 输出规范

回答用户时，根据任务类型输出对应内容。

### 从零创建项目时

输出：

1. 推荐方案
2. 目录结构
3. `pyproject.toml`
4. `CMakeLists.txt`
5. 绑定代码
6. Python facade
7. 构建命令
8. 验证命令

### 修复已有项目时

输出：

1. 根因判断
2. 修改的文件
3. 修改理由
4. 验证结果
5. 剩余风险

### 只问概念时

输出：

1. 推荐结论
2. 原因
3. 典型目录结构
4. 最小命令

---

## 14. 最终原则

默认不要交付裸 native 模块。

正确交付物是：

```text
一个可 pip install 的 wheel
```

正确使用方式是：

```python
import myengine
```

内部实现可以是：

```python
from . import _core
```

核心原则：

```text
C++ 负责性能敏感逻辑；
Python package 负责稳定 API、安装体验和工具链集成；
wheel 负责跨机器、跨团队、跨 CI 的可靠交付。
```
