---
name: cpp-game-sdk-coding-standard
description: Use when writing, reviewing, or refactoring C++17 native library, native plugin, middleware, or game SDK code involving target-based CMake, mandatory project-level unit-test/example/docs/Python-workflow facilities, module directory layout with tests/examples, GoogleTest-based unit tests, architecture design documentation, cross-platform builds, public C++ headers, exported symbols, optional explicitly requested C-style APIs, ownership/lifetime rules, performance constraints, or bundled formatting/config migration.
license: MIT
compatibility: opencode
metadata:
  audience: native-sdk-engineers
  workflow: cpp-game-sdk-development
  source: references/cpp-game-sdk-coding-standard-reference.md
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
- designing exported C-style APIs over internal C++ implementation when the user explicitly requests a C-style API;
- reviewing public headers, exported symbols, ownership, lifetime, threading, or error handling;
- writing target-based CMake, install rules, package exports, or dependency wiring;
- checking that a native project has first-class unit-test, example, documentation, and workflow-script facilities before AI-assisted coding;
- designing module directory structures with module-local `tests/` and `examples/` folders;
- designing the project-level `docs/` documentation folder, especially architecture design documents;
- adding or reviewing C++ unit tests, especially GoogleTest-based tests;
- designing static/shared native library layout;
- reviewing high-performance runtime or system programming code;
- applying or migrating `.clang-format`, `.editorconfig`, or `.gitattributes` defaults.

Typical triggers:

- "review this C++ target/header/export boundary"
- "write the CMake target for this SDK/native library"
- "make this project ready for AI-assisted C++ coding"
- "design this module folder layout with tests and examples"
- "add the architecture design docs under docs/"
- "add GoogleTest unit tests for this native module"
- "design a stable C API over this C++ implementation"
- "make this Visual Studio target show the right headers and sources"
- "check whether this SDK API is ABI-safe"
- "apply the bundled formatter/config defaults"

---

## Do not use me as the primary skill for

- repository-wide operating playbooks;
- extracting reusable engineering protocols;
- planning one complex implementation through planner/executor/reviewer waves;
- non-C++ application logic with no native SDK, exported library, CMake, or performance concern.

Prefer instead:

- `team-ai-coding-governance` for team/repository AI coding governance, source-of-truth, verification, docs, and git discipline;
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
- relevant public API/export, lifetime, and thread-safety notes.

### Strict SDK mode

Use for:

- public SDK headers, exported symbols, or explicitly requested C-style API design;
- exported functions or public headers;
- shared library symbol visibility;
- install/package exports;
- binary compatibility or distribution;
- security/concurrency/performance-sensitive SDK surface.

Output must include:

- public API/export checklist;
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
   - public C++ headers, optional C-style API, symbol visibility, packaging, binary compatibility.

If unspecified, default to:

```text
Standard mode + business development + SDK-ready cross-platform design.
```

Escalate to Strict SDK mode when public headers, shared library exports, explicit C-style APIs, or SDK distribution are involved.

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

### Public SDK API and exports

* Default to C++ public headers and explicit exported symbols for C++ SDK/native-library work.
* Keep public headers minimal, stable, and documented.
* Use explicit export macros for shared-library symbols and explicit calling-convention macros when the platform or API shape requires them.
* Do not require `extern "C"`, opaque handles, C result-code APIs, or C ABI naming unless the user explicitly asks for a C-style API or an integration surface requires one.
* When a C-style API is explicitly requested, use `extern "C"`, opaque handles, versionable POD structs where practical, SDK-owned-memory release functions, and no STL/templates/references/overloads/exceptions in the C ABI.
* Public headers must document ownership, lifetime, nullability, threading, and error behavior.

### Error handling

* Public C-style APIs return explicit result codes and validate pointer arguments.
* C++ public APIs follow the repository error policy while documenting exception/result behavior.
* Do not throw exceptions across C ABI boundaries; avoid uncaught exceptions crossing shared library boundaries unless the project explicitly owns both sides and allows that ABI risk.
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

### Project facilities and CMake

* Use target-based CMake only.
* Do not use global `include_directories`, `link_libraries`, or global compile options.
* Any project that activates this skill must have three first-class facilities before non-trivial AI-assisted coding proceeds: a unit-test submodule, an example-code submodule, and a documentation submodule.
* Name those facilities `tests/`, `examples/`, and `docs/` by default. If repository-local naming already differs, map the local names explicitly and verify they serve the same roles.
* The unit-test facility stores automated unit tests and should use GoogleTest as the default C++ test framework unless repository-local rules require another framework.
* The example facility stores runnable sample code that exercises real module usage; it is not a dump for ad-hoc scratch programs.
* The documentation facility stores project documentation, primarily architecture design documents, module-boundary explanations, and key technical decisions.
* If any required project-level facility is missing, treat that as a setup blocker for AI coding: create/wire the facility first or document the blocker before changing production code.
* Any project that activates this skill must also have a project-level `scripts/` directory with a canonical Python workflow CLI at `scripts/workflow.py`. Store the unified entry point at this fixed path; do not use `.ps1`, `.bat`, or `.sh` scripts as the canonical workflow entry point. Platform-specific wrappers may exist only as optional thin delegates to the Python CLI.
* The `scripts/workflow.py` CLI must support `-h`/`--help` and standardized subcommands named `configure`, `build`, `test`, `unit`, `examples`, `lint`, `format`, `tidy`, and `workflow`. Keep these names stable so higher-level Python orchestration can compose multiple generated modules without project-specific command adapters.
* Every C++ module directory should include module-local `tests/` and `examples/` subdirectories.
* Store unit tests under the module's `tests/` directory; prefer GoogleTest as the default C++ unit-test framework unless repository-local rules require a different framework.
* Store runnable sample code under the module's `examples/` directory so users and reviewers can exercise the module's intended usage.
* If a module has a legitimate reason to omit `tests/` or `examples/`, state the exception explicitly in the plan, review, or generated directory-structure notes instead of silently omitting it.
* Use `target_compile_features(... cxx_std_17)` or equivalent.
* Public headers must be installable when building an SDK.
* Package exports should provide imported targets.
* Do not apply project warning-as-error flags to third-party code.
* Prefer imported/prebuilt targets for large compiled dependencies.
* Use FetchContent only for small, header-only, test-only, or fast/stable dependencies.
* Every target's `CMakeLists.txt` **must** list **all** target-related files — headers and sources — in `target_sources()`. Use `source_group()` to organize them into logical folders. This guarantees every file appears in the IDE project tree when the solution is generated. When a new `.h` or `.cpp` is added, update `CMakeLists.txt` in the same commit.

---

## Naming and formatting

* Follow active project `.clang-format` first.
* If none exists, use `references/config/.clang-format` as a fallback.
* Files use lowercase with underscores.
* Internal C++ types use `PascalCase`.
* Internal C++ functions use the project convention; portable default: `PascalCase`.
* Portable default variables use `lower_snake_case`.
* Class members use trailing underscore.
* Exported C-style functions, when explicitly requested, use lower snake case with an SDK prefix, e.g. `game_sdk_create`.
* C-style API constants, enum values, and macros use uppercase SDK-prefixed names.
* Never use `using namespace` in public headers.
* Public SDK declarations use Doxygen comments with `@brief`, `@param`, `@return`, ownership/lifetime notes, and thread-safety notes.

---

## Public SDK API checklist

For public headers and exported functions, verify:

* C++ public headers are the default unless the user explicitly requests a C-style API;
* explicit export macro for shared-library symbols;
* explicit calling convention when needed;
* public declarations avoid unnecessary implementation detail exposure;
* nullability documented where relevant;
* ownership/lifetime documented;
* thread safety documented;
* create/destroy or acquire/release pairing when the API transfers resources;
* SDK-owned memory release rule when the SDK allocates memory for callers;
* symbol export validation command when public exports changed.

For explicitly requested C-style APIs, additionally verify:

* `extern "C"`;
* no exported C++ classes, STL containers, templates, references, overloads, or exceptions in the C ABI;
* opaque handles;
* versionable POD config structs where useful;
* explicit result codes.

---

## CMake target checklist

For CMake changes, verify:

* target-based commands only;
* no global include/link/compile pollution;
* the project has first-class `tests/`, `examples/`, and `docs/` facilities, or equivalent locally named unit-test/example/documentation submodules are explicitly mapped;
* the project has a `scripts/workflow.py` CLI exposing `configure`, `build`, `test`, `unit`, `examples`, `lint`, `format`, `tidy`, and `workflow` subcommands;
* missing project-level unit-test/example/documentation facilities are treated as blockers before production code changes;
* each C++ module layout includes `tests/` for unit tests and `examples/` for sample code, or an explicit exception rationale is documented;
* unit-test targets use GoogleTest by default, unless repository-local rules specify a different framework;
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
* Structure: verify project-level unit-test, example, documentation, and workflow-script facilities exist and are wired into the repository's build or documentation workflow where applicable.
* Documentation: verify `docs/` exists and contains architecture design documentation for the SDK or native library surface.
* Tests: GoogleTest unit tests under module-local `tests/`, run through `ctest --test-dir build --output-on-failure` or the project equivalent.
* Examples: build and run at least one relevant example from the project/module `examples/` facility when behavior is user-visible or integration-facing.
* Workflow script: verify `scripts/workflow.py` prints help with `-h`/`--help` and exposes `configure`, `build`, `test`, `unit`, `examples`, `lint`, `format`, `tidy`, and `workflow` subcommands.
* Public exports: use `dumpbin`, `nm`, `readelf`, or `otool` when public exports changed.
* Install/package: verify install rules and package discovery when CMake exports changed.
* Runtime/manual QA: run the example, CLI, plugin load, or API driver that exercises the change.

If a check is skipped, state why.

---

## Output contract

When generating or reviewing C++ SDK work, use this structure unless the user requested a shorter answer:

1. selected mode and technical domain;
2. design summary;
3. file list or directory structure, including project-level unit-test/example/documentation/script facilities and module-local `tests/` and `examples/` folders for C++ modules or an explicit blocker/exception rationale;
4. code / patch / CMake;
5. public API/export and ownership notes;
6. error handling notes;
7. threading and performance notes when relevant;
8. Python workflow script and standardized build/test/lint/format/tidy commands;
9. platform notes;
10. risks or follow-up checks.

For short answers, compress the structure but do not omit critical public API/export, ownership, or safety risks.

---

## Reference loading policy

Use `references/cpp-game-sdk-coding-standard-reference.md` when:

* generating a new SDK skeleton;
* designing public headers, exported symbols, or explicitly requested C-style APIs;
* changing install/package exports;
* reviewing cross-platform or performance-sensitive code;
* user asks for full standard or migration guidance.

Do not load or restate the long reference for small localized fixes.
