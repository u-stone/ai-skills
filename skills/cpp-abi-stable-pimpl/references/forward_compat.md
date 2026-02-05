# Forward Compatibility Strategies

To ensure your library can evolve without breaking older clients, adopt these strategies alongside PIMPL.

## 1. Reserved Virtual Slots
If your class exposes a virtual interface (pure abstract class), future additions to the vtable will break binary compatibility.
**Strategy**: Pre-allocate "reserved" virtual slots.

```cpp
class IInterface {
public:
    virtual void MethodA() = 0;
    
    // Reserved slots for future expansion
    virtual void _Reserved1() {}
    virtual void _Reserved2() {}
    virtual void _Reserved3() {}
};
```
*Note*: When you need to add `MethodB`, replace `_Reserved1` with it. Clients compiled against the old header will still have valid offsets.

## 2. Versioned Structs
For configuration structs passed to your API, include a size/version field.

```cpp
struct ConfigOptions {
    uint32_t structSize; // Set to sizeof(ConfigOptions)
    int optionA;
    // ...
};
```
*   **In your library**: Check `structSize` to determine which fields are valid.
*   **Expansion**: You can add `int optionB` at the end. Old clients send a smaller size; your library handles defaults.
