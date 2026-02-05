# Fast PIMPL (Inline PIMPL)

Standard PIMPL incurs a heap allocation (`new Impl`) and pointer indirection. For performance-critical classes, use "Fast PIMPL" to store the implementation directly in the object's layout while still hiding details.

## Implementation Pattern

### 1. Header (`FastClass.h`)
Reserve a fixed buffer of bytes. **Warning**: Changing the size breaks ABI.

```cpp
#include <type_traits>

class MYLIB_API FastClass {
public:
    FastClass();
    ~FastClass();
    void Action();

private:
    // Reserve 64 bytes. Adjust based on expected implementation size.
    // Alignment is critical.
    static constexpr size_t kImplSize = 64;
    static constexpr size_t kImplAlign = 8;
    
    std::aligned_storage<kImplSize, kImplAlign>::type m_storage;
};
```

### 2. Implementation (`FastClass.cpp`)
Use Placement New to construct the Impl inside the buffer.

```cpp
#include "FastClass.h"
#include <new>

struct FastClassImpl {
    int data[10]; // Must fit in kImplSize!
    void DoWork() { /*...*/ }
};

// Static assertion to ensure buffer is large enough (compile-time check)
static_assert(sizeof(FastClassImpl) <= sizeof(FastClass::m_storage), "Impl too big!");
static_assert(alignof(FastClassImpl) <= alignof(FastClass::m_storage), "Impl alignment mismatch!");

FastClass::FastClass() {
    new (&m_storage) FastClassImpl(); // Placement New
}

FastClass::~FastClass() {
    reinterpret_cast<FastClassImpl*>(&m_storage)->~FastClassImpl(); // Explicit Destructor
}

void FastClass::Action() {
    auto* impl = reinterpret_cast<FastClassImpl*>(&m_storage);
    impl->DoWork();
}
```
