# Agentic Project Playbook Reference

This document is a reusable reference for running a complex software project
with AI agents. It was distilled from GAP, but it is written so the portable
parts can be copied into another repository with minimal rewriting.

It separates:

- rules that are broadly portable to other projects;
- GAP-specific bindings that should be replaced after migration;
- OpenCode-specific packaging and workflow advice.

## 1. Purpose and Scope

Use this reference when you need a practical playbook for:

- starting agent work in a large repository quickly;
- defining coding, documentation, verification, and git discipline;
- capturing CMake and build-system lessons in a reusable way;
- packaging those lessons as an OpenCode skill.

This reference complements repository-local rules. It does not replace direct
user instructions, repository instructions, or current source-of-truth docs.

## 2. Constraint Precedence

When rules conflict, use this order:

1. direct user instruction;
2. safety, integrity, and non-fabrication rules;
3. repository-specific instructions;
4. current source-of-truth docs;
5. this playbook's portable defaults;
6. archived plans and historical notes.

Portable lesson: always identify the active source of truth early. The biggest
time loss in long-running projects is following stale plans after the codebase
has moved on.

## 3. Fast-Start Protocol for a Complex Repository

### 3.1 Survey First

Before implementing, gather enough context to avoid blind edits:

- read the root agent instruction file;
- read the status file and docs hub;
- read the build guide and top-level build configuration;
- identify module boundaries and dependency direction;
- identify the real user-facing surface;
- identify generated directories and local-only artifacts that must not be
  committed.

### 3.2 Parallel Context Gathering

For non-trivial work, parallelize early:

- use one or two exploration agents for code patterns and ownership;
- use a librarian-style agent for unfamiliar external APIs;
- read the concrete files you already know are relevant;
- consult an Oracle-style reviewer for architecture, hard debugging, or security
  and performance tradeoffs.

Portable lesson: delegation is for context gathering, not for losing ownership.
The main agent must still understand and verify the files it changes.

### 3.3 Plan Before Editing

For complex tasks, define:

- the behavior to change;
- the files expected to change;
- the build/test/manual QA commands;
- the commit boundaries;
- the likely risk areas.

A short concrete plan prevents both over-engineering and chaotic multi-file
changes.

## 4. Execution Protocol

Use this loop:

1. explore;
2. plan;
3. implement;
4. verify;
5. manually QA;
6. commit the atomic result if requested or required by repository policy.

Portable lesson: the work is not complete when the edit is written. It is
complete when the surface behaves correctly.

## 5. Coding Rules That Transplant Well

Portable defaults:

- prefer the smallest correct change;
- fix root causes when scope stays reasonable;
- avoid speculative compatibility layers and fallback logic;
- match the surrounding style before inventing a new one;
- do not refactor unrelated code while fixing a local issue;
- validate at real boundaries only;
- keep comments sparse and useful;
- add or adjust tests when guarding a subtle bug or important behavior.

Project-local bindings to determine after copying:

- language and language version;
- naming convention;
- error-handling model;
- ownership and concurrency rules;
- public API documentation standard;
- code formatting commands.

## 6. Documentation Rules That Transplant Well

Portable defaults:

- keep a docs hub or equivalent navigation file;
- separate current rules from archive material;
- update links when moving files;
- write new docs when they serve a distinct audience or portable purpose;
- keep code examples technically correct for the actual API and language level;
- clearly mark comparative research as non-binding.

Portable lesson: documentation should help an interrupted contributor resume the
project quickly. Good docs reduce agent warm-up cost.

## 7. Git Discipline for Agentic Work

Portable defaults:

- inspect `git status`, `git diff`, and recent history before committing;
- stage only intended files;
- keep generated artifacts, local notes, and session outputs out of commits;
- split commits by independent concerns;
- keep tests with their implementation;
- do not rewrite history or use destructive git commands without permission;
- match the repository's commit-message style.

Portable lesson: the most common agent git failure is a giant mixed commit with
implementation, docs, generated output, and local artifacts all staged together.

## 8. CMake and Build-System Lessons

### 8.1 Repository Layout

Strong default for C++ library projects:

```text
include/<project>/<module>/  public headers
src/<module>/                implementation
tests/                       test sources
examples/                    runnable usage examples
tools/                       standalone tools
cmake/                       shared CMake helpers
docs/                        project documentation
```

Portable lesson: separating `include/` from `src/` makes the public surface
explicit and improves both human onboarding and agent navigation.

### 8.2 Target-Based CMake

Prefer target-based CMake:

- one target per module or responsibility unit;
- target-scoped include directories, definitions, and compile options;
- accurate `PUBLIC` / `PRIVATE` / `INTERFACE` dependency visibility;
- project-prefixed options;
- no global warning flags that pollute third-party code.

Portable lesson: warnings-as-errors should usually be target-scoped, not global.

### 8.3 IDE Project Visibility

Every library target should expose all files it uses in the generated IDE
project, not just the files it compiles directly.  This matters for code
navigation in Visual Studio, Xcode, and similar IDEs.

Recommended rule:

1. **Own public headers**: glob from the public header directory and add to
   `target_sources()`.  Mark none of them as compiled (headers already are not).
2. **Own implementation files**: list explicitly in `add_library()` or
   `target_sources()`.
3. **Dependency headers and sources**: for each linked library target, attach its
   source files for IDE visibility only.  Use `HEADER_FILE_ONLY TRUE` on `.cpp`
   files so they appear in the project tree but are not compiled by the consumer.

Use `source_group()` to organize these into readable folders such as
`Header Files`, `Source Files`, and `Dependencies/<dep>/Header Files` /
`Dependencies/<dep>/Source Files`.

Portable lesson: `HEADER_FILE_ONLY TRUE` is directory-scoped in CMake ≤ 3.17.
Setting it in the consumer's CMakeLists.txt does not affect how the owning
target compiles the same file in its own directory.

### 8.4 Dependency Management

Practical pattern:

- `find_package()` first;
- `FetchContent` fallback second;
- keep fetched sources in a persistent cache outside the build directory;
- support an explicit offline mode.

Portable lesson: a persistent dependency cache keeps rebuilds fast after build
directory resets.

### 8.5 Workflow Scripts

For developer experience, prefer one full workflow script per platform instead
of many partial scripts. A full workflow script should:

1. configure;
2. build;
3. run tests;
4. run examples or the nearest real surface.

Portable lesson: when a build-system change claims success, the workflow script
is the most valuable manual QA surface.

## 9. OpenCode Practices

### 9.1 Skills to Keep Available

Commonly useful skill types:

- repository rule extraction;
- git discipline and commit planning;
- post-implementation review;
- browser automation for web UIs;
- OpenCode customization for local skills and configuration.

### 9.2 Skill Package Layout

Recommended package:

```text
.opencode/skills/<skill-name>/
  SKILL.md
  README.md
  references/
    <skill-name>-reference.md
```

`SKILL.md` should be concise and operational. Detailed background belongs under
`references/`.

### 9.3 LSP and Tooling Configuration

Useful defaults for CMake/C++ projects:

- `clangd` for C++ with a valid compile database when possible;
- `cmake-language-server` for CMake files;
- markdown diagnostics or link checks for docs.

If the environment routes language servers by file extension, `CMakeLists.txt`
may require explicit `.txt` mapping.

Example OpenCode CMake LSP binding:

```json
{
  "lsp": {
    "cmake": {
      "command": ["cmake-language-server"],
      "extensions": [".cmake", ".txt"]
    }
  }
}
```

Portable lesson: LSP is a fast feedback layer, not the final authority. Build
and tests still decide whether the project is actually healthy.

### 9.4 Session Hygiene

Keep local artifacts out of normal commits:

- local session folders;
- build output;
- generated evidence files;
- scratch notes;
- machine-local config unless the repository explicitly tracks it.

Portable lesson: a final `git status` before commit prevents most accidental
agent pollution.

## 10. Migration Checklist

When copying this playbook to another project, replace these bindings:

- language and language version;
- build system and canonical commands;
- directory layout and module boundaries;
- code style and naming conventions;
- docs structure and language policy;
- verification bar and test framework;
- commit style and review rhythm;
- generated and local-only directories;
- required OpenCode skills and LSP servers.

## 11. GAP Binding Snapshot

Current GAP-specific bindings:

- language: C++17;
- build system: CMake with CTest;
- repository layout: `include/gap/<module>/` and `src/<module>/`;
- docs hub: `docs/README.md`;
- current rules: `AGENTS.md`, `STATUS.md`, and `docs/standards/`;
- workflow scripts: `scripts/run_linux.sh`, `scripts/run_macos.sh`,
  `scripts/run_windows.bat`;
- local artifacts to exclude: `.sisyphus/**`, `.remember/**`, `build/`,
  generated evidence logs, `gui_module.md`, and `imgui.ini`;
- commit style: `[Phase X] Implement/Fix: <brief description>`.

## 12. Final Principle

The best agent workflow is the one that keeps the project buildable,
reviewable, and resumable after interruptions. The job is not only to write
code. It is to leave behind a repository that another engineer or agent can
re-enter quickly and safely.
