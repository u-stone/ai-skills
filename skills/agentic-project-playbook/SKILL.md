---
name: agentic-project-playbook
description: Use when defining or refining how one specific repository should operate day to day — startup, precedence, CMake, verification, git discipline, OpenCode usage, and project-local bindings for long-running AI-assisted development.
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: agentic-project-execution
  source: .opencode/skills/agentic-project-playbook/references/agentic-project-playbook-reference.md
---

# Agentic Project Playbook

## Use me when

- the task is about how **this repository** should be operated day to day;
- the team needs a repository-specific startup / maintenance / execution playbook;
- ad-hoc agent work in one repo is becoming chaotic and needs one local operating model;
- you are binding general engineering habits to this repo's concrete layout, commands, and source-of-truth files.

Typical triggers:

- "define the operating playbook for this repo"
- "document how agents should work in this repository"
- "standardize this project's startup, verification, and CMake workflow"
- "write the repo-specific playbook for long-running work here"

## Scope boundary

This skill is for **project operation inside one repository**.

Use it to define:

- repository-specific precedence and source-of-truth rules;
- project-local CMake, verification, git, and OpenCode bindings;
- startup and maintenance conventions for a long-lived codebase.

Do **not** use it as the primary skill for:

- extracting a portable cross-project engineering protocol;
- writing a reusable migration-ready ruleset for other repositories;
- defining the detailed execution loop for one complex task.

For those cases, prefer:

- `portable-authoring-protocol` for protocol extraction and migration;
- `plan-execute-verify-workflow` for task execution methodology;
- `cpp-game-sdk-coding-standard` for implementation-level C++ and CMake rules.

## Output contract

Produce results in this order unless the user explicitly wants a shorter form:

1. Purpose and scope
2. Constraint precedence
3. Fast-start protocol
4. Coding, docs, verification, and git rules
5. CMake and build-system rules
6. OpenCode configuration and session hygiene
7. Project-specific bindings and migration checklist

## Hard rules

- Read the repository instructions, status docs, and build guide first.
- Keep portable defaults separate from repository-specific bindings.
- Never fabricate build, test, QA, or tool results.
- Prefer the smallest correct change.
- Verification is part of the work, not a follow-up.
- Keep generated and local session artifacts out of normal commits.
- If the project already has stronger local rules, those override this skill.

## Execution steps

### 1. Survey the repository

Before writing the playbook, identify:

- active instruction files;
- current status / source-of-truth docs;
- canonical configure, build, test, and QA commands;
- public API layout and module boundaries;
- generated directories and local-only artifacts to exclude from commits;
- the real user-facing surfaces that must be manually tested.

### 2. Resolve precedence

Apply this order:

1. direct user instruction;
2. safety and non-fabrication rules;
3. repository-specific instructions;
4. current source-of-truth docs;
5. this skill's defaults;
6. archived plans and historical notes.

Do not let archived plans drive current behavior.

### 3. Extract portable rules first

Write the rules that should survive migration:

- startup and planning protocol;
- coding defaults;
- documentation defaults;
- verification stack;
- git discipline;
- CMake and dependency-management practices;
- OpenCode and LSP setup habits.

Do not mix these with GAP-specific values yet.

### 4. Add project bindings second

After the portable section, append the project-local bindings:

- language and language version;
- repository layout;
- naming rules;
- build and test commands;
- commit style;
- generated directories to exclude;
- required OpenCode skills or machine-local configuration.

### 5. Keep the skill entrypoint short

Use this file as the command-style entrypoint.

- Keep instructions operational.
- Use bullets and ordered steps.
- Avoid long rationale here.
- Put long explanations, examples, and migration detail in the bundled reference.

### 6. Keep the reference long

Use `references/agentic-project-playbook-reference.md` for:

- detailed rationale;
- long-form examples;
- migration checklist;
- repository-derived lessons learned.

### 7. Verify before stopping

At minimum verify:

- the skill folder contains `SKILL.md`, `README.md`, and the reference file;
- the `metadata.source` path in `SKILL.md` exists;
- README references resolve;
- the skill still matches the current repository playbook;
- any linked docs hub entry exists and is discoverable.

## CMake rules

- Apply `gap_set_strict_warnings()` per target, never globally.
- Every IDE-facing target — libraries, tools, executables, and test binaries —
  must expose the files engineers actually edit in the generated IDE project:
  own headers, own sources, and project-local dependency headers/sources added
  for visibility only.
- Do not limit this rule to installable library headers. If a target owns local
  `.hpp` / `.h` files under `src/` or a tool directory, include them in
  `target_sources(...)` so the generated Visual Studio solution is not missing
  editable headers.
- For dependency files use `target_sources(PRIVATE …)` + `HEADER_FILE_ONLY TRUE`
  on `.cpp` files so they appear in the IDE tree but are not compiled by the
  consumer.  Use `source_group()` to group them under
  `Dependencies/<dep>/Header Files` and `Dependencies/<dep>/Source Files`.
- Never alter the build graph or compile dependency `.cpp` files twice.
- Place reusable CMake helpers in `cmake/` and include them from the root
  `CMakeLists.txt`.

## Packaging rules

Expected layout:

```text
.opencode/skills/agentic-project-playbook/
  SKILL.md
  README.md
  references/
    agentic-project-playbook-reference.md
```

## Migration checklist

When copying this skill to another repository, replace these values:

- language and language version;
- build system and canonical commands;
- repository layout and module boundaries;
- code style and naming convention;
- verification bar and test framework;
- commit policy;
- excluded generated directories;
- required OpenCode skills and LSP servers.

## Bundled files

- `README.md` explains packaging and copying.
- `references/agentic-project-playbook-reference.md` contains the long-form playbook.
