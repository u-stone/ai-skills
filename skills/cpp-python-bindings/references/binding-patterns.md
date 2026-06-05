# 绑定代码模式

## 静态类绑定

```cpp
nb::class_<MyClass>(m, "MyClass", "Description.")
    .def_static("method_name", &MyClass::MethodName,
        nb::arg("param"), "Method description.")
    .def_static("get_value", &MyClass::GetValue)
    .def_static("set_value", &MyClass::SetValue, nb::arg("value"));
```

命名约定：C++ PascalCase → Python snake_case（`GetFPS` → `get_fps`）。

## 枚举绑定

```cpp
nb::enum_<MyEnum>(m, "MyEnum", "Description.")
    .value("VALUE_A", MyEnum::VALUE_A)
    .value("VALUE_B", MyEnum::VALUE_B);
```

`enum` 和 `enum class` 语法相同。建议始终使用完全限定名避免宏冲突。

## 函数重载（lambda 消歧义）

```cpp
// C++: void SetCommandLine(const char* cmd);
//      void SetCommandLine(int argc, char** argv);

.def_static("set_command_line_str",
    [](const char* cmd) { MyClass::SetCommandLine(cmd); },
    nb::arg("cmd_line"))
```

## 只读静态属性（非内联 static const）

```cpp
// C++: static const int Camera;  // 在 .cpp 中定义

.def_prop_ro_static("Camera",
    [](nb::handle) { return Permission::Camera; },
    "Camera permission constant.")
```

## 返回策略

```cpp
// 返回引用（不转移所有权）
.def_static("get_singleton", &Logger::GetSingleton,
    nb::rv_policy::reference)

// 返回新对象（转移所有权）
.def_static("create", &Factory::Create,
    nb::rv_policy::take_ownership)
```

| 策略 | 含义 |
|------|------|
| `nb::rv_policy::automatic` | 默认，nanobind 自行判断 |
| `nb::rv_policy::reference` | 不转移所有权 |
| `nb::rv_policy::take_ownership` | Python 接管所有权 |
| `nb::rv_policy::copy` | 复制一份 |
| `nb::rv_policy::move` | 移动给 Python |

## printf 变参 → lambda 包装

```cpp
// C++: void Log(Severity s, const char* fmt, ...);

m.def("log_info", [](const std::string& msg) {
    Log(GLogLevel::Information, "%s", msg.c_str());
}, nb::arg("message"));
```

## `void*` → nb::capsule

```cpp
.def_static("get_window", []() {
    void* hwnd = MyClass::GetWindow();
    return nb::capsule(hwnd, "HWND");
})
```

## 默认参数

```cpp
.def_static("send_message",
    &MyClass::SendMessage,
    nb::arg("key"),
    nb::arg("value") = "")   // 默认值
```

## 允许 None 的参数

```cpp
.def_static("set_instance",
    &MyClass::SetInstance,
    nb::arg("instance").none())  // 接受 Python None → C++ nullptr
```
