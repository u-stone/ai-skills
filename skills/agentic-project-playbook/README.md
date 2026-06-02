# agentic-project-playbook

This folder is a shareable OpenCode skill package for defining how one specific
repository should be operated and maintained over time.

It packages the GAP-derived project playbook into a repository-local skill that
can be copied elsewhere, but its primary job is to bind general engineering
habits to one repo's concrete commands, layout, and source-of-truth files.

## What is included

```text
.opencode/skills/agentic-project-playbook/
├── SKILL.md
├── README.md
└── references/
    └── agentic-project-playbook-reference.md
```

- `SKILL.md`
  - the skill entrypoint discovered by OpenCode;
  - contains the short command-style entrypoint and execution steps;
  - should stay concise and operational.
- `references/agentic-project-playbook-reference.md`
  - the long-form playbook;
  - intended for deep reading, rationale, and copying into another repository.

This package intentionally uses a two-layer shape:

- `SKILL.md` is the short command-style layer that tells an agent what to do;
- `references/agentic-project-playbook-reference.md` is the long-form human and
  migration reference that explains why.

## What this skill is for

Use this skill when you want to:

- define how agents should start, verify, and maintain work in this repository;
- document repository-specific CMake, verification, git, and OpenCode bindings;
- create a day-to-day operating playbook for long-running work in one codebase;
- standardize this repo's startup, precedence, and maintenance conventions.

## Do not use this skill for

- extracting a reusable cross-project engineering protocol;
- rewriting this repo's rules as a migration-ready standard for other repos;
- defining the plan-execute-verify loop for one complex implementation task.

## Prefer these skills instead

- `portable-authoring-protocol` for protocol extraction and migration;
- `plan-execute-verify-workflow` for task execution methodology;
- `cpp-game-sdk-coding-standard` for C++/CMake/ABI implementation rules.

## How to use it in this repository

Project-local placement:

```text
.opencode/skills/agentic-project-playbook/SKILL.md
```

Agents can load it by name:

```text
agentic-project-playbook
```

Typical use cases:

- "Use `agentic-project-playbook` to define our agent startup workflow."
- "Use `agentic-project-playbook` to define how this repository should run."
- "Use `agentic-project-playbook` to document our CMake and git discipline."

## How to copy it to another repository

Copy the whole folder into the target repository:

```text
<target-repo>/.opencode/skills/agentic-project-playbook/
```

Minimum required file is:

```text
<target-repo>/.opencode/skills/agentic-project-playbook/SKILL.md
```

Recommended copy is the whole folder so the bundled reference stays available.

## What to customize after copying

After moving this skill into another repository, review and update:

- language and language version;
- build system and canonical commands;
- repository layout and module boundaries;
- style guide and naming convention;
- documentation structure and language policy;
- test, QA, and release expectations;
- commit policy and destructive git restrictions;
- required OpenCode skills and machine-local LSP configuration.

## Source of truth

This skill is defined by the files in this folder:

- `SKILL.md`
- `references/agentic-project-playbook-reference.md`

The skill was derived from:

- `docs/guides/agentic_project_playbook.md`

If the playbook evolves, update both the guide and this skill package.

Keep them split deliberately:

- update `SKILL.md` when the operational steps or packaging contract changes;
- update the reference when the rationale, examples, or migration guidance
  changes;
- update both when the repository's effective workflow changes.

## Verification

At minimum, verify these points after editing the skill:

- `SKILL.md` still has valid YAML frontmatter;
- the folder name matches the skill name;
- the bundled reference path still exists;
- the reference still matches the current playbook and project behavior.
