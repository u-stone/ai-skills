# Modern Smart Pointers in PIMPL

While raw pointers are the "safest" for ABI, `std::unique_ptr` is preferred for modern 
C++ resource safety. Here is how to use it without MSVC C4251 warnings.

## 1. The Custom Deleter Pattern
MSVC C4251 occurs because the default deleter of `std::unique_ptr` is part of the 
class definition. Using a custom (non-inline) deleter moves the logic to the `.cpp`.

```cpp
// Header
class MYLIB_API MyClass {
public:
    MyClass();
    ~MyClass();
private:
    struct Impl;
    struct ImplDeleter { void operator()(Impl* p); };
    std::unique_ptr<Impl, ImplDeleter> m_impl;
};

// Implementation (.cpp)
struct MyClass::Impl { /*...*/ };
void MyClass::ImplDeleter::operator()(Impl* p) { delete p; }

MyClass::MyClass() : m_impl(new Impl()) {}
```

## 2. The Suppression Pattern
If you are certain the library and client use the same CRT/Compiler, you can simply 
suppress the warning.

```cpp
#pragma warning(push)
#pragma warning(disable: 4251)
    std::unique_ptr<Impl> m_impl;
#pragma warning(pop)
```

## 3. Comparison
| Method | Safety | Complexity | Recommended For |
| :--- | :--- | :--- | :--- |
| **Raw Pointer** | Highest (ABI) | High (Manual) | Public SDKs, Generic Plugins |
| **Custom Deleter** | High | Medium | Internal Corporate Libraries |
| **Suppression** | Low | Low | Monolithic Projects (Same Compiler) |
