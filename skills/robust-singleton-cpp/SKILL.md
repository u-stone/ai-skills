---
name: robust-singleton-cpp
description: Guidelines for implementing thread-safe, DLL-safe, and initialization-safe Singletons in C++11+. Use when designing shared libraries, DLLs, or core system centers that require a single global instance with strict lifecycle management.
---

# Robust Singleton Implementation Guide

Follow this "Gold Standard" implementation to avoid thread-safety issues, static 
initialization order crashes, and Windows Loader Lock deadlocks.

## The Gold Standard Template

### Header (.h)
```cpp
class MyCenter {
public:
    static MyCenter& Instance();
    static void Destroy(); // Essential for Windows DLL safety

    MyCenter(const MyCenter&) = delete;
    MyCenter& operator=(const MyCenter&) = delete;

private:
    MyCenter();
    ~MyCenter();

    struct Impl; // PIMPL for ABI stability
    Impl* m_impl;
};
```

### Implementation (.cpp)
```cpp
#include <atomic>
#include <mutex>

namespace {
    static std::atomic<MyCenter*> g_instance{nullptr};
    
    // Prevents Static Initialization Order Fiasco
    std::mutex& GetCreationMutex() {
        static std::mutex m;
        return m;
    }
}

MyCenter& MyCenter::Instance() {
    // 1. Double-checked locking with acquire-release semantics
    MyCenter* tmp = g_instance.load(std::memory_order_acquire);
    if (tmp == nullptr) {
        std::lock_guard<std::mutex> lock(GetCreationMutex());
        tmp = g_instance.load(std::memory_order_relaxed);
        if (tmp == nullptr) {
            tmp = new MyCenter();
            g_instance.store(tmp, std::memory_order_release);
        }
    }
    return *tmp;
}

void MyCenter::Destroy() {
    std::lock_guard<std::mutex> lock(GetCreationMutex());
    MyCenter* tmp = g_instance.load(std::memory_order_relaxed);
    if (tmp) {
        delete tmp; // Triggers destructor (e.g., stops worker threads)
        g_instance.store(nullptr, std::memory_order_release);
    }
}
```

## Key Rules

1. **Explicit Destruction**: Always provide a `Destroy()` method if the singleton owns threads. 
   Joining threads in a static destructor during DLL unload causes deadlocks.
2. **Atomic Pointers**: Use `std::atomic` for the instance pointer to prevent reordering.
3. **Local Static Mutex**: Never use a global `static std::mutex`. Use a function-local 
   static to ensure it's initialized on first use.
4. **Line Limit**: Keep all code lines under 100 characters.

## Technical Details
See [references/patterns.md](references/patterns.md) for deep dives into DCLP and Windows safety.