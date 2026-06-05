# 各脚本语言的 C API 封装要点

## Lua (via Lua C API / Sol3)

| C API 模式 | Lua 封装 |
|-----------|---------|
| `const char*` | `lua_pushstring(L, str)` |
| `uint8_t*` + `size_t` | `lua_pushlstring(L, data, size)` |
| Opaque handle | `lua_newuserdata` + metatable，或 lightuserdata |
| C 回调 + void* context | 在 context 中存 lua_State + function ref；回调中 `lua_rawgeti` + `lua_pcall` |
| 错误码 | `lua_pushnil` + `lua_pushstring(L, error_msg)` 或 `luaL_error` |
| Handle destroy | metatable `__gc` 自动调用 `destroy` |

**注意**：
- Lua 5.1/5.2/5.3 的 `lua_Integer` 大小不同（32/64 位），用 `int64_t` 确保一致
- Lua 不原生支持多线程，不要假设 C 回调可在 Lua 线程外安全执行

---

## Python (via nanobind / pybind11)

| C API 模式 | Python 封装 |
|-----------|------------|
| `const char*` | `nb::arg("name").c_str()` → `str` |
| `uint8_t*` + `size_t` | `nb::arg("data").noconvert()` → `bytes` |
| Opaque handle | `nb::class_<MyEngine_t>(m, "Engine")` |
| C 回调 + void* context | `nb::capsule(ctx, "ctx")` + lambda 包装 |
| 错误码 | nanobind 侧抛 `nb::python_error` 或 Python `RuntimeError` |
| Handle destroy | `nb::class_` 的 `__del__` 中调 `destroy`；或 `nb::rv_policy::take_ownership` |

**注意**：
- GIL 保护：回调需要在 Python C API 中获取 GIL
- STABLE_ABI 下不能直接操作 `PyObject*` 字段，必须用 API 函数

---

## C# (via P/Invoke / SWIG)

| C API 模式 | C# 封装 |
|-----------|---------|
| `const char*` | `[MarshalAs(UnmanagedType.LPUTF8Str)] string` |
| `uint8_t*` + `size_t` | `byte[]` + `ref int size` |
| Opaque handle | `IntPtr`（不用 `SafeHandle` 除非需要 finalizer） |
| C 回调 + void* context | `[UnmanagedFunctionPointer] delegate` + `GCHandle` 保活 |
| 错误码 | 检查返回值 + `Marshal.ThrowExceptionForHR` |
| Handle destroy | `IDisposable` + `Dispose()` 中调 `destroy` |

**注意**：
- delegate 必须用 `GCHandle.Alloc(delegate, GCHandleType.Normal)` 保活，否则 GC 可能回收正在等待回调的 delegate
- Windows/Android/iOS 的字符串编码不同（UTF-8/ANSI），始终用 `LPUTF8Str`

---

## JavaScript (via Emscripten / Node-FFI)

| C API 模式 | JS 封装 |
|-----------|---------|
| `const char*` | `UTF8ToString(ptr)` / `stringToUTF8(str)` |
| `uint8_t*` + `size_t` | `new Uint8Array(Module.HEAPU8.buffer, ptr, size)` |
| Opaque handle | `number`（指针值存为 Number；注意 64 位溢出） |
| C 回调 + void* context | `Module.addFunction(fn, 'viii')` + `Runtime.dynCall` |
| 错误码 | JS 侧检查返回值 + throw |
| Handle destroy | 手动调用 `destroy`（JS 无自动 finalizer） |

**注意**：
- Emscripten 的指针是 `int32_t`，64 位平台用 `BigInt` 或 `WASM_BIGINT`
- `addFunction` 有数量限制，大量回调需要池化管理

---

## 各语言共性问题

### 字符串编码

始终使用 **UTF-8**。避免在 C API 中暴露平台本地编码（Windows ANSI、Shift-JIS 等）。Python 和 Lua 默认 UTF-8；C# 需要 `LPUTF8Str`；JS 的 `TextEncoder/TextDecoder` 默认 UTF-8。

### 回调线程安全

如果 C 层在非主线程触发回调：
- **Python**: 回调中获取 GIL（`nb::gil_scoped_acquire`），注意避免死锁
- **Lua**: 不能在工作线程调 Lua C API（lua_State 不是线程安全的）；push 到主线程事件队列
- **C#**: 用 `SynchronizationContext.Post` 切回主线程
- **JS**: 用 `postMessage` 或 `Atomics` 通信（JS 是单线程的）

### 推荐：在 C API 层就限制回调线程

```c
/** 注册日志回调。[thread] 回调仅从主线程调用。 */
int my_engine_set_log_callback(MyEngine* engine, LogCallback cb, void* ctx);
```

在 C API 层保证回调线程模型，脚本语言封装就不需要处理线程安全问题。
