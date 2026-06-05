# Python ABI 兼容性策略

原生扩展的 ABI 策略必须和 `requires-python`、CMake 选项、CI 矩阵保持一致。

## 策略选择

| 策略 | 构建次数 | 产物 | 适用场景 |
|------|---------|------|----------|
| 每版本构建 | 每个 Python 次版本一次 | `cp39-cp39-*`, `cp310-cp310-*`, `cp312-cp312-*` | 需要支持 Python 3.9-3.11 |
| 稳定 ABI | Python 3.12+ 一次 | `cp312-abi3-*` | 可以要求 Python >=3.12 |

不要同时声明 `requires-python = ">=3.9"` 和 `wheel.py-api = "cp312"` 作为默认模板。前者表示支持 3.9-3.11，后者表示发布 3.12+ 稳定 ABI wheel。

## 每版本构建

```toml
[project]
requires-python = ">=3.9"

[tool.scikit-build]
# 不设置 wheel.py-api
```

```toml
[tool.cibuildwheel]
build = "cp39-* cp310-* cp311-* cp312-* cp313-*"
test-command = "python -c 'import mypackage; import mypackage.platform'"
```

## 稳定 ABI（nanobind）

```cmake
nanobind_add_module(_core
    STABLE_ABI
    ${SOURCES})
```

```toml
[project]
requires-python = ">=3.12"

[tool.scikit-build]
wheel.py-api = "cp312"
```

```toml
[tool.cibuildwheel]
build = "cp312-*"
test-command = "python -c 'import mypackage; import mypackage.platform'"
```

## Free-threaded Python

Free-threaded Python 需要用 nanobind 的 `FREE_THREADED` 选项单独构建。目前 free-threaded 构建没有稳定 ABI，不要假设一个 `cp312-abi3` wheel 覆盖 free-threaded 解释器。

## 平台标签

Linux 分发应生成 `manylinux` 或 `musllinux` wheel，而不是裸 `linux_x86_64.whl`。macOS 和 Windows 也应在干净环境里安装 wheel 并执行至少一个 import 测试。
