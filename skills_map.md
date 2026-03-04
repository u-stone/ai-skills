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

## Schema
- **Version**: Semantic Versioning (Major.Minor.Patch)
- **Status**: Active, Deprecated, Experimental, In Dev
- **Limitations**: Critical constraints or missing features to be aware of.
