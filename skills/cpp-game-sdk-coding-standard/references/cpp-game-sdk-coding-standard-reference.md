# C++ Game SDK Coding Standard Reference

## 1. Purpose and scope

This reference defines portable rules for C++17 game SDK, middleware, native plugin, and engine-adjacent native library work.

It assumes CMake and cross-platform support across Windows, macOS, Linux, Android, and iOS unless the user narrows the target.

Priorities:

1. correctness;
2. public API and export stability;
3. maintainability;
4. testability;
5. cross-platform compatibility;
6. ownership and resource lifetime;
7. error handling;
8. thread safety;
9. reasonable runtime performance;
10. clean CMake integration.

Generated code must be practical engineering code, not pseudo-code.

---

## 2. Rule precedence

Apply rules in this order:

1. direct user instruction;
2. safety, correctness, and non-fabrication rules;
3. repository-local instructions;
4. active project config files;
5. this skill's portable defaults;
6. historical or archived documents.

Repository-local rules win inside their repository unless unsafe.

---

## 3. Operating modes

### Quick mode

Use for:

- small review;
- small patch;
- naming/formatting check;
- small CMake fix.

Keep output short.

### Standard mode

Use for:

- normal SDK/native-library work;
- multi-file implementation;
- target-based CMake;
- ownership/lifetime/threading review.

Include code, CMake, and relevant verification commands.

### Strict SDK mode

Use for:

- public SDK headers;
- exported symbols;
- explicitly requested C-style APIs;
- shared library exports;
- install/package exports;
- binary compatibility.

Must include public API/export, ownership, thread-safety, error handling, symbol, packaging, and optional C-style ABI checks.

---

## 4. Technical domains

### Business development

Use for gameplay systems, editor tools, resource pipeline tools, scripting integration, configuration systems, and service integration.

Rules:

- prioritize readability;
- keep code easy to test;
- avoid premature optimization;
- isolate platform-specific code;
- use standard library facilities where appropriate;
- use `std::shared_ptr` only for true shared ownership.

Avoid:

- raw `new` / `delete`;
- mutable global state;
- macro-driven business logic;
- overly clever templates;
- hidden platform dependencies.

### System programming

Use for file systems, sockets, threading, dynamic loading, native handles, IPC, platform layers, and runtime services.

Rules:

- wrap native resources with RAII;
- never leak OS handles;
- check system API errors;
- hide platform-specific code behind narrow abstractions;
- avoid exposing platform handles through SDK APIs unless required;
- do not throw exceptions across shared library boundaries.

### High-performance development

Use for engine runtime, rendering, animation, physics, audio, networking, ECS, job systems, memory allocators, and resource streaming.

Rules:

- avoid heap allocation in hot paths;
- avoid unnecessary virtual calls in hot paths;
- avoid false sharing;
- prefer cache-friendly layouts and batching;
- avoid lock contention;
- avoid expensive logging/string formatting during frame updates;
- justify complex optimization with profiling data or clear targets.

For non-trivial algorithms, state:

- time complexity;
- space complexity;
- allocation behavior;
- hot-path suitability;
- thread-safety assumptions.

### Low-level library / SDK

Use for SDKs, shared libraries, static libraries, native plugins, middleware, and libraries distributed to external teams.

Rules:

- default public SDK surface is C++ headers with explicit exported symbols;
- public exported symbols use explicit export macros;
- C-style ABI rules apply only when the user explicitly asks for a C-style API or an integration surface requires one;
- explicitly requested C-style APIs use `extern "C"`, opaque handles, C-compatible data, and no STL/templates/references/overloads/exceptions in the C ABI;
- internal implementation may use C++17;
- public headers are stable and minimal;
- ownership/lifetime/threading/error behavior must be documented;
- SDK-owned memory is released through SDK APIs when the SDK allocates memory for callers;
- install rules and CMake package exports are provided when distributed.

---

## 5. C++ and compiler defaults

- Default language: C++17.
- Recommended CMake minimum for new portable SDKs: 3.24 unless the repository requires lower.
- Recommended compiler baselines:
  - GCC 9+
  - Clang 10+
  - AppleClang 12+
  - MSVC 19.28+
  - Android NDK Clang r23+
- Prefer `target_compile_features(target PUBLIC cxx_std_17)`.
- Avoid compiler-specific extensions unless guarded by feature checks.

---

## 6. Naming rules

- Files: lowercase with underscores, e.g. `asset_manager.h`.
- Types: `PascalCase`.
- Internal functions: follow project style; portable default is `PascalCase`.
- Variables: follow project style; portable default is `lower_snake_case`.
- Class members: trailing underscore.
- Internal constants: `kPascalCase`.
- Exported C-style functions, when explicitly requested: lower snake case with SDK prefix, e.g. `game_sdk_create`.
- C-style API constants and enum values: uppercase SDK-prefixed names.
- Namespaces: lowercase internal or public C++ namespaces as the project requires.
- No namespaces in exported C ABI when a C-style API is explicitly requested.
- Macros: uppercase snake case and minimized.
- Never use `using namespace` in public headers.

---

## 7. Formatting rules

Use the active project `.clang-format`.

If no project formatter exists, use the bundled fallback in:

```text
references/config/.clang-format
```

Portable defaults:

* spaces, not tabs;
* 4-space indentation unless project says otherwise;
* column limit around 100;
* braces for control statements;
* early returns over deep nesting;
* minimal public headers;
* Doxygen comments for exported declarations.

---

## 8. Public SDK API rules

Default public SDK work exports C++ headers and the required shared-library symbols. Do not force a C ABI when the user only asks for a C++ SDK, native library, public header, or exported symbol.

Required for default C++ public APIs:

* export macro for shared-library symbols;
* calling convention macro when the platform or API shape requires it;
* stable, minimal public headers;
* ownership/lifetime documentation;
* thread-safety documentation;
* documented exception/result behavior;
* explicit SDK-owned memory release rules when the SDK allocates memory for callers.

Use C-style ABI rules only when the user explicitly asks for a C-style API, C ABI, C-compatible plugin surface, FFI boundary, or an integration surface such as JNI/native binding requires it.

Required for explicitly requested C-style APIs:

* `extern "C"`;
* export macro;
* calling convention macro when needed;
* opaque handles;
* fixed-width integer types;
* explicit result codes;
* versionable POD structs when practical;
* ownership/lifetime documentation;
* thread-safety documentation;
* no C++ ABI exposure.

Prohibited in explicitly requested C-style ABI:

* C++ classes;
* STL containers;
* exceptions;
* templates;
* references;
* overloads;
* unstable compiler-specific ABI types.

---

## 9. Public header documentation

Every exported type, constant, struct, and function needs Doxygen-style comments.

Required documentation:

* `@brief`;
* `@param` for every parameter;
* nullability;
* ownership;
* lifetime;
* `@return`;
* thread-safety;
* error behavior.

Preferred shape for explicitly requested C-style public APIs:

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

/**
 * @brief Creates a new SDK context.
 * @param out_context Receives the created context. Must not be null. The caller owns the returned handle and must release it with game_sdk_destroy.
 * @return GAME_SDK_RESULT_OK on success, or an error code on failure.
 * @threadsafe This function is safe to call concurrently when out_context points to independent storage.
 */
GAME_SDK_API GameSdkResult GAME_SDK_CALL game_sdk_create(GameSdkContext** out_context);

/**
 * @brief Destroys an SDK context.
 * @param context Context returned by game_sdk_create. Passing null is allowed and has no effect.
 * @threadsafe The caller must ensure no other thread is using context.
 */
GAME_SDK_API void GAME_SDK_CALL game_sdk_destroy(GameSdkContext* context);

#ifdef __cplusplus
}
#endif
```

---

## 10. Symbol export rules

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

For Linux, macOS, Android, and iOS shared libraries:

* hide symbols by default;
* export only explicit SDK API symbols;
* validate final exports.

Validation commands:

```bash
nm -D libgame_sdk.so
readelf -Ws libgame_sdk.so
nm -gU libgame_sdk.dylib
otool -L libgame_sdk.dylib
dumpbin /EXPORTS game_sdk.dll
```

---

## 11. Resource management

* Internal C++ uses RAII.
* Use `std::unique_ptr` for exclusive ownership.
* Use `std::shared_ptr` only for true shared ownership.
* Use RAII wrappers for OS handles.
* Release resources on error paths.
* Every create/acquire API has a matching destroy/release API.
* SDK-owned memory is released by SDK-provided functions.

---

## 12. Error handling

Default C++ public APIs follow the repository error policy and document exception/result behavior.

Explicitly requested C-style APIs:

* return explicit result codes;
* validate pointer arguments;
* document nullability;
* catch internal exceptions if exceptions are allowed internally;
* never let exceptions cross ABI boundaries.

Portable result enum pattern:

```cpp
typedef enum GameSdkResult {
    GAME_SDK_RESULT_OK = 0,
    GAME_SDK_RESULT_INVALID_ARGUMENT = 1,
    GAME_SDK_RESULT_OUT_OF_MEMORY = 2,
    GAME_SDK_RESULT_IO_ERROR = 3,
    GAME_SDK_RESULT_UNSUPPORTED = 4,
    GAME_SDK_RESULT_INTERNAL_ERROR = 5
} GameSdkResult;
```

If a repository forbids exceptions entirely, follow its local result/error type.

---

## 13. Threading rules

* Document object thread ownership.
* Document which APIs are thread-safe.
* Do not access destroyed objects from background threads.
* Do not hold locks while doing I/O.
* Do not call user callbacks while holding locks.
* Do not create unbounded threads.
* Do not use unbounded queues without backpressure.
* Provide cancellation or shutdown for background work.

---

## 14. Third-party dependency rules

Before introducing a dependency, state:

* why it is needed;
* whether it is header-only;
* whether it requires compilation;
* supported platforms;
* license compatibility;
* SDK export impact;
* binary size impact;
* rebuild behavior;
* compile-option pollution risk.

Rules:

* prefer imported targets or prebuilt artifacts for large compiled dependencies;
* avoid `add_subdirectory(third_party/big_lib)` for heavy libraries;
* isolate third-party warnings and compile options;
* use FetchContent only for small/header-only/test-only/fast stable dependencies.

---

## 15. CMake rules

Use target-based CMake only.

Do not use:

```cmake
include_directories(...)
link_libraries(...)
add_compile_options(...)
```

as global project defaults for SDK/library logic.

Recommended target pattern:

```cmake
add_library(game_sdk ${GAME_SDK_LIBRARY_TYPE}
    src/game_sdk.cc
)

add_library(game::sdk ALIAS game_sdk)

target_sources(game_sdk
    PRIVATE
        src/game_sdk.cc
    PUBLIC
        FILE_SET public_headers
        TYPE HEADERS
        BASE_DIRS include
        FILES
            include/game_sdk/game_sdk.h
            include/game_sdk/export.h
)

target_include_directories(game_sdk
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

target_compile_features(game_sdk PUBLIC cxx_std_17)
```

CMake checklist:

* the project has three first-class AI-coding facilities: a unit-test submodule, an example-code submodule, and a documentation submodule;
* the default facility names are `tests/`, `examples/`, and `doc/`; if local names differ, the mapping is explicit and equivalent;
* missing project-level unit-test/example/documentation facilities are treated as setup blockers before production code changes;
* the project has a `scripts/workflow.py` CLI exposing `configure`, `build`, `test`, `unit`, `examples`, `lint`, `format`, `tidy`, and `workflow` subcommands;
* each module is a target;
* each C++ module directory contains module-local `tests/` and `examples/` subdirectories, or an explicit exception rationale is documented;
* module-local unit tests live under `tests/` and prefer GoogleTest unless repository-local policy chooses a different C++ test framework;
* module-local example code lives under `examples/` and demonstrates the module's intended public or integration-facing usage;
* usage requirements are scoped;
* public/private/interface dependencies are correct;
* install rules exist for distributed SDKs;
* package exports provide imported targets;
* public headers are installable;
* shared libraries use explicit visibility;
* local headers are visible in IDE targets;
* third-party flags do not pollute project targets.

---

## 16. Project layout

Recommended SDK-friendly layout:

```text
game_project/
  CMakeLists.txt
  CMakePresets.json
  cmake/
  include/game_sdk/
  src/
  modules/
  doc/
  examples/
  tests/
  tools/
  third_party/
  scripts/
  .clang-format
  .editorconfig
  .gitattributes
```

For AI-assisted C++ coding, `tests/`, `examples/`, `doc/`, and `scripts/` are mandatory engineering facilities, not optional niceties. `tests/` is the unit-test submodule and should be wired to GoogleTest by default. `examples/` is the runnable example-code submodule and should contain sample programs that exercise real intended usage. `doc/` is the documentation submodule and should primarily store architecture design documents, module-boundary explanations, and key technical decisions. `scripts/` should contain the canonical local-development and CI workflow entry point at `scripts/workflow.py`. The canonical entry point must not be a `.ps1`, `.bat`, or `.sh` script; platform-specific wrappers may exist only as optional thin delegates to the Python CLI. If a project uses different local names for non-script facilities, document the name mapping before editing production code.

The `scripts/workflow.py` CLI must support `-h`/`--help` and expose stable subcommands named:

```text
configure
build
test
unit
examples
lint
format
tidy
workflow
```

These command names form the portable integration contract. Higher-level Python orchestration should be able to call them across generated modules without hand-written command adapters.

Recommended module-local layout:

```text
modules/<module_name>/
  CMakeLists.txt
  include/
  src/
  tests/      # GoogleTest unit tests by default
  examples/   # runnable sample code for the module
```

Use the module-local `tests/` directory for unit tests and prefer GoogleTest as the default C++ unit-test framework. Use the module-local `examples/` directory for runnable examples that show intended usage. If a module legitimately has no meaningful unit-test or example surface, document the exception explicitly instead of omitting the directory silently. This module-level exception does not remove the project-level requirement to maintain working unit-test and example facilities.

---

## 17. Platform rules

### Windows

* Use `__declspec(dllexport)` / `__declspec(dllimport)`.
* Use `__cdecl` unless another convention is required.
* Prefer UTF-8 internally, convert to UTF-16 for Win32 wide APIs.
* Avoid exposing Windows types in public SDK headers.

### Linux

* Use ELF shared libraries.
* Use hidden visibility by default.
* Validate exports with `nm -D`, `readelf -Ws`, `ldd`, and `objdump -T`.

### macOS

* Use Mach-O dynamic libraries.
* Use hidden visibility by default.
* Validate with `nm -gU` and `otool -L`.

### Android

* Use the Android NDK toolchain.
* Be careful with API level availability and STL runtime linkage.
* Export C ABI functions for JNI/native integration when needed.

### iOS

* Prefer static libraries or frameworks depending on distribution model.
* Be aware of Apple platform restrictions on dynamic libraries.

---

## 18. Testing rules

Tests should cover:

* normal path;
* null pointer arguments;
* invalid struct size;
* invalid enum values;
* repeated create/destroy;
* error paths;
* static and shared builds;
* install/package discovery;
* thread-safety assumptions;
* cross-platform behavior when in scope.

Recommended command:

```bash
ctest --test-dir build --output-on-failure
```

When a module is added or restructured, verify that its `tests/` directory is wired into the build/test flow and that its `examples/` directory contains at least one runnable sample or a documented exception.

Before non-trivial AI-assisted coding, verify the project-level unit-test facility exists, is buildable, and runs through CTest or the local test runner. Prefer GoogleTest for C++ unit tests unless the repository has already standardized on another framework. Also verify the example facility exists and can build/run at least one representative example. Verify the `doc/` facility exists and contains architecture design documentation for the SDK or native library surface. Verify `scripts/workflow.py` prints help with `-h`/`--help` and exposes the standard subcommands.

---

## 19. Output template

For generated C++ SDK work:

```markdown
## Selected mode and domain

## Design summary

## Files

Include project-level unit-test/example/documentation/Python-workflow facilities. Include module-local `tests/` and `examples/` directories for C++ modules, or state the blocker/exception rationale.

## Code / CMake

## Public API/export notes

## Ownership and lifetime

## Error handling

## Thread safety

## Performance notes

## Cross-platform notes

## Verification commands

## Risks / follow-ups
```

For review output:

```markdown
## Verdict
APPROVE / REJECT / NEEDS INFO

## Findings
- [Critical/High/Medium/Low] ...

## Required fixes

## Suggested improvements

## Verification
```

---

## 20. Prohibited defaults

Do not generate:

* forcing C ABI for ordinary C++ public-header/export work;
* exposing unstable implementation details in public headers;
* undocumented exported symbols;
* throwing uncaught exceptions across a C ABI boundary;
* using STL/templates/references/overloads/exceptions in an explicitly requested C-style ABI;
* unchecked pointer arguments;
* ignored error codes;
* swallowed exceptions;
* raw `new` / `delete` in business logic;
* `using namespace` in public headers;
* global mutable singletons without justification;
* platform-specific types in public SDK headers;
* global CMake include/link/compile settings;
* large third-party libraries rebuilt on every clean build;
* one-platform-only code unless explicitly requested.

---

## 21. Config migration

Bundled config files live under:

```text
references/config/
```

They are fallback defaults.

Before copying to a target repository:

1. check existing project configs;
2. compare formatter style;
3. verify line endings;
4. verify charset;
5. verify binary and LFS patterns;
6. confirm generated files are not tracked as text;
7. do not overwrite local policy unless explicitly requested.

---

## 22. Eval cases

### Eval 1: Public SDK API generation

Input:

```text
Create a public C API for loading and unloading a texture manager.
```

Expected:

* Strict SDK mode;
* opaque handle;
* C ABI because the prompt explicitly asks for a public C API;
* export macro;
* result codes;
* Doxygen ownership and thread-safety docs;
* create/destroy pair.

Reject if:

* exports C++ class;
* uses STL in public ABI;
* omits ownership docs.

---

### Eval 2: CMake target generation

Input:

```text
Write the CMake target for a shared game SDK library with install/export support.
```

Expected:

* target-based CMake;
* no global include/link commands;
* public headers;
* install rules;
* package export;
* visibility settings.

Reject if:

* uses global `include_directories`;
* omits install/export for distributed SDK.

---

### Eval 3: Hot path review

Input:

```text
Review this per-frame update loop for performance risks.
```

Expected:

* high-performance domain;
* allocation/logging/lock contention review;
* complexity and allocation notes;
* no premature rewrite without evidence.

Reject if:

* gives only style comments;
* ignores hot-path constraints.

---

### Eval 4: Threading callback review

Input:

```text
Review this SDK callback dispatch code.
```

Expected:

* checks lock scope;
* rejects callback while holding lock;
* checks lifetime and shutdown;
* documents thread safety.

Reject if:

* allows user callback under mutex;
* ignores destroyed-object race.

---

### Eval 5: Config migration

Input:

```text
Apply the bundled .gitattributes to a new repo.
```

Expected:

* compare existing config first;
* warn that LFS policy is repository-specific;
* confirm Git LFS availability;
* avoid blind overwrite.

Reject if:

* overwrites existing config without review.

---

### Eval 6: Exception policy conflict

Input:

```text
Use exceptions internally, but the repository forbids exceptions.
```

Expected:

* repository-local rule wins;
* no exceptions;
* use result/error style.

Reject if:

* follows portable default over repo rule.
