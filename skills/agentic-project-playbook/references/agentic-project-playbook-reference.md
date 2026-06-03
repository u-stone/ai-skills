# Agentic Project Playbook Reference

This reference defines a reusable method for creating and maintaining a repository-local operating playbook for AI-assisted software work.

It separates:

1. portable rules that transplant well;
2. repository-specific bindings that must be replaced after migration;
3. OpenCode packaging and session hygiene guidance.

This reference complements repository-local rules. It does not replace direct user instructions, active repository instructions, or current source-of-truth documents.

---

## 1. Purpose and scope

Use this reference when you need to define how agents should operate inside one repository.

A good project playbook answers:

- where agents should start;
- which docs are authoritative;
- which commands verify work;
- what files must not be committed;
- how build, test, QA, docs, and git discipline work;
- which local tools, skills, and LSP servers matter;
- how an interrupted agent can resume safely.

This is not a task execution plan and not a language-specific coding standard.

---

## 2. Mode selection

### Quick mode

Use for:

- updating one command or path;
- checking one playbook rule;
- verifying package references;
- small README/SKILL edits.

Output:

- concise change;
- affected section;
- verification note.

### Standard mode

Use for:

- creating or revising the repo playbook;
- documenting startup, verification, git, docs, build, and tooling rules;
- adding repo-specific bindings.

Output:

- source-of-truth map;
- precedence rules;
- fast-start protocol;
- repo binding manifest;
- verification record.

### Full mode

Use for:

- first-time playbook creation;
- large repo consolidation;
- stale-doc cleanup;
- multi-agent onboarding;
- migration preparation.

Output:

- full source-of-truth map;
- conflict/staleness assessment;
- complete playbook;
- migration checklist;
- maintenance checklist.

---

## 3. Constraint precedence

When rules conflict, apply:

1. direct user instruction;
2. safety, integrity, and non-fabrication rules;
3. repository-specific instruction files;
4. current source-of-truth docs;
5. active build/test/tooling configuration;
6. this playbook's portable defaults;
7. archived plans and historical notes.

Portable lesson:

> Always identify active source of truth early. The biggest time loss in long-running projects is following stale plans after the repository has moved on.

Archived docs can inform history, but they must not drive current behavior unless explicitly reactivated.

---

## 4. Source-of-truth map

Maintain a compact map for the repository.

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
  "build_guides": [],
  "canonical_commands": {
    "configure": "",
    "build": "",
    "test": "",
    "lint": "",
    "format": "",
    "manual_qa": []
  },
  "repo_layout": {
    "source": [],
    "tests": [],
    "docs": [],
    "tools": [],
    "generated": []
  },
  "module_boundaries": [],
  "local_artifacts_to_exclude": [],
  "active_skills": [],
  "machine_local_tooling": [],
  "archived_or_non_binding_docs": []
}
````

Rules:

* Keep it compact.
* Use it to avoid repeated full repository scans.
* Update it when canonical files or commands change.
* Do not treat it as a substitute for reading files relevant to the current change.

---

## 5. Fast-start protocol

Before implementation work in a large repository:

1. read active repository instruction files;
2. read the status/source-of-truth docs;
3. read the docs hub if present;
4. identify canonical build/test/lint/QA commands;
5. identify module boundaries and dependency direction;
6. identify generated/local-only files that must not be committed;
7. identify the real user-facing verification surface;
8. create or update the source-of-truth map if needed.

For non-trivial work, parallelize context gathering only when it reduces total uncertainty. Delegation is for discovery, not for losing ownership.

The main agent remains responsible for understanding and verifying the files it changes.

---

## 6. Planning and execution discipline

Portable execution loop:

1. explore;
2. plan;
3. implement;
4. verify;
5. manually QA when needed;
6. inspect diff;
7. commit atomic result only if requested or required.

Portable defaults:

* prefer the smallest correct change;
* fix root causes when scope stays reasonable;
* avoid speculative compatibility layers;
* avoid unrelated refactors;
* match surrounding style;
* validate at real boundaries;
* add tests for subtle or important behavior;
* keep comments sparse and useful.

Work is complete when the relevant surface behaves correctly, not when the edit is written.

For complex task decomposition, use `plan-execute-verify-workflow` instead.

---

## 7. Documentation rules

Portable defaults:

* keep a docs hub or equivalent navigation file;
* separate current rules from archive material;
* update links when moving files;
* write new docs only when they serve a distinct audience or durable purpose;
* keep code examples technically correct;
* mark comparative research as non-binding;
* avoid duplicating rules across many docs unless one is clearly the source of truth.

Good docs reduce agent warm-up cost and help interrupted work resume safely.

---

## 8. Git discipline

Portable defaults:

* inspect `git status`, `git diff`, and relevant recent history before committing;
* stage only intended files;
* keep generated artifacts, local notes, evidence logs, and session outputs out of normal commits;
* split commits by independent concerns;
* keep tests with implementation;
* do not rewrite history without explicit permission;
* do not use destructive git commands without explicit permission;
* match the repository's commit-message style.

Most agent git failures are mixed commits with implementation, docs, generated output, and local artifacts staged together.

---

## 9. Verification policy

A playbook must record canonical verification surfaces.

Recommended categories:

```json
{
  "configure": "",
  "build": "",
  "unit_tests": "",
  "integration_tests": "",
  "lint": "",
  "format": "",
  "manual_qa": [],
  "release_or_package": ""
}
```

Rules:

* Do not fabricate command results.
* If a command was not run, say it was not run.
* If manual QA is required, name the actual user-facing surface.
* If verification is impossible in the current environment, state the blocker.

Verification record format:

```markdown
## Verification
- Files checked:
- Links/paths verified:
- Commands run:
- Commands not run:
- Manual QA:
- Known uncertainty:
```

---

## 10. Build-system and CMake lessons

For C++/CMake projects, portable defaults include:

* prefer target-based CMake;
* one target per module or responsibility unit;
* target-scoped include directories, definitions, and compile options;
* accurate `PUBLIC` / `PRIVATE` / `INTERFACE` dependency visibility;
* no global warning flags that pollute third-party code;
* project-prefixed options;
* persistent dependency cache when using fetched dependencies;
* explicit offline mode when needed.

IDE visibility lesson:

* generated IDE projects should expose files engineers actually edit;
* include target-owned headers and sources;
* add dependency files for visibility only when useful;
* avoid altering the build graph or compiling dependency `.cpp` files twice.

Repository-specific CMake details belong in the binding section, not in the portable rules.

For implementation-level C++/CMake/ABI standards, use `cpp-game-sdk-coding-standard`.

---

## 11. OpenCode practices

Recommended skill package layout:

```text
.opencode/skills/<skill-name>/
  SKILL.md
  README.md
  references/
    <skill-name>-reference.md
```

Guidelines:

* `SKILL.md` is concise and operational;
* long background belongs in `references/`;
* README explains packaging, copying, and maintenance;
* machine-local LSP configuration should be documented separately unless the repository explicitly tracks it.

Useful LSP/tooling bindings for CMake/C++ projects:

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

LSP is fast feedback, not final authority. Build and tests decide actual health.

---

## 12. Session hygiene

Keep out of normal commits unless explicitly tracked:

* local session folders;
* build output;
* generated evidence files;
* scratch notes;
* machine-local config;
* temporary screenshots/logs;
* local caches.

Before commit:

1. inspect status;
2. inspect diff;
3. stage intended files only;
4. verify generated/local artifacts are excluded;
5. write a scoped commit message.

---

## 13. Repository binding manifest

Use this schema when creating or revising a repo playbook:

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
  "required_skills": [],
  "tooling": {
    "lsp": [],
    "formatters": [],
    "linters": []
  },
  "archive_policy": "",
  "known_risks": []
}
```

Separate:

* portable defaults;
* repository-specific bindings;
* historical notes.

---

## 14. Migration checklist

When copying this playbook to another project, replace:

* project name;
* language and language versions;
* build system;
* canonical commands;
* directory layout;
* module boundaries;
* code style and naming conventions;
* docs structure;
* verification bar;
* test framework;
* commit style;
* generated/local-only directories;
* required skills;
* LSP and tool configuration;
* archived/stale docs policy.

Do not leave source-project paths or commands in a migrated playbook unless they are intentionally still valid.

---

## 15. Maintenance checklist

After editing the skill package:

* [ ] `SKILL.md` has valid YAML frontmatter.
* [ ] Folder name matches skill name.
* [ ] `metadata.source` points to the reference.
* [ ] README and SKILL agree on scope.
* [ ] Reference agrees with current repository behavior.
* [ ] Long rationale is not duplicated in SKILL.
* [ ] Repo-specific values are labeled as bindings.
* [ ] Archived docs are not presented as active rules.
* [ ] Verification record states what was and was not checked.

---

## 16. Eval cases

### Eval 1: Quick command update

Input:

```text
Update the playbook because tests now run with `ctest --test-dir out/build`.
```

Expected:

* choose Quick mode;
* update only command binding;
* verify affected references;
* do not rewrite full playbook.

Reject if:

* produces unrelated broad playbook rewrite.

---

### Eval 2: First-time repo playbook

Input:

```text
Create an agentic project playbook for this repository.
```

Expected:

* choose Full mode;
* survey active instruction files;
* produce source-of-truth map;
* produce repo binding manifest;
* separate portable defaults from repo values.

Reject if:

* invents commands;
* treats archived docs as active without evidence.

---

### Eval 3: Stale docs conflict

Input:

```text
The old plan says to use Make, but the current build guide uses CMake.
```

Expected:

* current build guide wins;
* archived plan marked non-binding;
* uncertainty noted if source status is unclear.

Reject if:

* follows stale plan.

---

### Eval 4: Git hygiene

Input:

```text
Commit the playbook changes.
```

Expected:

* inspect status and diff;
* stage intended files only;
* exclude generated/local artifacts;
* avoid destructive git operations without permission.

Reject if:

* stages broad unrelated files.

---

### Eval 5: Skill boundary

Input:

```text
Run this feature through planner/executor/reviewer waves.
```

Expected:

* recommend `plan-execute-verify-workflow`;
* do not misuse project playbook as execution workflow.

Reject if:

* creates a full task execution methodology inside this skill.

---

### Eval 6: C++ implementation rule request

Input:

```text
Design a public C ABI for this SDK.
```

Expected:

* recommend `cpp-game-sdk-coding-standard`;
* optionally note how repo playbook binds that skill locally.

Reject if:

* duplicates detailed ABI standard here.

```
