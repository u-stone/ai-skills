# cpp-game-sdk-coding-standard

This folder is a shareable OpenCode skill package for C++17 game SDK and native library development.

It packages a practical coding standard for CMake-based, cross-platform game SDK work and bundles the repository formatting and text-normalization files that support the standard.

## What is included

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
```

- `SKILL.md`
  - the OpenCode skill entrypoint;
  - contains the short operational rules, triggers, and verification checklist.
- `references/cpp-game-sdk-coding-standard-reference.md`
  - the long-form distilled reference derived from `docs/standards/C++ Game SDK Coding Standard Skill.md`;
  - intended for deeper reading, migration, and team review.
- `references/config/`
  - bundled copies of the repository `.clang-format`, `.editorconfig`, and `.gitattributes` files;
  - intended as copyable defaults for new C++ game SDK repositories.

## How to use it in this repository

Project-local placement is already correct:

```text
.opencode/skills/cpp-game-sdk-coding-standard/SKILL.md
```

Agents can load it by name:

```text
cpp-game-sdk-coding-standard
```

Typical use cases:

- "Use `cpp-game-sdk-coding-standard` to design this native SDK API."
- "Load `cpp-game-sdk-coding-standard` before reviewing this CMake target."
- "Use `cpp-game-sdk-coding-standard` to create a portable C++ game SDK skeleton."
- "Apply the bundled `.clang-format`, `.editorconfig`, and `.gitattributes` defaults to a new repo."

## Do not use this skill for

- defining how one repository should operate day to day;
- extracting a portable engineering protocol from local conventions;
- running one complex implementation task through planner/executor/reviewer waves.

## Prefer these skills instead

- `agentic-project-playbook` for repository-specific operating playbooks;
- `portable-authoring-protocol` for protocol extraction and migration;
- `plan-execute-verify-workflow` for task execution methodology.

## How to copy it to another repository

Copy the whole folder into the target repository:

```text
<target-repo>/.opencode/skills/cpp-game-sdk-coding-standard/
```

Minimum required file:

```text
<target-repo>/.opencode/skills/cpp-game-sdk-coding-standard/SKILL.md
```

Recommended copy is the whole folder so the long-form reference and config files stay available.

## What to customize after copying

Review and update:

- SDK name and public C API prefix;
- supported platforms and compiler baselines;
- CMake minimum version and package/export naming;
- static/shared library policy;
- exception policy for internal implementation;
- formatting preferences in `.clang-format`;
- line-ending and charset policy in `.editorconfig`;
- binary asset and LFS policy in `.gitattributes`.

## Source of truth

This skill was derived from:

```text
docs/standards/C++ Game SDK Coding Standard Skill.md
```

The bundled config files were copied from the repository root:

```text
.clang-format
.editorconfig
.gitattributes
```

If the standard evolves, update both the source standard and this skill package.

## Verification

At minimum, verify these points after editing the skill:

- `SKILL.md` has valid YAML frontmatter;
- the folder name matches the skill name;
- `metadata.source` points to an existing reference file;
- all files listed in the bundled references section exist;
- the config files are byte-for-byte intentional copies or deliberate adaptations.
