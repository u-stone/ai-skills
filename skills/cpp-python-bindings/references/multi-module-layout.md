# 多模块项目布局

## 目录结构设计原则

当项目有多个 C++ 引擎模块需要绑定：

1. **每个 C++ 模块 → 一个 Python 子包**（`gwengine.platform`、`gwengine.core`）
2. **每个子包 → 一个 nanobind 扩展**（`_gwp`、`_gwcore`）
3. **绑定代码和 Python facade 分离**（`bindings/` vs `src/`）
4. **示例代码按模块镜像**（`examples/platform/`、`examples/core/`）

## 完整布局

```
<project>/
├── pyproject.toml
├── CMakeLists.txt
├── cmake/
│   └── FindEngine.cmake
├── src/
│   └── <package>/
│       ├── __init__.py           # 顶层 facade + DLL 搜索
│       ├── py.typed
│       ├── platform/             # GWPlatform 子包
│       │   └── __init__.py       # from ._gwp import ...
│       ├── core/                 # 未来：GWCore 子包
│       │   └── __init__.py
│       └── render/               # 未来：GWRenderEngine 子包
│           └── __init__.py
├── bindings/
│   ├── platform/                 # GWPlatform C++ 绑定
│   │   ├── module.cpp            # NB_MODULE(_gwp, m)
│   │   ├── types.cpp
│   │   ├── app_info.cpp
│   │   └── ...
│   ├── core/                     # 未来
│   └── render/                   # 未来
├── examples/
│   ├── run_all.py
│   ├── platform/                 # 示例：GWPlatform
│   │   ├── 01_system_info.py
│   │   └── ...
│   ├── core/                     # 未来
│   └── render/                   # 未来
├── tests/
│   └── test_import.py
├── scripts/
│   ├── setup.ps1                 # 一键构建
│   └── add_module.py             # 新模块脚手架
└── docs/
    └── binding-limitations.md
```

## 扩展新模块

### 方式 A：脚手架脚本

```bash
python scripts/add_module.py core       # → gwengine.core
python scripts/add_module.py render     # → gwengine.render
python scripts/add_module.py math       # → gwengine.math
```

自动创建：
- `bindings/<name>/module.cpp` + 骨架文件
- `src/<package>/<name>/__init__.py`
- 更新 `CMakeLists.txt`（添加 target）
- 更新顶层 `__init__.py`

### 方式 B：手动

1. 创建 `bindings/<name>/module.cpp` + 绑定文件
2. 创建 `src/<package>/<name>/__init__.py`
3. `CMakeLists.txt` 添加 `nanobind_add_module(_<ext> ...)` + `target_link_libraries`
4. 创建 `examples/<name>/` + 示例
5. 生成 `.pyi` 存根

## 文件命名约定

| 文件类型 | 规则 | 示例 |
|---------|------|------|
| 模块入口 | `module.cpp` | `bindings/platform/module.cpp` |
| 枚举/类型 | `<name>_types.cpp` | `types.cpp` |
| 类绑定 | `<class_snake>.cpp` | `app_info.cpp` |
| 绑定调度器 | `<name>_bind.cpp` | `platform_bind.cpp` |
| Python facade | `src/<package>/<name>/__init__.py` | `src/gwengine/platform/__init__.py` |
| nanobind 模块名 | `_<short>` | `_gwp`, `_gwcore`, `_gwrender` |
