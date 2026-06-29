# Gemini CLI Skills Map

This file acts as a central registry for all installed skills, tracking their versions, status, and limitations.
Ideally, the `skill-master` skill should be used to maintain this file automatically.

| Skill Name | Version | Last Updated | Status | Known Limitations | Description |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **robust-singleton-cpp** | 1.0.0 | 2026-03-04 | Active | None | Thread-safe, DLL-safe singleton implementation for C++11+. |
| **cpp-abi-stable-pimpl** | 1.2.0 | 2026-03-04 | Active | Manual memory management req. | Standard PIMPL idiom using raw pointers for ABI stability. Now supports Fast PIMPL, C-wrappers, and Smart Pointers. |
| **skill-master** | 0.1.2 | 2026-03-04 | Active | Self-referential | A meta-skill to manage, audit, and optimize other skills. |
| **cmake-library-architect** | 0.1.0 | 2026-03-04 | Active | None | Guidelines for architecting professional C++ libraries with CMake. |
| **cpp_cmake_engineering** | 0.1.0 | 2026-03-04 | Active | None | Add complete engineering infrastructure to an existing C++ CMake project. |
| **project-launcher** | 0.1.0 | 2026-03-04 | Active | None | 自动识别项目类型并应用 ~/.gemini/rules/ 下的规则模版。 |
| **dmp-learning-accelerator** | 1.0.1 | 2026-03-04 | Active | Requires manual scaffold execution | Deep Mastery Protocol (DMP) — a rapid-bootstrap methodology for programming learning projects. Fuses PBL, the Feynman Technique, agile development, and long-term memory engineering into a single executable AI-collaboration protocol. |
| **skill-creator** | 0.32.1 | 2026-03-04 | Active | Built-in | Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Gemini CLI's capabilities with specialized knowledge, workflows, or tool integrations. |
| **engineering-master** | 1.0.0 | 2026-03-04 | Active | Project-specific files (plan.md, etc.) required | Implements high-rigor industrial software engineering workflows. Enforces a Plan-Align-Execute-Commit-Review cycle for complex projects. |
| **team-ai-coding-governance** | 1.0.0 | 2026-06-12 | Active | Requires project command bindings | Language-neutral team AI-assisted coding governance: source-of-truth precedence, tests/examples/docs, warning-free verification, git discipline, and C/C++ skill routing. |
| **cpp-python-bindings** | 0.1.0 | 2026-06-05 | Active | Requires stable C ABI from upstream | C++ native extension packaging and wheel delivery for Python — nanobind/pybind11, scikit-build-core, STABLE_ABI, editable install, multi-module layout. |
| **cpp-game-sdk-coding-standard** | 0.1.0 | 2026-06-05 | Active | None | Portable C++17 coding standard for game SDKs, native libraries, and middleware — target-based CMake, ABI stability, ownership, threading, error handling, and config migration. |
| **plan-execute-verify-workflow** | 0.1.0 | 2026-06-05 | Active | Requires plan/state/evidence directory setup | Mode-based planning workflow for AI-assisted work — Lite/Standard/Critical, structured evidence, compact state, targeted review, recovery protocol. |
| **c-style-api-design** | 0.1.0 | 2026-06-05 | Active | Requires downstream binding work per language | Cross-language C-style API shape for Lua/Python/C#/JS scripting bindings — opaque handles, error codes, callbacks, buffers, strings, versioning, and thread-safety contracts. |
| **cpp_win_path_safety** | 0.1.0 | 2026-06-05 | Active | Legacy skill — no standardized frontmatter | Systematic C++ path safety for AI agents — resolves std::filesystem::path encoding issues on Windows across C++17 defensive and C++20 type-safe branches. |

## Schema
- **Version**: Semantic Versioning (Major.Minor.Patch)
- **Status**: Active, Deprecated, Experimental, In Dev
- **Limitations**: Critical constraints or missing features to be aware of.
