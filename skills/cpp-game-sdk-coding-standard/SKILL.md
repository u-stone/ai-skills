---
name: cpp-game-sdk-coding-standard
description: Use when writing, reviewing, or refactoring C++17 native library or game-SDK code with target-based CMake, cross-platform targets, ABI-sensitive interfaces, IDE-visible target file layout, and performance/concurrency constraints.
license: MIT
compatibility: opencode
metadata:
  audience: native-sdk-engineers
  workflow: cpp-game-sdk-development
  source: .opencode/skills/cpp-game-sdk-coding-standard/references/cpp-game-sdk-coding-standard-reference.md
---

# C++ Game SDK Coding Standard

## What I do

- Guide C++17 game SDK, native plugin, middleware, and engine-adjacent library work.
- Keep public SDK boundaries ABI-stable while allowing modern C++ internally.
- Apply target-based CMake, cross-platform build hygiene, and explicit dependency rules.
- Preserve ownership, lifetime, threading, error handling, and performance constraints.
- Use the bundled repository config files as formatting and text-normalization references.

## Use me when

- generating or reviewing C++ game SDK code;
- designing a C-style exported SDK API over an internal C++ implementation;
- writing CMake targets, install rules, package exports, or dependency wiring;
- choosing project layout for static/shared native libraries;
- reviewing high-performance runtime, system programming, or cross-platform code;
- applying or migrating `.clang-format`, `.editorconfig`, or `.gitattributes` defaults.

Typical triggers:

- "review this C++ target / header / ABI boundary"
- "write the CMake target for this native library or tool"
- "fix this SDK-facing API / exported function design"
- "make this Visual Studio target show the right headers and sources"

Do **not** use this as the primary skill for:

- repository-wide operating playbooks;
- extracting a portable engineering protocol;
- planning and executing one complex task through review waves.

Prefer instead:

- `agentic-project-playbook` for repository-specific operating rules;
- `portable-authoring-protocol` for protocol extraction and migration;
- `plan-execute-verify-workflow` for task execution methodology.

## First step: select development mode

Before generating code, CMake, SDK API, layout, or refactoring guidance, identify the target mode:

1. **Business development** - readability, maintainability, iteration speed.
2. **System programming** - OS handles, threads, files, sockets, plugins, ABI, RAII.
3. **High-performance development** - cache behavior, hot paths, allocations, frame time.
4. **Low-level library / SDK** - C ABI, symbol visibility, packaging, binary compatibility.

If the user does not specify a mode, default to:

```text
Game business development + SDK-ready cross-platform design.
```

## Hard rules

- Use C++17 by default.
- Use target-based CMake only.
- Public exported SDK functions use C ABI: `extern "C"`, explicit export macros, no overloads.
- Do not expose STL containers, templates, C++ exceptions, references, or public C++ classes as SDK ABI.
- Use opaque handles for SDK objects and versionable POD structs for public config.
- SDK-owned memory must be released through SDK-provided functions.
- Public header files must document exported types and functions with Doxygen-style comments.
- Wrap resources with RAII; never leak OS handles.
- Do not throw exceptions across shared library or C ABI boundaries.
- Avoid raw `new` / `delete` in business logic.
- Avoid heap allocation, expensive logging, and lock contention in hot paths.
- Never call user callbacks while holding locks.
- Do not use global CMake include paths, link libraries, or compile options.
- Do not apply project warning-as-error flags to third-party code.

## Naming and formatting

- Follow the active project `.clang-format` first.
- If no project formatter exists, use the bundled fallback in `references/config/.clang-format`.
- Files use lowercase with underscores.
- Internal C++ types and functions use `PascalCase`.
- Internal variables use the project convention; for this skill's portable default, prefer `lower_snake_case` and member trailing underscores.
- Exported C functions use lower snake case with an SDK prefix, for example `game_sdk_create`.
- C API constants, enum values, and macros use uppercase SDK-prefixed names.
- Never use `using namespace` in public headers.
- In public headers, use Doxygen blocks with `@brief`, `@param`, `@return`, ownership/lifetime notes, and `@threadsafe` where applicable.

## CMake rules

- Require modern CMake and C++17 via target features.
- Every module should be a target; expose usage requirements with `target_*` commands.
- Every IDE-facing target must list its own implementation files **and its own
  local headers** in `target_sources(...)` so generated Visual Studio / IDE
  projects show the complete editable surface.
- When a target depends on project-local headers from another module and those
  headers are important for day-to-day editing or debugging, attach them to the
  consuming target for **IDE visibility only** without changing the build graph.
  Prefer `target_sources(PRIVATE ...)` and mark non-compiled dependency `.cpp`
  files `HEADER_FILE_ONLY` when they must appear in the solution tree.
- Mirror the target's logical layout with `source_group(...)` so headers and
  visibility-only dependency files appear in predictable folders inside the IDE.
- Support static and shared builds where SDK distribution requires it.
- Use explicit visibility settings for non-Windows shared libraries.
- Public headers must be installable and package exports should provide imported targets.
- Prefer imported targets or prebuilt artifacts for large compiled dependencies.
- Use FetchContent only for small, header-only, test-only, or fast/stable dependencies.

## Verification checklist

When completing C++ SDK work, verify the relevant surface:

- format: `clang-format --dry-run -Werror <files>` or project equivalent;
- build: configure and build Debug plus any requested shared/static variants;
- tests: run `ctest --test-dir build --output-on-failure` or project equivalent;
- ABI exports: validate symbols with `dumpbin`, `nm`, `readelf`, or `otool` when public SDK exports changed;
- install/package: verify install rules and package discovery when CMake exports changed;
- runtime/manual QA: run the actual example, CLI, plugin load, or API driver that exercises the change.

## Bundled references

- `references/cpp-game-sdk-coding-standard-reference.md` - long-form distilled standard.
- `references/config/.clang-format` - bundled formatter config from this repository.
- `references/config/.editorconfig` - bundled editor normalization config.
- `references/config/.gitattributes` - bundled Git attributes and LFS policy.
- `references/config/README.md` - how to apply and migrate the bundled config files.
