---
name: cpp-abi-stable-pimpl
description: Guide for implementing the PIMPL (Pointer to Implementation) idiom in C++ to ensure ABI stability and reduce compilation dependencies. Use when designing shared libraries (DLLs) or public APIs.
---

# PIMPL Implementation Guide

The PIMPL idiom moves all private implementation details into a hidden struct/class, 
exposing only an opaque pointer in the public header. This ensures ABI stability 
and speeds up compilation.

## The Gold Standard Template

### 1. Public Header (`MyClass.h`)
**Key Rule**: No private data members except the implementation pointer.

```cpp
#pragma once
#include <memory>
#include "Export.h" // Your export macros

class MYLIB_API MyClass {
public:
    MyClass();
    ~MyClass(); // Must be defined in .cpp to see Impl's destructor

    // Copy Semantics (Deep Copy)
    MyClass(const MyClass& other);
    MyClass& operator=(const MyClass& other);

    // Move Semantics (Transfer Ownership)
    MyClass(MyClass&& other) noexcept;
    MyClass& operator=(MyClass&& other) noexcept;

    void DoSomething();

private:
    struct Impl; // Forward declaration
    Impl* m_impl; // Raw pointer preferred for DLL boundary safety (vs std::unique_ptr)
    // NOTE: std::unique_ptr<Impl> triggers C4251 warning on MSVC if exported.
    // Using raw pointer + manual management in ctor/dtor is the most portable/safe method for DLLs.
};
```

### 2. Implementation File (`MyClass.cpp`)
**Key Rule**: All logic and state live here.

```cpp
#include "MyClass.h"
#include <iostream>
#include <string>

// Definition of the hidden implementation
struct MyClass::Impl {
    std::string internalState;
    
    void InternalHelper() {
        // ...
    }
};

// --- Lifecycle Management ---

MyClass::MyClass() : m_impl(new Impl()) {}

MyClass::~MyClass() {
    if (m_impl) {
        delete m_impl;
        m_impl = nullptr;
    }
}

// Deep Copy
MyClass::MyClass(const MyClass& other) : m_impl(new Impl(*other.m_impl)) {}

MyClass& MyClass::operator=(const MyClass& other) {
    if (this != &other) {
        *m_impl = *other.m_impl;
    }
    return *this;
}

// Move (Transfer ownership)
MyClass::MyClass(MyClass&& other) noexcept : m_impl(other.m_impl) {
    other.m_impl = nullptr;
}

MyClass& MyClass::operator=(MyClass&& other) noexcept {
    if (this != &other) {
        delete m_impl;
        m_impl = other.m_impl;
        other.m_impl = nullptr;
    }
    return *this;
}

// --- Public API ---

void MyClass::DoSomething() {
    m_impl->internalState = "Active";
    m_impl->InternalHelper();
}
```

## Advanced Strategies
Depending on your specific needs (performance vs. compatibility), consult these guides:

*   **[Forward Compatibility](references/forward_compat.md)**: How to plan for future API changes.
*   **[C-Style Interop](references/c_wrapper.md)**: Exposing your class to C, Python, or C#.
*   **[Fast PIMPL](references/fast_pimpl.md)**: Zero-overhead stack-allocated PIMPL.
*   **[Modern Smart Pointers](references/smart_pimpl.md)**: Using `unique_ptr` safely in DLLs.

## Checklist
- [ ] Forward declare `struct Impl` in the header.
- [ ] Use a raw pointer (`Impl*`) for the member to avoid MSVC C4251.
- [ ] Define the destructor in the `.cpp` file (where `Impl` is defined).
- [ ] Implement Copy/Move constructors manually (cannot use `= default`).
- [ ] Ensure no other private members exist in the header.

## References
- [ABI Checklist](references/abi_checklist.md): What breaks ABI?
- [Export Macros](references/export_macro.md): Cross-platform visibility.
