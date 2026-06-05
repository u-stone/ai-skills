# C/C++ 绑定限制与应对

不同 C++ 模式对 nanobind/pybind11 的支持程度不同。本文档列出常见限制及推荐解决方案。

## 对照表

| C/C++ 模式 | 支持 | 应对 |
|-----------|------|------|
| 静态成员函数、枚举、构造函数 | ✅ 直接 | `def_static` / `nb::enum_` / `nb::init<>` |
| STL 容器 (`vector`, `map`, `string`) | ⚠️ 需显式 `#include` | `#include <nanobind/stl/vector.h>` 等 |
| 函数重载 | ⚠️ 需消歧义 | Lambda 包装 / `static_cast` |
| 原始函数指针（C 回调） | ⚠️ 需适配器 | `nb::capsule` / 全局 `std::function` |
| `void*` 不透明指针 | ⚠️ 需 capsule | `nb::capsule(ptr, "name")` |
| 非内联静态常量 | ⚠️ 需 lambda getter | `def_prop_ro_static("x", [](nb::handle){ return X; })` |
| printf 变参 | ❌ 需包装 | Lambda 接受 `std::string` |
| 模板类 | ❌ 需显式实例化 | `nb::class_<MyClass<int>>` |
| private/protected 成员 | ❌ 无法访问 | 仅通过 public 接口 |
| 条件编译 (`#ifdef`) | ❌ 需镜像守卫 | 绑定代码中也加 `#ifdef` |
| `#define` 宏冲突 (win32 `ERROR`) | — | `#undef` + 完全限定名 |
| Debug/Release CRT 混用 | — | 统一构建配置 |

## 各模式详解

### 1. 函数重载

```cpp
// C++: 两个重载
static void SetCommandLine(const char* cmdLine);
static void SetCommandLine(int argc, char** argv);
```

修复：lambda 消歧义

```cpp
.def_static("set_command_line_str",
    [](const char* cmd) { AppInfo::SetCommandLine(cmd); },
    nb::arg("command_line"))
```

### 2. 原始函数指针

```cpp
typedef void (*GRIT_NATIVE_MESSAGE_CALLBACK)(std::string, std::string);
static void SetReceiveEngineMessageCallback(GRIT_NATIVE_MESSAGE_CALLBACK callback);
```

修复：全局 `std::function` + lambda + `nb::capsule`（Phase 2 实现）

### 3. `void*` 指针

```cpp
static void* GetWindow();
```

修复：`nb::capsule(ptr, "HWND")` 或跳过不绑定

### 4. printf 变参

```cpp
void Log(GLogLevel severity, const char* formatString, ...);
```

修复：lambda 包装为 `std::string`

```cpp
m.def("log_info", [](const std::string& msg) {
    Log(GLogLevel::Information, "%s", msg.c_str());
});
```

### 5. `windows.h` 宏冲突

`#define ERROR 0` 破坏 `enum Error { OK, FAILED, ... }`。

修复：
```cpp
#ifdef ERROR
#  undef ERROR
#endif
nb::enum_<gw::platform::Error>(m, "Error", ...)
```

### 6. 非内联静态常量

```cpp
class Permission {
    static const int Camera;  // 在 .cpp 中定义
};
```

修复：`def_prop_ro_static` lambda getter（不用 `def_ro_static` 取址）

### 7. Debug/Release CRT 混用

Debug 引擎 DLL + Release .pyd → 堆损坏（随机 crash）。

修复：`-Ccmake.define.CMAKE_BUILD_TYPE=Debug` 匹配引擎配置

### 8. 条件编译

```cpp
#if defined(GW_ENABLE_IMGUI)
    static bool GetEnableImGui();
#endif
```

修复：绑定代码中镜像守卫 `#if defined(GW_ENABLE_IMGUI)`

### 9. 模板类

```cpp
template <typename T> class RingBufferT { ... };
```

修复：显式实例化 `nb::class_<RingBufferT<int>>`

### 10. STL 容器

nanobind 需要显式包含对应头文件才能转换：

| C++ 类型 | nanobind 头文件 |
|---------|----------------|
| `std::string` | `#include <nanobind/stl/string.h>` |
| `std::vector<T>` | `#include <nanobind/stl/vector.h>` |
| `std::map<K,V>` | `#include <nanobind/stl/map.h>` |
| `std::pair<A,B>` | `#include <nanobind/stl/pair.h>` |
| `std::optional<T>` | `#include <nanobind/stl/optional.h>` |

### 11. 非所有权引用

```cpp
static Logger& GetSingleton();  // 返回引用，不转移所有权
```

修复：`.def_static("get_singleton", &GetSingleton, nb::rv_policy::reference)`
