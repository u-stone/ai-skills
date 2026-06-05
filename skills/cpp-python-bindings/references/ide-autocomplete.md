# IDE 自动补全配置

`_<ext>.pyd` / `_<ext>.so` 是编译后的二进制模块，Pylance、Pyright 和多数 IDE 不能可靠地从二进制中提取完整类型信息。应生成 `.pyi` 存根，并提交 `py.typed` 作为 PEP 561 标记。

## .pyi 存根生成

```bash
# nanobind
python -m nanobind.stubgen -m <package>.<module>._<ext> -o src/<package>/<module>

# pybind11
pip install pybind11-stubgen
pybind11-stubgen <package>.<module>._<ext> -o src
```

生成后检查：

- `src/<package>/<module>/_<ext>.pyi` 存在；
- `src/<package>/py.typed` 存在；
- wheel 安装后仍能看到 `.pyi` 和 `py.typed`。

`py.typed` 可以是空文件，也可以只包含注释：

```text
# PEP 561 marker
```

## VS Code 配置

```json
{
  "python.defaultInterpreterPath": "/path/to/python",
  "python.analysis.extraPaths": ["${workspaceFolder}/src"],
  "python.analysis.typeCheckingMode": "basic"
}
```

## 调试配置

```json
{
  "name": "Example: <name>",
  "type": "debugpy",
  "request": "launch",
  "program": "${workspaceFolder}/examples/<module>/script.py",
  "python": "${command:python.interpreterPath}",
  "cwd": "${workspaceFolder}",
  "env": {
    "NATIVE_LIBRARY_BIN_DIR": "${workspaceFolder}/../../build/bin/Debug",
    "PYTHONPATH": "${workspaceFolder}/src"
  },
  "justMyCode": false
}
```

`justMyCode: false` 只让 Python 调试器进入第三方 Python 代码。要单步调试 `.pyd` / `.so` 内的 C++，需要附加原生调试器，例如 Visual Studio、VS Code C++ 调试器、LLDB 或 GDB。

## 常见问题

**`ModuleNotFoundError: No module named '<package>.<module>._<ext>'`**

常见原因：VS Code 选择的 Python 解释器没有安装该包。

修复：

1. `Ctrl+Shift+P` → `Python: Select Interpreter` → 选择安装了包的解释器。
2. 对当前解释器重新执行 `pip install -e . --config-settings="cmake.define.NATIVE_LIBRARY_BUILD_DIR=..."`。
3. 确认 `python -c "import sys; print(sys.executable)"` 与 IDE 解释器一致。

## 其他 IDE

- PyCharm：将 `src/` 标记为 Sources Root。
- 通用：确保解释器是执行过 `pip install -e .` 的解释器。
