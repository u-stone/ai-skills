# cpp-game-sdk-coding-standard

A shareable OpenCode skill package for C++17 game SDK, native plugin, middleware, and native library development.

It packages:

- a short operational OpenCode skill entrypoint;
- a long-form C++ SDK coding standard reference;
- portable fallback config files for formatting and text normalization.

---

## Package layout

```text
.opencode/skills/cpp-game-sdk-coding-standard/
├── SKILL.md
├── README.md
└── references/
    ├── cpp-game-sdk-coding-standard-reference.md
    └── config/
        ├── .clang-format
        ├── .editorconfig
        ├── .gitattributes
        └── README.md
````

---

## What this skill is for

Use this skill for C++17 native SDK work involving:

* public C ABI design;
* internal C++ implementation;
* CMake target design;
* cross-platform native libraries;
* static/shared SDK packaging;
* symbol visibility;
* ownership, lifetime, threading, and error handling;
* high-performance runtime constraints;
* portable formatting and text-normalization defaults.

---

## What this skill is not for

Do not use this skill as the primary source for:

* repository-wide day-to-day operating rules;
* project management workflow;
* multi-agent execution methodology;
* non-C++ work with no native SDK/CMake/ABI concern.

Prefer:

* `agentic-project-playbook` for repository operating rules;
* `portable-authoring-protocol` for protocol extraction and migration;
* `plan-execute-verify-workflow` for complex task execution methodology.

---

## Workflow modes

| Mode       | Use when                                             | Output style                     |
| ---------- | ---------------------------------------------------- | -------------------------------- |
| Quick      | small review, small fix, formatting/naming check     | short finding + verification     |
| Standard   | normal SDK/native library implementation             | design + code/CMake + checks     |
| Strict SDK | public ABI, exports, packaging, binary compatibility | full ABI/checklist-driven output |

Default to Standard mode unless the task is clearly tiny or public ABI-sensitive.

---

## How to use

Project-local placement: `.opencode/skills/cpp-game-sdk-coding-standard/SKILL.md`

Agents can load it by name: `cpp-game-sdk-coding-standard`

Example prompts:

* "Use `cpp-game-sdk-coding-standard` to design this native SDK API."
* "Review this public header for ABI safety."
* "Write a CMake target for this native library."
* "Create an SDK skeleton with install/package exports."
* "Apply the bundled `.clang-format`, `.editorconfig`, and `.gitattributes` defaults to a new repo."

---

## Copying to another repository

Copy the whole folder:

`<target-repo>/.opencode/skills/cpp-game-sdk-coding-standard/`

Minimum required file:

`<target-repo>/.opencode/skills/cpp-game-sdk-coding-standard/SKILL.md`

Recommended copy includes the reference and config files.

---

## What to customize after copying

Review and update:

* SDK name;
* public C API prefix;
* supported platforms;
* compiler baseline;
* CMake minimum version;
* package/export naming;
* static/shared library policy;
* exception policy;
* formatter preferences;
* line-ending policy;
* LFS/binary asset policy;
* generated/local artifact policy.

---

## Config migration warning

Bundled config files are portable defaults, not universal truth.

Before copying `.clang-format`, `.editorconfig`, or `.gitattributes` into a target repository:

1. check whether the target repository already has stronger local rules;
2. compare indentation, line endings, charset, and formatter sections;
3. confirm binary and asset file handling;
4. confirm Git LFS is available and desired;
5. avoid overwriting existing project-specific policy unless explicitly requested.

---

## Verification after editing this skill

* [ ] `SKILL.md` has valid YAML frontmatter.
* [ ] Folder name matches `cpp-game-sdk-coding-standard`.
* [ ] `metadata.source` points to an existing reference file.
* [ ] Bundled reference files exist.
* [ ] Config files are intentional copies or deliberate adaptations.
* [ ] README and SKILL agree on use cases and exclusions.
* [ ] Strict SDK mode includes ABI, ownership, threading, and export checks.


