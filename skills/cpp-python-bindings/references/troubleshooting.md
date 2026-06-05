# C++/Python 原生扩展排错指南

本文件只保留可复用的排错模式，避免绑定到某个具体项目脚本或目录结构。

## 1. `ModuleNotFoundError: No module named '<package>'`

检查顺序：

1. 是否在当前解释器执行过 `pip install -e .`。
2. IDE 选择的解释器是否与命令行一致。
3. `src/<package>/__init__.py` 是否存在。
4. native 扩展是否安装到 import 路径对应目录，例如 `<package>/<module>/_core.*.pyd`。

## 2. `dynamic module does not define module export function`

native 扩展文件名和初始化函数不一致。

- nanobind：`NB_MODULE(_core, m)` 必须匹配 `_core.*.pyd` / `_core.*.so`。
- pybind11：`PYBIND11_MODULE(_core, m)` 必须匹配 `_core.*.pyd` / `_core.*.so`。

## 3. Windows `DLL load failed while importing _<ext>`

常见原因：

- 依赖 DLL 不在搜索路径中；
- Debug/Release CRT 混用；
- 传递依赖缺失；
- VC++ runtime 未安装。

处理方式：

```python
# src/<package>/<module>/__init__.py
import os
import sys

if sys.platform == "win32":
    os.add_dll_directory(os.path.dirname(__file__))
    native_bin = os.environ.get("NATIVE_LIBRARY_BIN_DIR")
    if native_bin:
        os.add_dll_directory(native_bin)
```

开发期确保 C++ 库和 Python 扩展使用同一构建类型。Release Python 通常不提供 `python3xx_d.lib`，不要让普通 Debug 扩展强行依赖 debug Python。

## 4. Linux / macOS 找不到依赖库

Linux 使用 `$ORIGIN`，macOS 使用 `@loader_path`，让扩展从自身目录查找随 wheel 分发的动态库。

```cmake
if(APPLE)
    set_target_properties(_core PROPERTIES INSTALL_RPATH "@loader_path")
elseif(UNIX)
    set_target_properties(_core PROPERTIES INSTALL_RPATH "$ORIGIN")
endif()
```

## 5. 返回引用导致崩溃

当 C++ 返回内部对象引用或指针时，不要依赖默认返回策略。

pybind11：

```cpp
py::class_<NativeObject>(m, "NativeObject")
    .def("get_child", &NativeObject::get_child,
         py::return_value_policy::reference_internal);
```

nanobind：

```cpp
nb::class_<NativeObject>(m, "NativeObject")
    .def("get_child", &NativeObject::get_child,
         nb::rv_policy::reference_internal);
```

## 6. Windows 宏冲突

`windows.h` 可能定义 `ERROR`、`min`、`max` 等宏，破坏枚举或函数名。

```cpp
#define NOMINMAX
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#ifdef ERROR
#  undef ERROR
#endif
```

## 7. ABI 策略不一致

症状：wheel 文件名、Python 版本声明和实际可安装版本不一致。

规则：

- 支持 Python 3.9-3.11：每版本构建，不设置 `wheel.py-api = "cp312"`。
- 使用 `STABLE_ABI`：`requires-python = ">=3.12"`，并设置 `wheel.py-api = "cp312"`。
- free-threaded Python 单独构建，不假设被 `abi3` wheel 覆盖。

## 8. 最小验证命令

```bash
pip install -e .
python -c "import <package>; import <package>.<module>"
python -m build --wheel
python -m venv .venv-wheel-test
.venv-wheel-test/Scripts/pip install dist/*.whl
.venv-wheel-test/Scripts/python -c "import <package>; import <package>.<module>"
```

在 Linux/macOS 上把最后两行换成对应的 `bin/pip` 和 `bin/python`。
