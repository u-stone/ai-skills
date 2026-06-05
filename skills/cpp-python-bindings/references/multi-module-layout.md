# 多模块项目布局

当一个 C++ 库有多个模块需要暴露给 Python，推荐使用一个 Python 顶层包，每个 C++ 模块对应一个 Python 子包和一个内部 native 扩展。

## 目录结构

```text
<project>/
├── pyproject.toml
├── CMakeLists.txt
├── cmake/
│   └── FindNativeLibrary.cmake
├── src/
│   └── <package>/
│       ├── __init__.py
│       ├── py.typed
│       ├── platform/
│       │   └── __init__.py       # from ._core import ...
│       ├── core/
│       │   └── __init__.py
│       └── render/
│           └── __init__.py
├── bindings/
│   ├── platform/
│   │   ├── module.cpp            # NB_MODULE(_core, m)
│   │   ├── types.cpp
│   │   └── app_info.cpp
│   ├── core/
│   └── render/
├── examples/
│   ├── run_all.py
│   ├── platform/
│   ├── core/
│   └── render/
└── tests/
    └── test_import.py
```

## 命名规则

| 对象 | 规则 | 示例 |
|------|------|------|
| Python 顶层包 | 小写、PEP 8 | `mypackage` |
| Python 子包 | 对应 C++ 模块 | `mypackage.platform` |
| native 扩展 | 下划线前缀，视为内部实现 | `mypackage.platform._core` |
| C++ 模块入口 | 与扩展短名一致 | `NB_MODULE(_core, m)` |
| CMake install 目录 | 与 import 目录一致 | `mypackage/platform` |

## 扩展新模块

1. 创建 `bindings/<module>/module.cpp` 和绑定文件。
2. 创建 `src/<package>/<module>/__init__.py`。
3. 在 CMake 中添加一个 `nanobind_add_module(_<ext> ...)` target。
4. 将 target 安装到 `<package>/<module>`。
5. 生成并提交 `.pyi` 存根。
6. 确保 `src/<package>/py.typed` 被包含进 wheel。

## py.typed

`py.typed` 是 PEP 561 标记文件，告诉类型检查器这个包包含类型信息。顶层包中放一个 `py.typed` 即可；如果 wheel 中缺少该文件，IDE 可能忽略已生成的 `.pyi`。
