# C-Style API Wrappers for Interop

Even with PIMPL, C++ classes cannot be easily consumed by C, Python (ctypes), or C# (P/Invoke) due to name mangling and exception handling models.
**Solution**: Expose a C-style API using Opaque Pointers.

## 1. Define the Opaque Handle
In your public C header (`mylib_c.h`):

```c
#ifdef __cplusplus
extern "C" {
#endif

// Opaque handle (client never sees the struct definition)
typedef struct MyClass_T* MyClassHandle;

MYLIB_API MyClassHandle MyClass_Create();
MYLIB_API void MyClass_Destroy(MyClassHandle handle);
MYLIB_API void MyClass_DoSomething(MyClassHandle handle);

#ifdef __cplusplus
}
#endif
```

## 2. Implement the Wrapper (`mylib_c.cpp`)
Internally cast the handle back to your PIMPL class. **Always catch exceptions boundaries.**

```cpp
#include "mylib_c.h"
#include "MyClass.h"

MyClassHandle MyClass_Create() {
    try {
        return reinterpret_cast<MyClassHandle>(new MyClass());
    } catch (...) { return nullptr; }
}

void MyClass_Destroy(MyClassHandle handle) {
    if (handle) delete reinterpret_cast<MyClass*>(handle);
}

void MyClass_DoSomething(MyClassHandle handle) {
    auto* obj = reinterpret_cast<MyClass*>(handle);
    if (obj) {
        try {
            obj->DoSomething();
        } catch (...) { 
            // Log error or return error code
        }
    }
}
```
