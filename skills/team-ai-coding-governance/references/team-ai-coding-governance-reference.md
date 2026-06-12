# Team AI Coding Governance Reference

This reference defines a project-agnostic team standard for AI-assisted coding. It combines the useful parts of the former repository playbook and portable authoring protocol into one governance skill.

It is not tied to any project name or programming language. Repository-specific values belong in bindings, not in the portable rules.

---

## 1. Purpose and scope

A team AI coding governance skill answers:

- where agents should start before coding;
- which instructions and docs are authoritative;
- when code changes require unit tests, examples, docs, and manual QA;
- which verification commands decide whether work is complete;
- how git is initialized, kept clean, and committed;
- when language-specific skills must be applied.

This skill governs AI-assisted engineering behavior. It does not replace language-specific coding standards or complex execution workflows.

---

## 2. Operating modes

### Quick mode

Use for small updates, small checks, and localized corrections.

Expected output:

- selected mode;
- affected file or rule;
- verification note;
- commit status if code changed.

### Standard mode

Use for normal code changes and new modules.

Expected output:

- source-of-truth summary;
- plan covering implementation, unit tests, examples, docs, verification, and git;
- verified change set;
- atomic commit record when verification passes.

### Strict mode

Use for public APIs, shared modules, core algorithms, production-facing changes, third-party dependencies, cross-team modules, and C/C++ public headers/exports.

Expected output:

- source-of-truth map;
- repository binding manifest updates when needed;
- unit-test coverage;
- runnable example coverage;
- no-warning/no-error build record;
- runtime no-crash/no-unhandled-exception record;
- docs decision;
- git commit record;
- blockers and known uncertainty.

---

## 3. Constraint precedence

When rules conflict, apply:

1. direct user instruction;
2. safety, integrity, and non-fabrication rules;
3. repository-local instruction files;
4. current source-of-truth docs;
5. active build/test/tooling configuration;
6. this skill's portable defaults;
7. archived plans, stale docs, and historical notes.

Archived documents can explain history but must not drive current behavior unless explicitly reactivated.

---

## 4. Source-of-truth map

Use a compact map for non-trivial work and long sessions:

```json
{
  "instructions": [
    {
      "path": "",
      "status": "active | archived | unknown",
      "notes": ""
    }
  ],
  "status_docs": [],
  "docs_hub": "",
  "canonical_commands": {
    "configure": "",
    "build": "",
    "test": "",
    "unit": "",
    "examples": "",
    "lint": "",
    "format": "",
    "manual_qa": []
  },
  "repo_layout": {
    "source": [],
    "tests": [],
    "examples": [],
    "docs": [],
    "tools": [],
    "generated": []
  },
  "module_boundaries": [],
  "local_artifacts_to_exclude": [],
  "active_language_skills": [],
  "archived_or_non_binding_docs": []
}
```

Keep it compact. It is a navigation aid, not a substitute for reading files relevant to the current change.

---

## 5. Repository binding manifest

Separate portable rules from repository-specific values:

```json
{
  "project_name": "",
  "languages": [],
  "language_versions": {},
  "build_system": "",
  "canonical_commands": {
    "configure": "",
    "build": "",
    "test": "",
    "unit": "",
    "examples": "",
    "lint": "",
    "format": "",
    "manual_qa": []
  },
  "repository_layout": {},
  "module_boundaries": [],
  "style_rules": [],
  "documentation_policy": [],
  "verification_policy": [],
  "git_policy": [],
  "generated_or_local_artifacts": [],
  "required_language_skills": [],
  "tooling": {
    "lsp": [],
    "formatters": [],
    "linters": []
  },
  "archive_policy": "",
  "known_risks": []
}
```

Never promote project-specific paths, commands, or style values into portable rules without labeling them.

---

## 6. Startup protocol

Before implementation work:

1. read active repository instruction files;
2. identify current source-of-truth docs and stale docs;
3. identify canonical build, unit-test, example, lint, format, and manual QA commands;
4. inspect existing code, test, example, and docs patterns for the touched area;
5. identify generated and local-only files that must not be committed;
6. inspect git repository state and dirty worktree state;
7. identify language-specific skills needed for the files involved;
8. create or update the source-of-truth map if needed.

Parallelize independent context gathering when it reduces uncertainty, but do not duplicate a specialist search already in progress.

---

## 7. Language-specific routing

This skill is language-neutral. It routes to language-specific skills when implementation details matter.

For C/C++/CMake/native library work, also use `cpp-game-sdk-coding-standard` when any of the following apply:

- files: `.c`, `.h`, `.hpp`, `.cpp`, `.cc`, `.cxx`, `.cmake`, `CMakeLists.txt`;
- concepts: SDK, native library, native plugin, middleware, CMake target, shared library, static library, public header, exported symbol, ABI, C++17, GoogleTest, `.clang-format`;
- actions: C/C++ generation, review, refactor, packaging, export, test, example, or documentation.

Do not duplicate that skill's implementation rules. It owns C++ naming, formatting, CMake, public header/export, ownership, lifetime, threading, performance, packaging, and C-style API details.

C-style APIs are not the default for C++ work. Use C-style rules only when the user explicitly asks for C-style API, C ABI, FFI, scripting binding, or a native integration boundary that requires it.

When scripting-language binding API design is the focus and `c-style-api-design` is available, use it alongside the C++ skill.

---

## 8. Coding protocol

For code changes:

- read before changing;
- search existing patterns before inventing new ones;
- prefer the smallest correct change;
- fix root causes when scope stays reasonable;
- do not add speculative fallbacks, retries, compatibility shims, or feature flags unless required;
- match local style and architecture;
- validate at user input, external API, untrusted I/O, and persistence boundaries;
- preserve public behavior unless the user requested a behavior change.

For every meaningful production-code change, explicitly decide:

- which unit tests need to be added or updated;
- which runnable example needs to be added or updated;
- whether docs under `docs/` need to be added or updated;
- which verification commands must pass before commit.

The default answer for new modules is that unit tests and examples are required. Exceptions must be written down with a concrete reason.

---

## 9. Unit-test and example requirements

Unit tests are required when:

- new first-party production code is added;
- behavior changes;
- a bug is fixed;
- public contracts or boundaries change;
- core algorithms, parsing, serialization, concurrency, or error handling are involved;
- a previous missing test would make safe maintenance difficult.

Examples are required when:

- a new module is introduced;
- public APIs or extension points are introduced;
- integration steps are non-obvious;
- the module is intended for reuse by another team or future agent;
- user-visible behavior needs a runnable demonstration.

Examples must be runnable through the repository's normal workflow where possible. They are not scratch programs.

If no meaningful example exists, document the exception in the plan or final report.

---

## 10. Build and runtime verification

For each verified code increment:

- build affected first-party production code with no warnings and no errors;
- build affected unit-test code with no warnings and no errors;
- build affected example code with no warnings and no errors;
- run relevant unit tests with no failure;
- run relevant examples with no crash and no unhandled exception;
- run manual QA through the real surface when applicable.

Third-party libraries are excluded from the team's no-warning policy unless intentionally maintained as first-party code. Isolate third-party warnings instead of weakening first-party standards.

If a repository has no canonical command yet, define one before relying on ad-hoc commands for repeated work.

---

## 11. Documentation decision rules

Documentation prose is distinct from source code. Do not impose code line-width or formatting rules on prose unless repository policy explicitly requires it.

Documentation must remain exact:

- file paths and command names are real;
- code examples match the actual API and language version;
- old or speculative notes are marked as non-binding;
- docs are discoverable from the expected hub when they are durable.

Create or update `docs/` content when a change affects:

- module architecture or dependency boundaries;
- implementation details required for safe maintenance;
- non-trivial algorithms or data structures;
- performance-sensitive or correctness-sensitive behavior;
- third-party libraries, dependency tradeoffs, unusual build options, or wrapped APIs;
- public APIs, extension points, plugin contracts, or integration workflows.

Do not create docs only for ceremony. Write the smallest durable document that helps a real future reader.

---

## 12. Git initialization and commit policy

All AI-assisted code work should be tracked by git.

If the workspace is not in a git repository:

1. initialize git before implementation unless the user forbids it;
2. create or update ignore rules for generated, intermediate, cache, local session, and machine-local files;
3. make the first commit only after the initial verifiable baseline or first cohesive verified change.

For existing git repositories:

- inspect `git status` before editing and before committing;
- assume unrelated dirty files may belong to someone else;
- never revert unrelated changes without explicit permission;
- stage only intended files;
- keep generated artifacts, build outputs, local notes, evidence logs, temporary screenshots, caches, and machine-local config out of normal commits;
- commit each cohesive verified code increment after first-party build/test/example verification passes with no warnings and no errors;
- keep implementation, unit tests, examples, and docs together when they verify the same change;
- do not hard reset, force push, rewrite history, or discard work without explicit permission.

If active repository rules require a different commit cadence, follow the stricter rule without weakening verification or atomic staging.

---

## 13. Verification record

Use this completion record for code work:

```markdown
## Verification
- Files checked:
- Source-of-truth files:
- Commands run:
- Build warnings/errors:
- Unit tests:
- Examples:
- Manual QA:
- Commands not run:
- Known uncertainty:
- Commit:
```

Do not claim a check passed without tool output from the current work.

---

## 14. Generated and local artifact exclusions

Exclude from normal commits unless explicitly intended:

- build directories and compiler outputs;
- generated intermediates;
- dependency caches;
- local session folders;
- scratch notes;
- evidence logs;
- temporary screenshots and logs;
- machine-local IDE/LSP config;
- OS/editor caches.

Record repository-specific exclusions in `.gitignore` or the local equivalent when creating a new repository.

---

## 15. Migration from replaced skills

This skill replaces:

- `agentic-project-playbook`
- `portable-authoring-protocol`

Preserved from the former project playbook:

- source-of-truth map;
- startup protocol;
- repository binding manifest;
- stale-doc precedence;
- verification record;
- session hygiene;
- package verification.

Preserved from the former authoring protocol:

- portable rules vs project bindings;
- documentation prose vs source-code formatting separation;
- documentation examples must be technically correct;
- AI execution discipline;
- non-fabrication and explicit uncertainty rules.

Dropped or narrowed:

- protocol extraction as a primary workflow;
- project-specific sample bindings;
- duplicate git and verification prose;
- any C++ implementation details that belong in `cpp-game-sdk-coding-standard`.

---

## 16. Package verification checklist

After editing this skill package:

- [ ] `SKILL.md` has valid YAML frontmatter.
- [ ] Folder name matches `team-ai-coding-governance`.
- [ ] `metadata.source` points to an existing reference file.
- [ ] README and reference agree with the entrypoint.
- [ ] Long rationale stays in the reference, not the entrypoint.
- [ ] No project-specific values are presented as portable rules.
- [ ] Old skill names appear only in migration/history notes.
- [ ] C/C++ implementation rules are routed to `cpp-game-sdk-coding-standard`.
- [ ] Unit-test, example, docs, build, and git requirements are intact.

---

## 17. Eval cases

### Eval 1: New non-C++ module

Input:

```text
Create a new data validation module for this project.
```

Expected:

- choose Standard or Strict mode based on scope;
- inspect source-of-truth and existing patterns;
- add production code, unit tests, and runnable example unless exception is justified;
- decide whether `docs/` is needed;
- build and run tests/examples with no first-party warnings/errors before commit.

Reject if:

- code is added without test/example consideration;
- no git/verification record is produced.

### Eval 2: New C++ module

Input:

```text
Add a new C++ module for loading texture metadata.
```

Expected:

- use this skill and also route to `cpp-game-sdk-coding-standard`;
- do not default to C-style API unless explicitly requested;
- include unit tests, examples, docs decision, warning/error-free build, and commit record.

Reject if:

- duplicates C++ rules here;
- forces `extern "C"` without a C-style API request.

### Eval 3: Gitless workspace

Input:

```text
This folder is not under git. Start a new module here.
```

Expected:

- initialize git unless user forbids it;
- configure artifact exclusions;
- commit only after a cohesive verified change passes.

Reject if:

- code work proceeds without git initialization or explicit user opt-out.

### Eval 4: Documentation decision

Input:

```text
Replace the caching algorithm and add a third-party dependency.
```

Expected:

- update or create `docs/` material for algorithm and dependency rationale;
- keep prose clear rather than forcing source-code line width;
- verify docs paths and examples.

Reject if:

- skips docs decision;
- documents inaccurate commands, paths, or APIs.

### Eval 5: Stale docs conflict

Input:

```text
The old plan says to use Make, but the current build config uses CMake.
```

Expected:

- active build configuration wins;
- old plan is treated as historical/non-binding unless reactivated;
- uncertainty is stated if source status is unclear.

Reject if:

- follows stale plan over current tooling.

### Eval 6: Generated artifacts in commit

Input:

```text
Commit the completed module, including anything needed.
```

Expected:

- inspect status and diff;
- stage intended source, tests, examples, docs, and config only;
- exclude build output, caches, session artifacts, and temporary files.

Reject if:

- stages broad unrelated files or generated intermediates.
