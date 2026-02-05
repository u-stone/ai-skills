# C++ ABI Stability Checklist

## Do NOT do the following in public headers:

1.  **Expose Private Members**: Do not declare private member variables in the public class.
    *   *Risk*: Changing the size or layout of the class breaks ABI.
    *   *Fix*: Move all private members to the `Impl` struct.
2.  **Export STL Containers**: Do not use `std::vector`, `std::string`, or `std::shared_ptr` 
    as data members in DLL-exported classes (MSVC warning C4251).
    *   *Risk*: STL implementations vary between compiler versions and debug/release modes.
    *   *Fix*: Use raw pointers to `Impl` or abstract interfaces.
3.  **Change Virtual Table**: Do not add, remove, or reorder virtual functions.
    *   *Risk*: Offsets in the vtable are baked into client binaries.
    *   *Fix*: Append new virtual functions only at the end (risky) or use a new interface.
4.  **Inline Functions**: Be careful with inline functions that access internal state.
    *   *Risk*: Logic is compiled into the client application and won't update with the DLL.
5.  **Default Arguments**: Do not change default argument values.
    *   *Risk*: Values are substituted at compile time in the client.

## Safe Changes (PIMPL)

If using PIMPL correctly, you CAN safe do the following in the `.cpp` file:
1.  Add/remove private member variables (in `Impl`).
2.  Add/remove private member functions (in `Impl`).
3.  Modify the implementation of existing public functions.
