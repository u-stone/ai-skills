# IDE 自动补全配置

## 为什么需要额外配置

`_<ext>.pyd` 是编译后的二进制，VS Code / Pylance 无法直接从 `.pyd` 提取类型信息。必须生成 `.pyi` 类型存根文件。

## .pyi 存根生成

```bash
# nanobind（内置工具）
python -m nanobind.stubgen -m <package>.<module>._<ext> -O src/<package>/<module>

# pybind11（第三方工具）
pip install pybind11-stubgen
pybind11-stubgen <package>._<ext> -o src
```

生成产物 `_<ext>.pyi` 包含所有类、方法、枚举的类型签名。**应提交到 Git**，这样 clone 后即获得自动补全。

## VS Code 配置

### settings.json

```json
{
    "python.defaultInterpreterPath": "/path/to/python.exe",
    "python.analysis.extraPaths": ["${workspaceFolder}/src"],
    "python.autoComplete.extraPaths": ["${workspaceFolder}/src"],
    "python.analysis.typeCheckingMode": "basic"
}
```

### launch.json（调试配置）

```json
{
    "name": "Example: <name>",
    "type": "debugpy",
    "request": "launch",
    "program": "${workspaceFolder}/examples/<module>/script.py",
    "python": "${command:python.interpreterPath}",
    "cwd": "${workspaceFolder}",
    "env": {
        "ENGINE_BIN_DIR": "${workspaceFolder}/../../build/bin/Debug",
        "PYTHONPATH": "${workspaceFolder}/src"
    },
    "justMyCode": false
}
```

关键点：
- `ENGINE_BIN_DIR` → 确保 .pyd 能找到依赖 DLL
- `PYTHONPATH` → 包含 `src/`，让 Pylance 发现包
- `justMyCode: false` → 允许单步进入 .pyd 的 C++ 层

## 常见问题

**`ModuleNotFoundError: No module named '<package>.<module>._<ext>'`**

原因：VS Code 选择的 Python 解释器未安装该包。

修复：
1. `Ctrl+Shift+P` → `Python: Select Interpreter` → 选择安装了包的版本
2. 或为当前版本重新安装：`pip install -e . --config-settings="cmake.define.ENGINE_BUILD_DIR=..."`
3. 或在 `settings.json` 中设置 `python.defaultInterpreterPath`

## 其他 IDE

- **PyCharm**: 将 `src/` 标记为 Sources Root（右键 → Mark Directory as → Sources Root）
- **通用**: 确保 Python 解释器是安装了包的那个
