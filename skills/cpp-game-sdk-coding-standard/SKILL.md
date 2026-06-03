---
name: cpp-game-sdk-coding-standard
description: Use when writing, reviewing, or refactoring C++17 native library, native plugin, middleware, or game SDK code involving target-based CMake, cross-platform builds, ABI-sensitive public interfaces, ownership/lifetime rules, performance constraints, or bundled formatting/config migration.
license: MIT
compatibility: opencode
metadata:
  audience: native-sdk-engineers
  workflow: cpp-game-sdk-development
  source: .opencode/skills/cpp-game-sdk-coding-standard/references/cpp-game-sdk-coding-standard-reference.md
  modes:
    - quick
    - standard
    - strict-sdk
---

# C++ Game SDK Coding Standard

A portable C++17 coding standard for game SDKs, native libraries, middleware, native plugins, and engine-adjacent modules.

Use the lightest mode that safely satisfies the user request.

---

## Use me when

Use this skill for:

- generating or reviewing C++17 SDK/native-library code;
- designing exported C ABI over internal C++ implementation;
- reviewing ABI, ownership, lifetime, threading, or error handling;
- writing target-based CMake, install rules, package exports, or dependency wiring;
- designing static/shared native library layout;
- reviewing high-performance runtime or system programming code;
- applying or migrating `.clang-format`, `.editorconfig`, or `.gitattributes` defaults.

Typical triggers:

- "review this C++ target/header/ABI boundary"
- "write the CMake target for this SDK/native library"
- "design a stable C API over this C++ implementation"
- "make this Visual Studio target show the right headers and sources"
- "check whether this SDK API is ABI-safe"
- "apply the bundled formatter/config defaults"

---

## Do not use me as the primary skill for

- repository-wide operating playbooks;
- extracting reusable engineering protocols;
- planning one complex implementation through planner/executor/reviewer waves;
- non-C++ application logic with no native SDK, ABI, CMake, or performance concern.

Prefer instead:

- `agentic-project-playbook` for repository-specific operating rules;
- `portable-authoring-protocol` for protocol extraction and migration;
- `plan-execute-verify-workflow` for complex task execution methodology.

---

## Mode selection

Before generating code, CMake, SDK API, or review output, select one mode.

### Quick mode

Use for:

- small code review;
- small CMake correction;
- naming/formatting check;
- short answer.

Output:

- selected mode;
- key finding or patch;
- focused verification command.

Do not load or restate the long reference unless needed.

### Standard mode

Use for:

- normal SDK/native library implementation;
- multi-file C++ or CMake changes;
- cross-platform concerns;
- ownership/threading/error-handling review.

Output:

- selected mode;
- design summary;
- code or patch;
- CMake/build/test guidance;
- relevant ABI/lifetime/thread-safety notes.

### Strict SDK mode

Use for:

- public SDK ABI design;
- exported functions or public headers;
- shared library symbol visibility;
- install/package exports;
- binary compatibility or distribution;
- security/concurrency/performance-sensitive SDK surface.

Output must include:

- ABI checklist;
- public header documentation requirements;
- ownership/lifetime rules;
- error handling rules;
- thread-safety notes;
- export/symbol validation commands;
- install/package verification when CMake exports changed.

---

## Development domain

Also classify the technical domain:

1. **Business development**
   - readability, maintainability, iteration speed.

2. **System programming**
   - OS handles, files, sockets, threads, plugins, dynamic libraries, RAII.

3. **High-performance development**
   - hot paths, cache behavior, allocations, lock contention, frame time.

4. **Low-level library / SDK**
   - C ABI, symbol visibility, packaging, binary compatibility.

If unspecified, default to:

```text
Standard mode + business development + SDK-ready cross-platform design.
````

Escalate to Strict SDK mode when public ABI, shared library exports, or SDK distribution is involved.

---

## Rule precedence

Apply rules in this order:

1. explicit user instruction;
2. safety, correctness, and non-fabrication rules;
3. repository-local instructions and project config;
4. active `.clang-format`, `.editorconfig`, `.gitattributes`;
5. this skill's portable defaults;
6. historical or archived documents.

If a repository-specific rule conflicts with this portable standard, the repository-specific rule wins inside that repository unless it is unsafe.

---

## Hard rules

### C++ baseline

* Use C++17 by default.
* Prefer practical engineering code over pseudo-code.
* Keep public headers minimal and stable.
* Avoid compiler-specific extensions unless guarded.

### Public SDK ABI

* Exported SDK functions must use C ABI.
* Use `extern "C"` and explicit export/calling-convention macros.
* Do not expose STL containers, C++ exceptions, templates, references, overloads, or public C++ classes as SDK ABI.
* Use opaque handles for SDK objects.
* Use versionable POD structs for public configs when practical.
* SDK-owned memory must be released through SDK-provided functions.
* Public headers must document ownership, lifetime, nullability, threading, and error behavior.

### Error handling

* Public C API returns explicit result codes.
* Validate pointer arguments.
* Do not throw exceptions across C ABI or shared library boundaries.
* If internal exceptions are allowed by the project, catch them at the SDK boundary and convert them to result codes.
* If the repository forbids exceptions, use its result/error style.

### Resource and lifetime

* Use RAII internally.
* Never leak OS handles.
* Use `std::unique_ptr` for exclusive ownership.
* Use `std::shared_ptr` only for true shared ownership.
* Avoid raw `new` / `delete` in business logic.
* Every create/acquire API needs a matching destroy/release rule.

### Threading and callbacks

* Document thread ownership and thread safety.
* Do not access destroyed objects from background threads.
* Do not hold locks while performing I/O.
* Never call user callbacks while holding locks.
* Avoid unbounded queues and unbounded thread creation.
* Provide shutdown/cancellation when background work exists.

### Performance

* Avoid heap allocation in hot paths.
* Avoid expensive logging/string formatting in frame loops.
* Avoid lock contention in performance-sensitive paths.
* State complexity, allocation behavior, and thread-safety assumptions for non-trivial algorithms.

### CMake

* Use target-based CMake only.
* Do not use global `include_directories`, `link_libraries`, or global compile options.
* Every module should be a target.
* Use `target_compile_features(... cxx_std_17)` or equivalent.
* Public headers must be installable when building an SDK.
* Package exports should provide imported targets.
* Do not apply project warning-as-error flags to third-party code.
* Prefer imported/prebuilt targets for large compiled dependencies.
* Use FetchContent only for small, header-only, test-only, or fast/stable dependencies.
* IDE-facing targets should list local headers in `target_sources(...)`.

---

## Naming and formatting

* Follow active project `.clang-format` first.
* If none exists, use `references/config/.clang-format` as a fallback.
* Files use lowercase with underscores.
* Internal C++ types use `PascalCase`.
* Internal C++ functions use the project convention; portable default: `PascalCase`.
* Portable default variables use `lower_snake_case`.
* Class members use trailing underscore.
* Exported C functions use lower snake case with an SDK prefix, e.g. `game_sdk_create`.
* C API constants, enum values, and macros use uppercase SDK-prefixed names.
* Never use `using namespace` in public headers.
* Public SDK declarations use Doxygen comments with `@brief`, `@param`, `@return`, ownership/lifetime notes, and thread-safety notes.

---

## Public SDK API checklist

For public headers and exported functions, verify:

* C ABI only;
* no exported C++ classes;
* no STL/template/reference/exception ABI exposure;
* explicit export macro;
* explicit calling convention when needed;
* opaque handles;
* versionable config structs where useful;
* result codes;
* nullability documented;
* ownership/lifetime documented;
* thread safety documented;
* create/destroy or acquire/release pairing;
* SDK-owned memory release function;
* symbol export validation command.

---

## CMake target checklist

For CMake changes, verify:

* target-based commands only;
* no global include/link/compile pollution;
* C++17 requirement is target-scoped;
* public/private/interface dependencies are correct;
* public headers are installable when required;
* shared library visibility is explicit;
* package export/import target works when required;
* IDE-visible headers are listed in `target_sources`;
* third-party warnings/options are isolated;
* static/shared variant policy is clear.

---

## Verification checklist

Run only the relevant checks for the change.

* Format: `clang-format --dry-run -Werror <files>` or project equivalent.
* Build: configure and build Debug; add Release/shared/static variants when relevant.
* Tests: `ctest --test-dir build --output-on-failure` or project equivalent.
* ABI exports: use `dumpbin`, `nm`, `readelf`, or `otool` when public exports changed.
* Install/package: verify install rules and package discovery when CMake exports changed.
* Runtime/manual QA: run the example, CLI, plugin load, or API driver that exercises the change.

If a check is skipped, state why.

---

## Output contract

When generating or reviewing C++ SDK work, use this structure unless the user requested a shorter answer:

1. selected mode and technical domain;
2. design summary;
3. file list or directory structure;
4. code / patch / CMake;
5. ABI and ownership notes;
6. error handling notes;
7. threading and performance notes when relevant;
8. build/test/format commands;
9. platform notes;
10. risks or follow-up checks.

For short answers, compress the structure but do not omit critical ABI, ownership, or safety risks.

---

## Reference loading policy

Use `references/cpp-game-sdk-coding-standard-reference.md` when:

* generating a new SDK skeleton;
* designing public ABI;
* changing install/package exports;
* reviewing cross-platform or performance-sensitive code;
* user asks for full standard or migration guidance.

Do not load or restate the long reference for small localized fixes.
