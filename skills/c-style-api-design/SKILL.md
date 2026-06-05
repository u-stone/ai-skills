---
name: c-style-api-design
description: >
  设计或审查 C/C++ API 时，确保 API 能被 Lua、Python（nanobind/pybind11/Cython/ctypes）、
  JavaScript（Emscripten/Node-FFI）、C#（P/Invoke）等脚本语言无歧义地封装。
  当用户提到 "C API 设计"、"封装给 Lua/Python/脚本"、"C ABI 边界"、"extern C 导出"、
  "跨语言 API"、"脚本绑定友好的 C API"、"设计 C API 给脚本用"、"opaque handle"、
  "callback 跨语言"、"避免 ABI 问题" 时使用。
license: MIT
compatibility: opencode
metadata:
  audience: native-sdk-engineers
  workflow: cross-language-c-api-design
  source: skills/c-style-api-design/SKILL.md
  modes:
    - design
    - review
    - interop-planning
---

# Skill: 面向脚本语言绑定的 C-Style API 设计

## 使用边界

本 Skill 关注**面向脚本语言绑定的 C 风格 API 形状设计**。

优先用于：

- 设计可被 Lua/Python/C#/JavaScript 稳定封装的 C ABI；
- 审查现有 C/C++ API 是否存在脚本绑定死角；
- 规划 opaque handle、error code、callback、buffer、string、versioning 等跨语言边界；
- 在真正写 nanobind/pybind11/Cython/P/Invoke/FFI 绑定前，先把 ABI 设计干净。

不要把它当作主要 Skill 用于：

- 通用 C++17 SDK 实现规范或更广泛的 ABI/导出/CMake 设计；
- 直接生成 Python 轮子、editable install、stub、打包与分发流程；
- repository-wide 的工程流程或项目运行规则。

边界建议：

- `cpp-game-sdk-coding-standard`：更广泛的 C++17 SDK / native library / CMake / public ABI 标准；
- `cpp-python-bindings`：在 C ABI 已经设计清楚后，继续做 Python 绑定、包布局与 wheel 交付；
- 本 Skill：聚焦“先把跨语言可封装的 C API 设计对”。

## 0. 核心问题

C++ 的很多特性（重载、模板、异常、`std::function`、`std::string`、继承）无法直接跨语言传递。如果 API 不预先设计为 C ABI，后期绑定到 Lua/Python/C# 时会遇到语义无法转换的死角。

**本 Skill 的目标**：设计「一次导出，多语言封装」的 C API 层。

---

## 1. 数据类型选择

### 1.1 可以直接跨语言传递的类型

| 类型 | 说明 |
|------|------|
| `int32_t`, `uint32_t`, `int64_t`, `uint64_t` | 定长整数，所有语言都能精确映射 |
| `float`, `double` | 浮点数 |
| `const char*` | 以 null 结尾的 UTF-8 字符串 |
| `uint8_t*` + `size_t` | 二进制 buffer（不要用 `void*` 裸指针） |
| 不透明指针 `struct Handle_t*` (typedef to `Handle`) | 对象句柄，跨边界只传指针不访存 |
| `bool` | C99 `_Bool`（但要注意各语言 `bool` 大小不同，建议用 `int`） |

### 1.2 需要包装的类型

| C++ 类型 | 问题 | 替代方案 |
|---------|------|---------|
| `std::string` | ABI 不稳定，各编译器布局不同 | `const char*` + `size_t`，或 opaque string handle |
| `std::vector<T>` | STL 布局不可跨语言 | `const T*` + `size_t` |
| `std::function<>` | 无法跨 FFI 传递 | C 函数指针 + `void* context` |
| `std::shared_ptr<T>` / `std::unique_ptr<T>` | C ABI 无智能指针语义 | 显式 `create`/`destroy` + 引用计数（如需要） |
| 异常 | 跨语言边界未定义 | 返回错误码，或通过回调传递错误 |
| C++ 类（含 vtable） | 布局依赖编译器 | Opaque handle + C 函数操作 |

### 1.3 绝对不能暴露给脚本语言的类型

- 模板实例化类型（编译器特定符号）
- `std::function`、lambda、任何闭包
- C++ 异常（跨 `extern "C"` 边界是 UB）
- 任何 C++ 标准库容器（`std::vector`、`std::map` 等）
- 带虚函数的类（vtable 布局 ABI 不稳定）
- 非 POD 的 struct/class

---

## 2. Opaque Handle 模式

### 2.1 原则

所有 C++ 对象通过**不透明指针**暴露给脚本语言。脚本语言只持有指针，所有操作通过 C 函数完成。

```c
// my_api.h
#ifdef __cplusplus
extern "C" {
#endif

typedef struct MyEngine_t MyEngine;    // 不透明——外部永远不解引用

MyEngine*    my_engine_create(const char* config_path);
void         my_engine_destroy(MyEngine* engine);
int          my_engine_tick(MyEngine* engine, float dt);

// 获取属性的 getter——永远不暴露内部字段
int          my_engine_get_fps(const MyEngine* engine);
const char*  my_engine_get_app_name(const MyEngine* engine);

#ifdef __cplusplus
}
#endif
```

```c
// my_api.cpp —— 内部实现
#include "my_api.h"
#include "Engine.hpp"   // 真实的 C++ 类

struct MyEngine_t {
    Engine* impl;        // 真正的 C++ 对象
};

MyEngine* my_engine_create(const char* config_path) {
    auto* h = new MyEngine_t;
    h->impl = new Engine(config_path);
    return h;
}

void my_engine_destroy(MyEngine* engine) {
    delete engine->impl;
    delete engine;
}
```

### 2.2 Handle 的命名约定

- Opaque struct：`<Prefix>_t`（如 `GWEngine_t`）
- Create：`<prefix>_create` 或 `<prefix>_open`
- Destroy：`<prefix>_destroy` 或 `<prefix>_close`

### 2.3 多个 Handle 类型

如果库有多个核心对象，每种一个 handle：

```c
typedef struct GWEngine_t GWEngine;
typedef struct GWScene_t  GWScene;
typedef struct GWCamera_t GWCamera;

GWEngine* gw_engine_create(const char* config);
GWScene*  gw_scene_create(GWEngine* engine, const char* name);
GWCamera* gw_scene_get_camera(GWScene* scene, int index);
```

---

## 3. 错误处理

### 3.1 推荐方案：返回错误码 + last-error 查询

```c
// 方式 A：返回值 = 错误码（0 = 成功）
int my_engine_load_scene(MyEngine* engine, const char* path);

// 获取最后一次错误的详细信息
const char* my_engine_get_last_error(MyEngine* engine);
int         my_engine_get_last_error_code(MyEngine* engine);
```

```python
# Python 封装
def load_scene(engine, path):
    if engine.load_scene(path) != 0:
        raise RuntimeError(engine.get_last_error())
```

### 3.2 备选方案：输出参数

```c
// 方式 B：输出参数传错误信息（适合无状态库）
int my_engine_load_scene(MyEngine* engine, const char* path,
                         const char** out_error_msg);
```

### 3.3 不推荐的方案

| 方案 | 问题 |
|------|------|
| 跨 `extern "C"` 抛 C++ 异常 | 未定义行为，各编译器行为不同 |
| 通过 `errno` 传错误 | 线程不安全，且各平台 `errno` 值不同 |
| 返回 `std::string` 错误信息 | ABI 不稳定 |

---

## 4. 回调设计

### 4.1 问题

C++ 的 `std::function`、lambda、成员函数指针都无法跨 FFI 传递。

### 4.2 正确方案：C 函数指针 + `void* context`

```c
// C API —— 声明
typedef void (*LogCallback)(const char* message, int severity, void* context);

void my_engine_set_log_callback(MyEngine* engine,
                                 LogCallback callback,
                                 void* context);
```

```python
# Python —— 通过 nanobind/pybind11 封装
def _log_callback(message: str, severity: int, ctx: int) -> None:
    print(f"[{severity}] {message}")

# ctx 可以是 Python 对象 ID，或 capsule 封装的任意数据
engine.set_log_callback(_log_callback, ctx)
```

### 4.3 context 指针的设计原则

- `void* context` 是**透传数据**——C 层不取值、不释放、不访问
- 脚本侧通过 `context` 保持 Python/JS/Lua 对象存活，防止 GC
- 调用约定：回调执行时 C 层把 `context` 原样传回

### 4.4 生命周期保证

```c
// 注册回调时返回 token，方便注销
int my_engine_set_log_callback(MyEngine* engine,
                                LogCallback callback,
                                void* context);
void my_engine_remove_log_callback(MyEngine* engine, int token);
```

注销是为了让脚本侧释放 `context` 关联的资源。

---

## 5. 数组和 Buffer 传递

### 5.1 输入：指针 + 长度

```c
// 传递二进制数据（不要用 void*，用 uint8_t* 明确字节语义）
int my_engine_load_buffer(MyEngine* engine,
                           const uint8_t* data,
                           size_t size);

// 传递结构体数组
int my_engine_set_vertices(MyEngine* engine,
                            const Vertex* vertices,
                            size_t count);
```

### 5.2 输出：预分配 + 写入长度

```c
// 方式 A：调用者分配，被调者写入
int my_engine_get_logs(MyEngine* engine,
                        char* buffer,
                        size_t buffer_size,
                        size_t* out_written);
```

```c
// 方式 B：先查询大小，再获取数据
int my_engine_get_logs_size(MyEngine* engine, size_t* out_size);
int my_engine_get_logs(MyEngine* engine, char* buffer, size_t buffer_size);
```

### 5.3 不推荐

- 返回 `std::vector` 或分配的 buffer 让调用者释放（跨堆释放）
- 用 `void*` 无长度信息传递二进制数据

---

## 6. 字符串处理

### 6.1 输入

- 始终接受 `const char*`（UTF-8 编码）
- 如果字符串可能包含 `\0`，同时传 `const char*` + `size_t`

### 6.2 输出

```c
// 方式 A：调用者提供 buffer
int my_engine_get_app_name(MyEngine* engine,
                            char* buffer,
                            size_t buffer_size);

// 方式 B：返回内部指针（只读，生命周期跟随 engine）
const char* my_engine_get_app_name(const MyEngine* engine);
```

**规则**：
- 方案 B 的返回指针只在 engine 存活（或下次同一 API 调用前）有效
- 方案 A 需要 `buffer_size` 参数防止溢出

### 6.3 不推荐

- 返回 `std::string`
- 通过 `char**` 分配内存让调用者 `free`（跨堆 `free` 是 UB）

---

## 7. 版本兼容性

### 7.1 结构体字段预留

```c
// 对外暴露的配置结构体 —— 加 version/size 字段
typedef struct {
    size_t struct_size;      // sizeof(GWEngineConfig) —— 调用者填入
    int width;
    int height;
    int max_fps;
    const char* title;
    // 未来扩展加在这里，旧调用者不受影响
} GWEngineConfig;

int my_engine_create_with_config(GWEngineConfig* config);
```

```cpp
// 内部实现 —— 根据 struct_size 判断版本
int my_engine_create_with_config(GWEngineConfig* config) {
    int max_fps = 60;  // 默认值
    if (config->struct_size >= offsetof(GWEngineConfig, max_fps) + sizeof(int))
        max_fps = config->max_fps;
    // ...
}
```

### 7.2 API 版本查询

```c
// 查询 API 版本号
int my_engine_get_api_version(void);  // 返回 MAJOR*10000 + MINOR*100 + PATCH
```

---

## 8. 线程安全

### 8.1 原则

C API 中的每个函数必须在文档中明确：

- **thread-safe**：可从任意线程调用（内部有互斥锁或线程局部存储）
- **not thread-safe**：必须在主线程调用
- **reentrant**：可从信号处理器调用（通常只有纯计算函数能承诺此条）

### 8.2 设计建议

- 初始化/反初始化不假设线程安全（`create`/`destroy` 在主线程调用）
- 查询类函数（getter）尽量 thread-safe
- 如果无法保证 thread-safe，在 API 名字中显式标注：`my_engine_tick_main_thread_only`

---

## 9. 初始化与生命周期

### 9.1 推荐模式

```c
// 1) 查询版本（无需初始化）
int my_engine_get_api_version(void);

// 2) 创建实例
MyEngine* my_engine_create(const char* config_path);

// 3) 使用实例
int my_engine_load_scene(MyEngine* engine, const char* path);
int my_engine_tick(MyEngine* engine, float dt);

// 4) 销毁实例
void my_engine_destroy(MyEngine* engine);
```

### 9.2 避免

- 隐式全局初始化（`MyEngine* e = my_engine_get_instance()`）
- `atexit` 注册清理函数（跨 DLL 边界的 `atexit` 行为不可移植）
- 假设只有单实例（如果需要单实例，让调用者显式传递相同的 handle）

---

## 10. 跨语言边界检查清单

每个 C API 函数在提交前检查：

```
类型安全
[ ] 所有参数和返回值都是 §1.1 中列出的 C 类型
[ ] 不传递 std::string、std::vector、std::function
[ ] 不暴露 C++ 异常跨 extern "C" 边界
[ ] 不返回内部成员的 non-const 指针（破坏封装和不透明性）

错误处理
[ ] 所有可能失败的函数返回错误码或使用 last-error 机制
[ ] last-error 与实例关联（线程安全：每 engine 实例一个 last-error）
[ ] 不依赖 errno 跨语言传递错误

回调
[ ] 所有回调使用 C 函数指针 + void* context 模式
[ ] context 在 C 层被透传，不取值、不释放
[ ] 提供注销回调的机制

内存
[ ] 调用者分配 buffer 的接口带 size 参数
[ ] 不要求跨堆 free（C 层分配的内存由 C 层释放）
[ ] 返回的内部指针明确声明有效期

版本
[ ] 对外 struct 包含 struct_size 字段
[ ] 提供 get_api_version 函数

线程
[ ] 文档标记每个函数的线程安全性
[ ] 初始化/销毁不假设隐式锁

命名
[ ] 所有公共符号带统一前缀（如 gw_）
[ ] create/open 对应 destroy/close，成对出现
[ ] 用 _t 后缀标记 opaque handle typedef
```

---

## 11. 与 `cpp-python-bindings` 技能的对接

本 Skill 设计的 C API 是 `cpp-python-bindings` 所描述流程的**上游输入**。流程为：

```
C++ 引擎内部
    │
    ▼  用本 Skill 的设计原则
设计薄 C ABI 适配层
    │
    ▼  用 cpp-python-bindings Skill 的流程
nanobind/pybind11 绑定 C API → Python package → wheel
```

C ABI 层越干净，Python（和 Lua/C#/JS）绑定就越简单。

---

## 12. 参考文件

| 文件 | 内容 |
|------|------|
| `references/c-api-examples.h` | 完整的 C API 头文件示例（含 handle / callback / array / error） |
| `references/per-language-guidance.md` | 各语言（Lua/Python/C#/JS）对 C API 的特殊要求和封装模式 |
