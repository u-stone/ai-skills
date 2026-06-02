# C++ Game SDK Coding Standard Reference

## Purpose and Scope

This reference defines portable rules for C++17 game SDK, middleware, native plugin, and engine-adjacent library work. It assumes CMake as the build system and cross-platform support across Windows, macOS, Linux, Android, and iOS unless the user narrows the target.

The standard prioritizes, in order:

1. correctness;
2. maintainability;
3. testability;
4. cross-platform compatibility;
5. clear ownership and resource lifetime;
6. stable SDK boundaries;
7. reasonable runtime performance;
8. clean CMake integration;
9. static and shared library support;
10. LLVM C++ Style-based naming and formatting.

Generated code must be practical engineering code, not pseudo-code.

## Constraint Precedence

Apply rules in this order:

1. direct user instruction;
2. safety, correctness, and non-fabrication rules;
3. repository-local instruction files;
4. active project config files such as `.clang-format`, `.editorconfig`, and `.gitattributes`;
5. this skill's portable defaults;
6. archived or historical documents.

If repository-local GAP rules conflict with this portable standard, GAP-local rules win inside this repository.

## Required Initial Clarification

Before generating C++ code, project layout, CMake configuration, SDK API, or refactoring suggestions, identify the target development mode:

1. **Business development** - iteration speed, readability, maintainability, feature stability.
2. **System programming** - OS APIs, threads, files, sockets, memory mapping, processes, plugins, dynamic libraries, ABI, resource lifetime.
3. **High-performance development** - CPU cache, memory layout, SIMD, branch prediction, allocation reduction, lock contention, frame-time stability.
4. **Low-level library / SDK** - ABI stability, C-style exported APIs, symbol visibility, dependency isolation, installation, packaging, binary compatibility.

If unspecified, default to game business development plus SDK-ready cross-platform design.

## Mode-Specific Rules

### Business Development

Use for gameplay systems, editor tools, resource pipeline tools, scripting integration, configuration systems, and game service integration.

- Prioritize readability and maintainability.
- Prefer simple, direct code.
- Avoid premature optimization.
- Use standard library facilities where appropriate.
- Keep gameplay logic isolated from platform-specific details.
- Make code easy to test.
- Use `std::shared_ptr` only for true shared ownership.

Avoid raw `new` / `delete`, mutable global state, macro-driven business logic, overly clever templates, deep inheritance hierarchies, and hidden platform dependencies.

### System Programming

Use for file systems, sockets, threading, dynamic library loading, memory mapping, native handles, IPC, platform abstraction layers, and runtime services.

- Describe Windows, macOS, Linux, Android, and iOS differences when relevant.
- Wrap native resources with RAII.
- Never leak OS handles.
- Never ignore system API errors.
- Do not expose platform-specific handles through public SDK APIs unless explicitly required.
- Keep platform-specific code behind narrow abstraction layers.
- Avoid throwing exceptions across shared library boundaries.

### High-Performance Development

Use for engine runtime systems, rendering, animation, physics, audio, networking, ECS, job systems, memory allocators, and resource streaming.

- Avoid heap allocation in hot paths.
- Avoid unnecessary virtual calls in hot paths.
- Avoid false sharing.
- Prefer cache-friendly data layouts and batching.
- Avoid lock contention and unbounded queues.
- Avoid unnecessary string formatting and expensive logging during frame update.
- Justify complex optimization with profiling data or clear performance targets.

For non-trivial algorithms, state time complexity, space complexity, allocation behavior, hot-path suitability, and thread-safety assumptions.

### Low-Level Library / SDK

Use for SDKs, shared libraries, static libraries, native plugins, middleware, and libraries distributed to external teams.

- All exported functions must use C-style ABI.
- Public exported functions must be declared with `extern "C"`.
- Public exported functions must use explicit export macros.
- Public SDK ABI must not expose C++ classes, STL containers, exceptions, templates, references, or overloaded functions.
- Internal implementation may use modern C++17.
- Public headers must be stable and minimal.
- Public API must explicitly document ownership, lifetime, threading, error handling, and versioning.
- Memory allocated inside the SDK must be released by the SDK.
- Provide install rules and CMake package export rules.
- Support both static and shared libraries when distribution requires it.

## C++ and Compiler Defaults

- Default language: C++17.
- Default CMake minimum: CMake 3.24 for portable new SDKs, unless the repository requires a lower version.
- Recommended compiler baselines: GCC 9+, Clang 10+, AppleClang 12+, MSVC 19.28+, Android NDK Clang r23+.
- Set `CMAKE_CXX_STANDARD 17`, `CMAKE_CXX_STANDARD_REQUIRED ON`, and `CMAKE_CXX_EXTENSIONS OFF` or use `target_compile_features(... cxx_std_17)`.
- Avoid compiler-specific extensions unless guarded by feature checks.

## Naming Rules

- Files: lowercase with underscores, for example `asset_manager.h` and `asset_manager.cc`.
- Types: `PascalCase`, for example `AssetManager`, `TextureDesc`, `TextureFormat`.
- Internal C++ functions: `PascalCase` in this standard.
- Exported C functions: lower snake case with SDK prefix, for example `game_sdk_create`.
- Class members: trailing underscore.
- Portable default variables: lower snake case. When a project has a stronger local convention, follow it.
- Constants: `k` + PascalCase for internal C++, SDK-prefixed uppercase for C ABI constants.
- Namespaces: lowercase internal namespaces; no namespaces in exported C ABI.
- Macros: uppercase snake case, minimized.
- Never use `using namespace` in public headers.

## Formatting Rules

Use the project `.clang-format`. If none exists, use the bundled config in `references/config/.clang-format` as a starting point.

Portable defaults:

- no tabs;
- column limit 100;
- LLVM style base where no local style exists;
- braces for control statements;
- early returns over deep nesting;
- clean and minimal public headers.
- Doxygen-style comments for exported public header declarations.

## Public SDK API Rules

All public exported SDK functions must use C ABI.

Required public API characteristics:

- opaque handles for SDK objects;
- fixed-width integer types;
- versionable POD structs with `struct_size` and version fields when practical;
- explicit result codes;
- explicit ownership and lifetime documentation;
- explicit thread-safety documentation;
- no C++ references, STL containers, exceptions, overloads, templates, or unstable compiler-specific ABI.

### Public Header Documentation

Public header files must use Doxygen-style comments for exported types, constants, structs, and functions.

Required documentation points:

- `@brief` for every exported type and function;
- `@param` for each parameter, including nullability and ownership expectations;
- `@return` for result codes, returned pointers, borrowed strings, or value semantics;
- ownership and lifetime notes for handles, buffers, and SDK-owned memory;
- `@threadsafe` or an explicit thread-safety note for public APIs.

Prefer comments on the declaration in the public header, not only on the implementation.

Recommended public header shape:

```cpp
#pragma once

#include <stdint.h>

#include "game_sdk/export.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct GameSdkContext GameSdkContext;

typedef enum GameSdkResult {
  GAME_SDK_RESULT_OK = 0,
  GAME_SDK_RESULT_INVALID_ARGUMENT = 1,
  GAME_SDK_RESULT_OUT_OF_MEMORY = 2,
  GAME_SDK_RESULT_IO_ERROR = 3,
  GAME_SDK_RESULT_INTERNAL_ERROR = 4
} GameSdkResult;

GAME_SDK_API GameSdkResult GAME_SDK_CALL game_sdk_create(GameSdkContext** out_context);
GAME_SDK_API void GAME_SDK_CALL game_sdk_destroy(GameSdkContext* context);

#ifdef __cplusplus
}
#endif
```

## Symbol Export Rules

Shared libraries must use explicit export macros.

Recommended export header:

```cpp
#pragma once

#if defined(_WIN32)
#if defined(GAME_SDK_BUILDING_DLL)
#define GAME_SDK_API __declspec(dllexport)
#else
#define GAME_SDK_API __declspec(dllimport)
#endif
#define GAME_SDK_CALL __cdecl
#else
#if defined(GAME_SDK_BUILDING_DLL)
#define GAME_SDK_API __attribute__((visibility("default")))
#else
#define GAME_SDK_API
#endif
#define GAME_SDK_CALL
#endif
```

For Linux, macOS, Android, and iOS shared libraries, hide symbols by default and export only explicit SDK API symbols.

## Resource Management

- Internal C++ code follows RAII.
- Use `std::unique_ptr` for exclusive ownership.
- Use `std::shared_ptr` only for true shared ownership.
- Use RAII wrappers for OS handles.
- Ensure resources are released on error paths.
- Every `create` function has a corresponding `destroy` function.
- SDK-owned memory must be released through SDK-provided functions.

## Error Handling

- Exported C API uses explicit result codes.
- Validate pointer arguments.
- Never allow exceptions to cross C ABI boundaries.
- If internal exceptions are used, catch them at the public API boundary and convert them to result codes.
- Document ownership and error behavior.

Inside GAP specifically, repository rules prohibit C++ exceptions entirely; use the project's `Result<T, E>` style instead.

## Third-Party Dependency Rules

Before introducing a dependency, explain why it is needed, whether it is header-only, whether it requires compilation, supported platforms, license compatibility, SDK export impact, binary size impact, rebuild behavior, and compile-option pollution risk.

- Header-only libraries can be included directly and wrapped with `INTERFACE` targets.
- Large compiled libraries should prefer prebuilt binaries, package managers with binary caches, imported targets, or external dependency build directories.
- Avoid `add_subdirectory(third_party/big_lib)` for heavy libraries.
- Avoid applying main project warning-as-error flags to third-party code.
- Use FetchContent only for small, header-only, test-only, or fast/stable dependencies.

## CMake Rules

- Use target-based CMake only.
- Do not use global `include_directories`, `link_libraries`, or global compile options.
- Every module should be its own target.
- Public headers must be installable.
- SDKs should export CMake package targets.
- Build should support Debug, Release, RelWithDebInfo, and MinSizeRel where applicable.
- Build should support Windows, macOS, Linux, Android, and iOS toolchains when in scope.

Recommended target pattern:

```cmake
add_library(game_sdk ${GAME_LIBRARY_TYPE}
  src/game_sdk.cc
)

add_library(game::sdk ALIAS game_sdk)

target_include_directories(game_sdk
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

target_compile_features(game_sdk PUBLIC cxx_std_17)
```

## Project Layout

Prefer an SDK-export-friendly structure:

```text
game_project/
  CMakeLists.txt
  CMakePresets.json
  cmake/
  include/game_sdk/
  src/
  modules/
  examples/
  tests/
  tools/
  third_party/
  scripts/
  .clang-format
  .editorconfig
  .gitattributes
```

## Platform Rules

### Windows

- Use `__declspec(dllexport)` / `__declspec(dllimport)`.
- Use `__cdecl` for exported C functions unless another calling convention is explicitly required.
- Prefer UTF-8 internally, but convert to UTF-16 when calling Win32 wide APIs.
- Avoid exposing Windows types in public SDK headers.

### Linux

- Use ELF shared libraries.
- Use hidden visibility by default.
- Validate exports with `nm -D`, `readelf -Ws`, `ldd`, and `objdump -T`.

### macOS

- Use Mach-O dynamic libraries.
- Use hidden visibility by default.
- Validate with `nm -gU` and `otool -L`.

### Android

- Use the Android NDK toolchain.
- Export C ABI functions for JNI or native integration.
- Be careful with API-level availability and STL runtime linkage.

### iOS

- Use Xcode or a CMake iOS toolchain.
- Prefer static libraries or frameworks depending on distribution model.
- Dynamic library usage is restricted by Apple platform rules.

## Threading Rules

- Document which thread owns each object.
- Document which APIs are thread-safe.
- Do not access destroyed objects from background threads.
- Do not hold locks while performing IO.
- Do not call user callbacks while holding locks.
- Do not create unbounded threads.
- Do not use unbounded queues without backpressure.
- Provide cancellation or shutdown mechanisms for background work.

## Testing Rules

Tests should cover normal paths, null pointer arguments, invalid struct size, invalid enum values, repeated create/destroy, error paths, cross-platform behavior, static and shared library builds, install/package discovery, and thread-safety assumptions where applicable.

Recommended commands:

```bash
ctest --test-dir build --output-on-failure
```

For SDK export validation:

- Linux: `nm -D`, `readelf -Ws`.
- macOS: `nm -gU`, `otool -L`.
- Windows: `dumpbin /EXPORTS`.

## Output Rules for Generated Answers

When generating C++ SDK work, use this structure by default:

1. selected development mode;
2. design summary;
3. directory structure or file list;
4. complete code;
5. CMake configuration;
6. build, run, test, lint, and tidy commands;
7. error handling explanation;
8. ownership and lifetime explanation;
9. thread-safety explanation;
10. cross-platform notes;
11. SDK export and ABI notes;
12. testing suggestions.

If the user asks for a short answer, compress the response but do not omit critical risks.

## Prohibited Defaults

Do not generate:

- public exported C++ classes as SDK ABI;
- public exported STL containers;
- public exported exceptions;
- public exported templates;
- public overloaded exported functions;
- raw `new` / `delete` in business logic;
- unchecked pointer arguments in C API;
- ignored error codes;
- swallowed exceptions;
- `using namespace` in public headers;
- global mutable singletons without justification;
- platform-specific types in public SDK headers;
- global CMake include paths;
- global CMake compile options that affect third-party code;
- large third-party libraries rebuilt as part of every clean main project build;
- code that only works on one platform unless explicitly requested.

## Bundled Config Files

This skill includes the repository config files under `references/config/`:

- `.clang-format` for formatting defaults;
- `.editorconfig` for charset, indentation, final newline, trimming, and line-ending policy;
- `.gitattributes` for text normalization and binary/LFS file handling.

When migrating the skill, copy these files only after checking whether the target repository already has stronger or more specific config.
