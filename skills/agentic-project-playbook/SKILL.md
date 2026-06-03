---
name: agentic-project-playbook
description: Use when defining, refining, or maintaining how one specific repository should operate day to day: startup, source-of-truth precedence, verification commands, git discipline, build-system bindings, local agent rules, and long-running AI-assisted development conventions.
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: agentic-project-execution
  source: .opencode/skills/agentic-project-playbook/references/agentic-project-playbook-reference.md
  modes:
    - quick
    - standard
    - full
---

# Agentic Project Playbook

A repository-local operating playbook for AI-assisted software development.

This skill binds general engineering habits to one repository's actual layout, commands, source-of-truth files, verification surfaces, git policy, and agent tooling.

Keep this entrypoint short and operational. Put long rationale, examples, and migration guidance in the bundled reference.

---

## Use me when

Use this skill when the task is about how **this repository** should be operated, maintained, verified, or documented over time.

Typical triggers:

- "define the operating playbook for this repo"
- "document how agents should work in this repository"
- "standardize this project's startup, verification, and git workflow"
- "write the repo-specific playbook for long-running work here"
- "extract the current source-of-truth files and commands"
- "update the repository's agent startup process"

---

## Do not use me as the primary skill for

- extracting a reusable cross-project protocol;
- writing a migration-ready standard detached from this repository;
- running one complex feature through a planner/executor/reviewer workflow;
- implementation-level C++/CMake/ABI coding rules.

Prefer instead:

- `portable-authoring-protocol` for protocol extraction and migration;
- `plan-execute-verify-workflow` for complex task execution methodology;
- `cpp-game-sdk-coding-standard` for C++/CMake/ABI implementation rules.

---

## Mode selection

Choose the lightest mode that satisfies the request.

### Quick mode

Use for:

- small playbook edits;
- updating one command, path, or policy;
- answering where a repo rule should live;
- checking whether the playbook still references valid files.

Output:

- short finding;
- changed section or patch;
- verification note.

### Standard mode

Use for:

- creating or revising the main repo playbook;
- documenting startup, verification, git, build, and agent rules;
- adding repo-specific bindings.

Output:

1. purpose and scope;
2. source-of-truth map;
3. precedence rules;
4. fast-start protocol;
5. verification and git rules;
6. build/tooling bindings;
7. migration or maintenance checklist.

### Full mode

Use for:

- first-time playbook creation;
- large repo onboarding;
- consolidating scattered rules;
- resolving stale or conflicting docs;
- preparing the playbook for reuse by multiple agents.

Output must include:

- source-of-truth map;
- repo binding manifest;
- stale-doc/archive policy;
- verification contract;
- local artifact exclusion rules;
- migration checklist;
- final file/package verification.

---

## Rule precedence

When rules conflict, apply this order:

1. direct user instruction;
2. safety, integrity, and non-fabrication rules;
3. repository-local instruction files;
4. current source-of-truth docs;
5. active build/test/tooling configuration;
6. this skill's portable defaults;
7. archived plans, historical notes, and stale docs.

Do not let archived or stale documents drive current behavior.

If repository-local rules are stronger than this skill, repository-local rules win.

---

## First step: survey the repository

Before writing or revising a playbook, identify only the context needed for the requested mode.

Minimum survey:

- active instruction files;
- source-of-truth docs;
- canonical configure/build/test/QA commands;
- repository layout and module boundaries;
- generated directories and local-only artifacts;
- real user-facing surfaces that require manual QA;
- commit policy and destructive-git restrictions;
- required agent skills, tools, or LSP configuration.

Avoid repeatedly rereading unchanged files. Prefer a compact source-of-truth map.

---

## Source-of-truth map

Maintain or produce a compact map when creating or updating the playbook:

```json
{
  "instructions": [],
  "status_docs": [],
  "docs_hub": "",
  "build_guides": [],
  "canonical_commands": {
    "configure": "",
    "build": "",
    "test": "",
    "lint": "",
    "manual_qa": []
  },
  "repo_layout": {},
  "generated_or_local_artifacts": [],
  "active_skills": [],
  "archived_or_non_binding_docs": []
}
````

This map is a navigation aid, not a replacement for reading relevant files.

---

## Repo binding manifest

When producing the playbook, separate portable defaults from repository-specific bindings.

```json
{
  "project_name": "",
  "languages": [],
  "build_system": "",
  "canonical_commands": {},
  "layout": {},
  "module_boundaries": [],
  "style_rules": [],
  "docs_policy": [],
  "verification_policy": [],
  "git_policy": [],
  "local_artifacts_to_exclude": [],
  "required_agent_skills": [],
  "machine_local_tooling": []
}
```

Never mix reusable principles and one-repo values without labeling them.

---

## Hard rules

* Read active repository instructions before defining repository behavior.
* Keep portable defaults separate from repo-specific bindings.
* Never fabricate build, test, QA, LSP, or tool results.
* Verification is part of the work, not a follow-up.
* Prefer the smallest correct playbook change.
* Keep generated output, local session artifacts, and machine-local files out of normal commits.
* Do not rewrite history or run destructive git commands without explicit permission.
* If a command was not run, say it was not run.
* If source-of-truth is incomplete or conflicting, state the uncertainty.

---

## Output contract

Unless the user requests a shorter form, produce:

1. selected mode;
2. purpose and scope;
3. source-of-truth map;
4. constraint precedence;
5. fast-start protocol;
6. coding, docs, verification, and git rules;
7. build/tooling bindings;
8. OpenCode and session hygiene;
9. project-specific binding manifest;
10. migration or maintenance checklist;
11. verification record.

---

## Verification record

When completing playbook work, include:

```markdown
## Verification
- Files checked:
- Links/paths verified:
- Commands verified:
- Commands not run:
- Known uncertainty:
```

Do not claim verification without evidence.

---

## Packaging rules

Expected layout:

```text
.opencode/skills/agentic-project-playbook/
  SKILL.md
  README.md
  references/
    agentic-project-playbook-reference.md
```

After editing this skill package, verify:

* `SKILL.md` has valid YAML frontmatter;
* the folder name matches the skill name;
* `metadata.source` points to an existing reference;
* README and reference agree with the entrypoint;
* repo-specific bindings are not accidentally promoted to portable rules.

---

## Reference loading policy

Use `references/agentic-project-playbook-reference.md` when:

* creating the playbook from scratch;
* resolving conflicting repository rules;
* preparing migration guidance;
* explaining rationale;
* producing long-form examples.

Do not load or restate the long reference for small playbook edits.
