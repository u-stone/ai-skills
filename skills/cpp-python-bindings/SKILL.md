---
name: cpp-python-native-package
description: >
  将 C++ 代码封装为标准 Python 原生扩展包，并通过 editable install 与 wheel 进行开发和交付。
  当用户提到 C++ 扩展、Python 绑定、pybind11、nanobind、Cython、SWIG、CFFI/ctypes、
  .pyd、.so、.dylib、Python 模块打包、pip install -e .、wheel、scikit-build-core、CMake、
  IDE 自动补全、.pyi 存根、STABLE_ABI、Python ABI 兼容性 时使用。
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

---

## 1. 先判断用户当前阶段

根据用户描述，把任务归入一个阶段。

### A. 从零创建项目 → 见 §2

### B. 已有 `.pyd` / `.so`，不知道放哪 → 见 §3

### C. 已有 CMake 构建，想接入 Python 包 → 见 §4

### D. import 失败或 wheel 失败 → 见 §10（错误处理决策树）

---

## 2. 从零创建项目的标准流程

### 2.1 选择绑定方案

| 场景 | 推荐方案 | 原因 |
|---|---|---|
| 普通 C++ 类/函数暴露给 Python | `pybind11` | 生态成熟，文档丰富 |
| 新项目、大量绑定、追求更轻编译 | `nanobind` | 编译快、二进制小、STABLE_ABI 支持清晰 |
| Python-first、NumPy/Buffer 深度集成 | `Cython` | Python 语义和数据处理 |
| 遗留 C/C++ 大接口快速导出 | `SWIG` | 自动化程度高 |
| 只有稳定 C ABI | `CFFI` / `ctypes` | 简单但不适合复杂 C++ |

默认推荐：`nanobind` + `scikit-build-core` + `CMake`。如果用户已有 pybind11 代码、团队标准或第三方示例，保留 pybind11，不为换框架而重写。

### 2.2 包布局（多模块项目）

当项目有多个 C++ 模块需要绑定时，使用 **按模块分层的布局**：

```text
<project>/
├── pyproject.toml
├── CMakeLists.txt                    # 双模式 CMake（独立 + 引擎集成）
├── cmake/
│   └── Find<Library>.cmake           # 查找预编译 C++ 库（可选）
├── src/
│   └── <package>/                    # Python 包根目录
│       ├── __init__.py               # 顶层 facade + DLL 路径
│       ├── py.typed
│       └── <module>/                 # 每个 C++ 模块对应一个子包
│           └── __init__.py           # 从 ._<ext> 重新导出 API
├── bindings/
│   └── <module>/                     # C++ 绑定代码
│       ├── module.cpp                # NB_MODULE(_<ext>, m) 入口
│       ├── <class>_bind.cpp          # 各类绑定
│       └── ...
├── examples/
│   └── <module>/                     # 示例代码（按模块组织）
├── tests/
│   └── test_import.py
├── scripts/
│   ├── setup.ps1                     # 一键构建
│   ├── build_wheel.ps1               # 打包 wheel
│   └── add_module.py                 # 新模块脚手架
└── docs/
    └── binding-limitations.md        # 绑定限制参考
```

**命名规则**：

| 对象 | 规则 | 示例 |
|---|---|---|
| Python import 包名 | 小写，PEP 8 | `mypackage` |
| C++ 扩展模块名 | 以下划线开头，表示内部实现 | `_core`=`mypackage.platform._core` |
| 磁盘输出模块名 | 必须和 import 名一致 | `_core.*.pyd` / `_core.*.so` |
| `NB_MODULE` 名 | 必须和 import 名一致 | `NB_MODULE(_core, m)` |

### 2.3 编写构建文件

详见 `references/build-templates.md`：
- `pyproject.toml` 模板
- `CMakeLists.txt` 模板（双模式：独立 + 引擎集成）
- `Find<Library>.cmake` 模板（预编译库发现）

### 2.4 编写绑定代码

详见 `references/binding-patterns.md`：
- 静态类绑定（`def_static`）
- 枚举绑定（`nb::enum_`）
- 重载函数处理（lambda 消歧义）
- 只读静态属性（`def_prop_ro_static`）
- 返回策略（`rv_policy::reference`）

### 2.5 Python facade

```python
# src/<package>/<module>/__init__.py
import os, sys

_pkg_dir = os.path.dirname(__file__)
if sys.platform == "win32":
    os.add_dll_directory(_pkg_dir)
    # 开发期可通过环境变量加入依赖 DLL 目录；变量名按项目替换。
    _native_bin = os.environ.get("NATIVE_LIBRARY_BIN_DIR", "")
    if _native_bin:
        os.add_dll_directory(_native_bin)

from ._<ext> import ClassA, ClassB, EnumC

__all__ = ["ClassA", "ClassB", "EnumC"]
```

### 2.6 构建与验证

```bash
# 1) 开发安装
pip install -e . --config-settings="cmake.define.NATIVE_LIBRARY_BUILD_DIR=/path/to/build"

# 2) 验证
python -c "import <package>; from <package>.<module> import ClassA; print(ClassA.method())"

# 3) 打 wheel
python -m build --wheel

# 4) 干净环境验证
python -m venv .venv-test && .venv-test/Scripts/pip install dist/*.whl
python -c "import <package>"
```

---

## 3. 已有 `.pyd` / `.so`，不知道放哪

1. 放进 `src/<package>/` 的对应子目录。
2. 创建 `__init__.py` 作为 facade。
3. 检查 native 模块名是否和初始化函数一致。
4. 引导改成 `pip install -e .`。
5. 不把 `PYTHONPATH` 作为正式方案。

---

## 4. 已有 CMake 构建，想接入 Python 包

1. 保留已有 C++ target，不修改原有代码。
2. 增加独立的 binding target（`nanobind_add_module` / `pybind11_add_module`）。
3. `target_link_libraries(_<ext> PRIVATE <cpp_target>)`。
4. 使用**双模式 CMake**：检测 `TARGET <cpp_target>` 是否存在来自动切换。

```cmake
if(TARGET NativeLibrary)
    # 集成模式：直接链接已有 CMake target
    set(NATIVE_LIBRARY_TARGETS NativeLibrary)
else()
    # 独立模式：查找预编译库
    include(cmake/FindNativeLibrary.cmake)
endif()
```

5. `install(TARGETS _<ext> ... DESTINATION <package>/<module>)`。
6. 如有动态库，安装进同一 package 目录并配置 rpath。
7. 用 `scikit-build-core` 接入 wheel。

---

## 5. IDE 自动补全配置

`_<ext>.pyd` 是编译后的二进制，VS Code / Pylance 无法直接从 `.pyd` 提取类型信息。必须生成 **`.pyi` 类型存根文件**。

### 5.1 生成 .pyi 存根

nanobind 内置 stub 生成器：

```bash
python -m nanobind.stubgen -m <package>.<module>._<ext> -o src/<package>/<module>
```

生成产物 `_<ext>.pyi` 包含所有类、方法、枚举的类型签名。**应提交到 Git**。

### 5.2 VS Code 配置

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "C:\\...\\python.exe",
    "python.analysis.extraPaths": ["${workspaceFolder}/src"],
    "python.autoComplete.extraPaths": ["${workspaceFolder}/src"]
}
```

```json
// .vscode/launch.json — 调试配置
{
    "name": "Example: <name>",
    "type": "debugpy",
    "request": "launch",
    "program": "${workspaceFolder}/examples/<module>/script.py",
    "python": "${command:python.interpreterPath}",
    "env": {
        "NATIVE_LIBRARY_BIN_DIR": "${workspaceFolder}/../../build/bin/Debug",
        "PYTHONPATH": "${workspaceFolder}/src"
    },
    "justMyCode": false
}
```

关键：`NATIVE_LIBRARY_BIN_DIR` 确保 DLL 可找到；`justMyCode: false` 只影响 Python 调试器是否进入第三方 Python 代码。要调试 `.pyd` / `.so` 内的 C++，需要附加原生调试器（MSVC、LLDB 或 GDB）。

### 5.3 其他 IDE

- **PyCharm**: 将 `src/` 标记为 Sources Root。
- **通用**: 确保解释器是安装了包的版本（`pip install -e .` 注册到 site-packages）。

### 5.4 常见问题

**VS Code 选择了错误 Python 版本** → `ModuleNotFoundError: No module named '<package>.<module>._<ext>'`。

修复：`Ctrl+Shift+P` → `Python: Select Interpreter` → 选择安装了包的版本。或在 `settings.json` 中设置 `python.defaultInterpreterPath`。

---

## 6. C/C++ 绑定限制与应对

不同 C++ 模式对绑定的友好程度不同。详见 `references/binding-limitations.md`。

### 快速对照表

| C/C++ 模式 | 支持 | 应对 |
|-----------|------|------|
| 静态成员函数、枚举、构造函数 | ✅ 直接 | `def_static` / `nb::enum_` / `nb::init<>` |
| STL 容器 (`vector`, `map`, `string`) | ⚠️ 需显式 `#include` | `#include <nanobind/stl/vector.h>` 等 |
| 函数重载 | ⚠️ 需消歧义 | Lambda 包装 |
| 原始函数指针（C 回调） | ⚠️ 需适配器 | `nb::capsule` / 全局 `std::function` |
| `void*` 不透明指针 | ⚠️ 需 capsule | `nb::capsule(ptr, "name")` |
| 非内联静态常量 | ⚠️ 需 lambda getter | `def_prop_ro_static("x", [](nb::handle){ return X; })` |
| printf 变参 | ❌ 需包装 | Lambda 接受 `std::string` |
| 模板类 | ❌ 需显式实例化 | `nb::class_<RingBufferT<int>>` |
| private/protected 成员 | ❌ 无法访问 | 仅通过 public 接口 |
| 条件编译 (`#ifdef`) | ❌ 需镜像守卫 | 绑定代码中也加 `#ifdef` |
| `#define` 宏冲突 (win32 `ERROR`) | — | `#undef` + 完全限定名 |

### 检查清单（添加新绑定前）

```
[ ] 函数重载？ → lambda 消歧义
[ ] void* 参数/返回值？ → 跳过或 nb::capsule
[ ] 函数指针（回调）？ → 跳过或适配器
[ ] 返回引用（非所有权）？ → rv_policy::reference
[ ] printf 变参？ → lambda 包装为 std::string
[ ] 模板类？ → 显式实例化
[ ] static const 成员？ → def_prop_ro_static lambda
[ ] 使用 std::vector/map？ → 包含对应 nanobind/stl/*.h
[ ] #ifdef 守卫？ → 绑定代码中镜像
[ ] private 成员需暴露？ → 仅在 public getter 存在时绑定
[ ] windows.h ERROR 等宏冲突？ → #undef + 完全限定名
```

---

## 7. 是否需要受限的 C/C++ 导出层

### 问题

直接绑定现有的 C++ API 头文件时，会遇到：
- 过于宽泛的接口（大量平台特定方法）
- `void*` 句柄和函数指针回调
- 复杂的 include 链导致不必要的依赖
- 没有考虑 Python 侧的惯用法

### 推荐：添加一个薄 C ABI 适配层

当以下条件任一条成立时，考虑在 C++ 库和 Python 绑定之间**插入一个受限的导出层**：

1. **C++ 类有复杂生命周期**（需要 RAII、引用计数等）→ 用 `extern "C"` 函数包装创建/销毁
2. **API 大量使用回调** → C 适配层将 Python callable 转为 `void*` context + 函数指针对
3. **需要跨语言错误传递** → C 适配层将 C++ 异常转为错误码
4. **需要瘦身接口** → 只暴露 Python 实际需要的子集
5. **header 依赖链复杂** → 适配层头文件只 include 最少依赖

```cpp
// thin_adapter.h —— 受限的 C ABI 导出层
#pragma once
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef void* NativeHandle;
typedef void (*MessageCallback)(const char* key, const char* value, void* ctx);

NativeHandle native_create(const char* config_path);
void         native_destroy(NativeHandle h);
int          native_tick(NativeHandle h, float dt);
void         native_register_callback(NativeHandle h, MessageCallback cb, void* ctx);

#ifdef __cplusplus
}
#endif
```

优点：
- nanobind/pybind11 绑定变得简单：只绑定 C 函数
- 跨语言边界清晰（只传递基本类型 + 不透明句柄）
- 错误处理统一（C++ 异常在适配层内部捕获，转为错误码返回）

代价：
- 多一层间接调用
- 需要维护适配层代码

**总结**：先评估是否需要薄 C ABI 适配层，不要默认增加一层。以下场景中通常值得添加：
- 需要跨 Python 版本/跨平台分发
- API 涉及复杂生命周期或回调
- 原始 C++ 接口过于庞大（>50 个公共方法）

---

## 8. Python ABI 兼容性与跨版本分发

### 8.1 原生扩展与 Python 版本绑定

`.pyd` / `.so` 链接了特定的 `python3X.dll`，因此**默认绑定到一个 Python 次版本**：

```
_core.cp312-win_amd64.pyd       →  每版本 ABI，只能由 Python 3.12 加载
_core.cp312-abi3-win_amd64.pyd  →  稳定 ABI，可由 Python 3.12+ 加载
```

### 8.2 两种分发策略

| 策略 | 构建次数 | 产物 | 适用场景 |
|------|---------|------|---------|
| **每版本构建** | N 次（每个 Python 版本） | `cp312-*.whl`, `cp313-*.whl`, ... | 需要支持 <3.12 的旧版本 |
| **稳定 ABI**（推荐） | **1 次**（3.12+） | `cp312-abi3-*.whl` → 3.12/3.13/3.14 通用 | 可以要求 >=3.12 |

### 8.3 启用 STABLE_ABI（nanobind）

```cmake
# CMakeLists.txt
nanobind_add_module(_core ${SOURCES}
    STABLE_ABI    # 一个 .pyd 兼容 Python 3.12+
)
```

```toml
# pyproject.toml
[tool.scikit-build]
wheel.py-api = "cp312"  # 标记为稳定 ABI wheel
```

**限制**：如果发布稳定 ABI wheel，`requires-python` 必须与 `wheel.py-api = "cp312"` 对齐，通常设为 `>=3.12`。如果必须支持 3.9-3.11，使用每版本构建，不要同时声明 cp312 稳定 ABI。

**不影响**：nanobind 绑定语法、STL 转换、异常处理、GIL 管理均无变化。

**额外注意**：
- Python debug 构建（`python_d.exe`）不兼容 STABLE_ABI；需单独编译 debug 版本
- Free-threaded Python（3.13t）需额外 `FREE_THREADED` 标志；目前 free-threaded 构建没有稳定 ABI，不能依赖 `STABLE_ABI`
- 自定义 `nb::type_slots()` 使用少数 CPython 特有 slot 时不兼容（罕见）

### 8.4 多 Python 版本的开发环境

每个 Python 安装需要分别 `pip install -e .`：

```bash
& "C:\Python312\python.exe" -m pip install -e . --config-settings="cmake.define.NATIVE_LIBRARY_BUILD_DIR=..."
& "C:\Python314\python.exe" -m pip install -e . --config-settings="cmake.define.NATIVE_LIBRARY_BUILD_DIR=..."
```

**VS Code**: 通过 `python.defaultInterpreterPath` 指定默认解释器，或 `Ctrl+Shift+P` 切换。

---

## 9. 多模块项目扩展

从一个模块扩展到多个模块时的步骤：

### 9.1 手动添加

1. 创建 `bindings/<new_module>/` + `module.cpp`
2. 创建 `src/<package>/<new_module>/__init__.py`
3. 在 `CMakeLists.txt` 中添加 `nanobind_add_module(_<ext> ...)` + `target_link_libraries`
4. 创建 `examples/<new_module>/` + 示例脚本
5. 生成 `.pyi` 存根

### 9.2 使用脚手架脚本

```bash
python scripts/add_module.py <new_module>
```

自动创建：绑定 C++ 骨架、Python facade、CMake target、更新 `__init__.py`。

---

## 10. 错误处理决策树

### 10.1 `ModuleNotFoundError: No module named '<package>'`

判断：
- 没安装 → `pip install -e .`
- 安装到错的 Python 版本 → 检查 `python -c "import sys; print(sys.executable)"`
- 包布局错误 → 检查 `src/<package>/__init__.py`
- VS Code 选择错误解释器 → `Ctrl+Shift+P` 选择安装了包的版本

### 10.2 `dynamic module does not define module export function`

模块初始化函数名与文件名不匹配。检查 `NB_MODULE(_name, m)` 与 `.pyd` 文件名一致。

### 10.3 `DLL load failed while importing _<ext>`

Windows 常见。检查：
- 依赖 DLL 是否在搜索路径中（`os.add_dll_directory`、项目自定义 `*_BIN_DIR` 环境变量）
- **Debug/Release CRT 混用**：Debug 引擎 + Release 绑定 → 随机堆损坏
  - 修复：统一构建配置（`cmake.define.CMAKE_BUILD_TYPE=Debug`）
- 传递依赖是否齐全（FFmpeg、VLD、OpenSSL 等——仅 Debug 引擎加载时检查所有传递依赖）
- VC++ runtime 是否安装

### 10.4 Linux `cannot open shared object file` / macOS `Library not loaded`

设置 rpath + 确保依赖库安装到同目录。详见 §2.5 和 §4。

### 10.5 MSVC `invalid integer constant expression` (Log.h)

`windows.h` 将 `ERROR` 定义为宏 → 与 `enum Error` 冲突。
修复：`#undef ERROR` + 使用完全限定名 `namespace::Error`。

---

## 11. 动态库加载规则

### 11.1 Windows

`__init__.py` 中调用 `os.add_dll_directory()`；引擎 DLL 安装到同目录。

### 11.2 Linux

`INSTALL_RPATH "$ORIGIN"` 让 `.so` 在其自身目录搜索依赖。

### 11.3 macOS

`INSTALL_RPATH "@loader_path"` 同上。

---

## 12. 验收清单

```text
[ ] 使用标准 src/<package> 包布局（多模块项目按模块分层）
[ ] 有 pyproject.toml + CMakeLists.txt（双模式）
[ ] native 模块在 package 内，非项目根目录
[ ] C++ 模块名和 Python import 名一致
[ ] .pyi 类型存根已生成并提交到 Git
[ ] .vscode/settings.json 配置了 python.analysis.extraPaths
[ ] pip install -e . 成功
[ ] import <package> 成功
[ ] python -m build --wheel 成功
[ ] 干净虚拟环境安装 wheel 成功
[ ] 若有动态库依赖，依赖库已打进 wheel
[ ] Windows/Linux/macOS 动态库加载路径已处理
[ ] STABLE_ABI 或每版本构建策略已确定
[ ] 至少有一个 import 测试
[ ] Binding limitations 检查清单已完成（§6）
```

---

## 13. 最终原则

- 默认不交付裸 native 模块。
- 正确交付物：**一个可 pip install 的 wheel**。
- C++ 负责性能敏感逻辑；Python package 负责稳定 API、安装体验和工具链集成；wheel 负责跨机器、跨团队、跨 CI 的可靠交付。

---

## 14. 参考文件

详细模板和深入讨论见以下文件：

| 文件 | 内容 |
|------|------|
| `references/build-templates.md` | pyproject.toml、CMakeLists.txt、Find<Library>.cmake 完整模板 |
| `references/binding-patterns.md` | 绑定代码模式：静态类、枚举、重载、回调、返回值策略 |
| `references/binding-limitations.md` | C/C++ 模式限制与应对（13 种模式 + 检查清单） |
| `references/python-abi-strategies.md` | Python ABI 版本策略、STABLE_ABI 详细分析、cibuildwheel 配置 |
| `references/ide-autocomplete.md` | VS Code / PyCharm 自动补全配置、.pyi 存根生成、launch.json 调试 |
| `references/multi-module-layout.md` | 多模块项目目录结构设计、扩展步骤、脚手架脚本 |
