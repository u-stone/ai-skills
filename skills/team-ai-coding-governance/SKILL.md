---
name: team-ai-coding-governance
description: Use for nearly all new module work and for AI-assisted code, test, example, documentation, build, or git changes that need team-wide consistency. This language-neutral skill defines source-of-truth precedence, agent startup discipline, unit-test/example requirements, warning/error-free verification, documentation decisions, git initialization and commit rules, and repository binding hygiene. For C or C++ source, headers, CMake, native libraries, SDKs, or exported symbols, also use cpp-game-sdk-coding-standard.
license: MIT
compatibility: opencode
metadata:
  audience: team-engineers
  workflow: ai-coding-governance
  source: skills/team-ai-coding-governance/references/team-ai-coding-governance-reference.md
  modes:
    - quick
    - standard
    - strict
---

# Team AI Coding Governance

A language-neutral team operating standard for AI-assisted coding.

Use this skill to keep agents consistent when they create or change modules, code, tests, examples, documentation, build files, or git history. It replaces the old split between repository playbooks and portable authoring protocols.

---

## Use me when

Use this skill for nearly all non-trivial coding work, especially:

- creating a new module, package, service, library, plugin, SDK, or command;
- adding or changing production code;
- adding or changing build, test, lint, format, CI, packaging, or release configuration;
- deciding whether new unit tests, examples, or docs are required;
- defining repository-local AI coding rules, verification commands, or source-of-truth maps;
- standardizing team behavior for AI-assisted coding across repositories;
- committing completed code changes after verification.

For tiny prose-only edits or one-line non-code corrections, use Quick mode and keep the workflow lightweight.

---

## Do not use me as the primary skill for

- complex task orchestration through planner/executor/reviewer waves; use `plan-execute-verify-workflow`;
- implementation-level C/C++/CMake/native SDK rules; also use `cpp-game-sdk-coding-standard`;
- C-style API shape for scripting-language bindings; also use `c-style-api-design`;
- pure skill authoring or skill audits; use the dedicated skill-creation or audit workflow.

This skill governs the work. It does not replace language-specific coding standards.

---

## Required language routing

When the task touches C or C++ source files, headers, CMake targets, native libraries, SDK exports, public headers, or platform-native plugin bindings, also apply `cpp-game-sdk-coding-standard`.

Trigger that association when any of these appear:

- files ending in `.c`, `.h`, `.hpp`, `.cpp`, `.cc`, `.cxx`, `.cmake`, or `CMakeLists.txt`;
- task terms such as C, C++, CMake, native library, SDK, plugin, middleware, shared library, static library, public header, exported symbol, ABI, GoogleTest, or `.clang-format`;
- a request to generate, review, refactor, package, export, or test C/C++ code.

Do not duplicate C++ naming, formatting, ownership, threading, error-handling, CMake, ABI, or packaging rules here. The C++ skill defaults to C++ public headers and exported symbols; C-style APIs are only for explicit C-style API, C ABI, FFI, or binding requests.

---

## Mode selection

Choose the lightest mode that satisfies the request.

### Quick mode

Use for small rule checks, small code/doc updates, command/path updates, or verifying whether a test/example/doc is needed.

Output:

- selected mode;
- change or finding;
- verification note;
- commit status if code changed.

### Standard mode

Use for normal new module work, code changes, build/test updates, repository governance updates, or multi-file changes.

Output:

1. selected mode and scope;
2. source-of-truth summary;
3. implementation/test/example/doc plan;
4. verification commands and results;
5. git actions and commit reference.

### Strict mode

Use for public APIs, shared modules, core algorithms, production-facing behavior, cross-team modules, third-party dependency changes, security-sensitive changes, or C/C++ work involving public headers, native exports, or packaging.

Output must include:

- source-of-truth map;
- unit-test and example coverage decision;
- warning/error-free build record;
- runtime/no-crash verification record;
- docs decision;
- git status and commit record;
- known uncertainties or blockers.

---

## Rule precedence

When rules conflict, apply this order:

1. direct user instruction;
2. safety, integrity, and non-fabrication rules;
3. repository-local instruction files;
4. current source-of-truth docs;
5. active build/test/tooling configuration;
6. this skill's portable defaults;
7. archived plans, stale docs, and historical notes.

Archived docs may explain history but do not drive current behavior unless the user reactivates them.

---

## Startup protocol

Before changing code, gather only the context needed for the selected mode:

- active repository instructions;
- source-of-truth docs and docs hub;
- canonical configure/build/test/lint/format/manual QA commands;
- module boundaries and dependency direction;
- existing test and example patterns;
- generated/intermediate/local-only artifacts;
- git repository state and dirty worktree state;
- language-specific skills required for the touched files.

Do not repeatedly reread unchanged files. Maintain a compact source-of-truth map for long work.

---

## Coding requirements

For every code change:

- read relevant files before changing them;
- prefer the smallest correct change;
- match existing project style and architecture;
- avoid unrelated refactors;
- validate only at real boundaries unless project rules require more;
- do not fabricate behavior, test results, build output, or tool output.

For new modules and meaningful production-code changes:

- add or update relevant unit-test code;
- add or update a runnable example or document why no meaningful example exists;
- keep implementation, unit tests, examples, and relevant docs in the same verified change set;
- compile the affected first-party implementation, tests, and examples with no warnings and no errors;
- run the relevant tests and examples with no crash and no unhandled exception.

The warning-free requirement applies to first-party code. Do not force third-party libraries to satisfy this repository's warning policy unless the team intentionally vendors and maintains them as first-party code.

---

## Documentation rules

Documentation prose is not source code. Do not apply code formatting rules such as line width to prose unless repository policy explicitly says so.

Documentation must still be exact:

- paths, identifiers, commands, and type names must match reality;
- code examples must be technically correct for the active API and language version;
- stale docs must be marked or ignored according to source-of-truth precedence.

Create or update docs under `docs/` when the change introduces or materially changes:

- module architecture or boundaries;
- implementation details future maintainers need to modify behavior safely;
- non-trivial, performance-sensitive, correctness-sensitive, or domain-specific algorithms;
- third-party libraries, unusual configuration, wrapped APIs, or dependency tradeoffs;
- public contracts, extension points, or integration flows.

Do not create docs only to look complete. Prefer targeted docs with a durable audience.

---

## Verification rules

Verification is part of the work, not a follow-up.

For code changes, verify the relevant first-party surfaces:

- diagnostics or type checks where available;
- configure/build with no warnings and no errors for changed first-party code;
- unit tests for changed behavior;
- examples for new modules or integration-facing behavior;
- manual QA through the real user-facing surface when applicable.

If verification cannot run, state the blocker and do not claim success. If unrelated pre-existing warnings or failures block a clean result, identify them separately from the current change.

Use this record format when reporting completion:

```markdown
## Verification
- Files checked:
- Commands run:
- Unit tests:
- Examples:
- Build warnings/errors:
- Manual QA:
- Commands not run:
- Known uncertainty:
```

---

## Git rules

All code governed by this skill should be under git.

- If the current workspace is not inside a git repository, initialize git before implementation unless the user forbids it.
- Inspect `git status` and the intended diff before every commit.
- Keep generated files, build outputs, caches, local sessions, evidence logs, scratch notes, and machine-local config out of normal commits.
- After each verified code change or cohesive module increment, create an atomic commit once relevant first-party builds/tests/examples pass with no warnings and no errors.
- Stage only intended files.
- Keep tests, examples, and docs with the implementation commit they verify.
- Do not rewrite history or run destructive git commands without explicit permission.
- Do not revert unrelated dirty-worktree changes.

If repository or session rules impose a stricter commit policy, follow the stronger active rule while preserving atomicity and verification.

---

## Reference loading policy

Use `references/team-ai-coding-governance-reference.md` when:

- creating a new project or module governance baseline;
- resolving conflicting repository rules;
- deciding test/example/docs requirements for non-trivial work;
- designing a source-of-truth map or repository binding manifest;
- explaining migration from the replaced governance skills;
- writing evals or auditing whether the skill is being applied correctly.

Do not load or restate the long reference for small localized fixes.
