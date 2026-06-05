# Python ABI 兼容性策略

## 原生扩展与 Python 版本绑定

`.pyd` / `.so` 链接了特定的 `python3X.dll`，因此默认绑定到一个 Python 次版本。

## 两种分发策略

| 策略 | 构建次数 | 产物 | 适用 |
|------|---------|------|------|
| 每版本构建 | N 次 | `cp312-*.whl`, `cp313-*.whl` | 需支持 <3.12 |
| **稳定 ABI** | **1 次** | `cp312-abi3-*.whl` → 3.12+ | 可要求 >=3.12 |

## 启用 STABLE_ABI

```cmake
nanobind_add_module(_core ${SOURCES}
    STABLE_ABI    # 一个 .pyd 兼容 Python 3.12+
)
```

```toml
[tool.scikit-build]
wheel.py-api = "cp312"
```

## STABLE_ABI 影响分析

### 已确认的影响

| # | 影响 | 严重程度 |
|---|------|---------|
| 1 | Python >= 3.12 才启用（旧版静默回退） | 低——不影响兼容性 |
| 2 | 二进制体积减小 5-10% | 正面 |
| 3 | 不能直接访问 CPython 结构体字段 | nanobind 透明处理 |
| 4 | 部分 CPython API 函数不可用 | 不在 nanobind 使用范围 |
| 5 | 自定义 type slots 可能受限 | 大多数项目不使用 |
| 6 | Python debug 构建不兼容 | 需单独编译 debug 版 |
| 7 | Free-threaded 需额外 `FREE_THREADED` 标志 | 一行 CMake 即可 |

### 不影响的方面

nanobind 绑定语法、STL 转换、异常处理、GIL 管理、回调适配、跨平台（Win/Linux/macOS）、`pip install -e .` 开发流程——全部无变化。

## 多 Python 版本开发

每个 Python 安装需要分别 `pip install -e .`：

```bash
& "C:\Python312\python.exe" -m pip install -e . --config-settings="cmake.define.ENGINE_BUILD_DIR=..."
& "C:\Python314\python.exe" -m pip install -e . --config-settings="cmake.define.ENGINE_BUILD_DIR=..."
```

## cibuildwheel 跨平台构建

```toml
[tool.cibuildwheel]
build = "cp39-* cp310-* cp311-* cp312-*"
test-command = "python -c 'import mypackage'"
```

```bash
pip install cibuildwheel
cibuildwheel --output-dir wheelhouse
```

Linux 应生成 `manylinux` wheel，而非裸 `linux_x86_64.whl`。
