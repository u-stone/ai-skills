---
name: cmake-library-architect
description: Guidelines for architecting professional C++ libraries with CMake. Use when creating new C++ libraries, refactoring projects into libraries, or setting up FetchContent/DLL exports.
---

# CMake Library Architect

This skill provides a standard procedure for building C++ libraries that are:
1.  **FetchContent-ready**: Easily consumable by other CMake projects.
2.  **Cross-platform**: Correctly handling Windows DLL exports (`__declspec`) and Linux/macOS visibility.
3.  **Modern**: Using `TARGET`-based CMake best practices.

## Workflow

### 1. Structure the Project
Adopt the standard directory layout. This is non-negotiable for `FetchContent` to work cleanly without path pollution.
See [directory_structure.md](references/directory_structure.md).

### 2. Define Export Macros
You MUST handle Windows symbol visibility explicitly.
1.  Create `include/<Project>/Export.h`.
2.  Use the template in [template_Export.h](references/template_Export.h).
3.  Apply `<PROJECT>_API` macros to all public classes and functions.

### 3. Configure CMake
Your `CMakeLists.txt` must handle aliases, include interfaces, and export definitions.
Use the template in [template_CMakeLists.txt](references/template_CMakeLists.txt).

**Critical Checklist:**
- [ ] `add_library(Name src/...)`
- [ ] `add_library(Name::Name ALIAS Name)` (Crucial for FetchContent consistency)
- [ ] `target_include_directories` with `BUILD_INTERFACE` and `INSTALL_INTERFACE`
- [ ] `generate_export_header` OR manual `DEFINE_SYMBOL` handling for Windows DLLs.
- [ ] `BUILD_SHARED_LIBS` support.

### 4. Implementation Details
- **Source Files**: In `.cpp` files, define the `<PROJECT>_EXPORTS` macro if not handled by CMake, or rely on CMake's `DEFINE_SYMBOL`.
- **Static Builds**: If building statically, ensure `template_Export.h` logic compiles to empty macros.

## Common Pitfalls
- **Missing API macro**: Causes linker errors (`LNK2019`) on Windows when building as DLL.
- **Incorrect Include Paths**: Consumers cannot find headers because `target_include_directories` was private or absolute paths were used without `BUILD_INTERFACE`.
- **Symbol Clashes**: Not namespacing headers (e.g., `include/MyLib.h` vs `include/MyProject/MyLib.h`). Always use the latter.