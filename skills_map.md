# Gemini CLI Skills Map

This file acts as a central registry for all installed skills, tracking their versions, status, and limitations.
Ideally, the `skill-master` skill should be used to maintain this file automatically.

| Skill Name | Version | Last Updated | Status | Known Limitations | Description |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **robust-singleton-cpp** | 1.0.0 | 2026-02-05 | Active | None | Thread-safe, DLL-safe singleton implementation for C++11+. |
| **cpp-abi-stable-pimpl** | 1.2.0 | 2026-02-05 | Active | Manual memory management req. | Standard PIMPL idiom using raw pointers for ABI stability. Now supports Fast PIMPL, C-wrappers, and Smart Pointers. |
| **skill-master** | 0.1.1 | 2026-02-05 | In Dev | Self-referential | A meta-skill to manage, audit, and optimize other skills. |
| **cmake-library-architect** | 0.1.0 | 2026-02-05 | Active | None | Guidelines for architecting professional C++ libraries with CMake. |
| **engineering-master** | 0.1.0 | 2026-02-26 | Active | Requires project documentation (plan.md, etc.) | Implements high-rigor industrial software engineering workflows. |

## Schema
- **Version**: Semantic Versioning (Major.Minor.Patch)
- **Status**: Active, Deprecated, Experimental, In Dev
- **Limitations**: Critical constraints or missing features to be aware of.
