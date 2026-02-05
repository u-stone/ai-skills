# Singleton Patterns & Pitfalls

## 1. Thread Safety & DCLP
Double-Checked Locking Pattern (DCLP) without `std::atomic` is broken due to instruction reordering.
The CPU might assign memory to the pointer before the constructor finishes.
**Solution**: Use `std::atomic<T*>` with `acquire-release` semantics.

## 2. Static Initialization Order Fiasco
Global static objects (like `std::mutex`) in different compilation units have undefined 
initialization order. Accessing an uninitialized mutex during singleton creation causes crashes.
**Solution**: "Construct on First Use" - use a function-local static mutex.

## 3. Windows DLLs & Loader Lock
On Windows, `DllMain` (PROCESS_DETACH) runs under a "Loader Lock". Joining threads or 
performing complex cleanup during this phase causes deadlocks.
**Solution**: 
- **Leaky Singleton**: Don't destroy the singleton at process exit (let OS reclaim memory).
- **Explicit Destroy**: Provide a `Destroy()` method to be called manually before `main` exits.

## 4. ABI Stability (PIMPL)
In exported headers (DLLs), use raw pointers for PIMPL to avoid MSVC C4251 warnings caused by 
private smart pointer members. Handle the raw pointer's lifecycle in the constructor/destructor.
