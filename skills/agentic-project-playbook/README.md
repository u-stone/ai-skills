# agentic-project-playbook

A shareable OpenCode skill package for defining how one specific repository should be operated and maintained by AI agents over time.

It packages a repository-local operating playbook pattern:

- startup protocol;
- source-of-truth precedence;
- verification commands;
- git discipline;
- build-system and tooling bindings;
- OpenCode/session hygiene;
- migration and maintenance checks.

This skill is repo-local by design. It binds general engineering habits to one repository's concrete files, commands, layout, and policies.

---

## Package layout

```text
.opencode/skills/agentic-project-playbook/
├── SKILL.md
├── README.md
└── references/
    └── agentic-project-playbook-reference.md
```

* `SKILL.md`

  * short operational entrypoint discovered by OpenCode;
  * should stay concise and command-style.
* `references/agentic-project-playbook-reference.md`

  * long-form playbook reference;
  * contains rationale, templates, examples, and migration guidance.

---

## What this skill is for

Use this skill to:

* define how agents should start work in this repository;
* document current source-of-truth files;
* bind canonical build, test, lint, and QA commands;
* define local git discipline and artifact exclusions;
* capture repository-specific OpenCode and tooling expectations;
* maintain a day-to-day operating playbook for long-running AI-assisted development.

---

## What this skill is not for

Do not use this skill as the primary tool for:

* extracting a reusable cross-project protocol;
* writing a migration-ready engineering standard;
* executing one complex feature through task/review waves;
* implementation-level C++/CMake/ABI rules.

Prefer:

* `portable-authoring-protocol` for protocol extraction and migration;
* `plan-execute-verify-workflow` for task execution methodology;
* `cpp-game-sdk-coding-standard` for implementation-level C++ and CMake rules.

---

## Modes

| Mode     | Use when                               | Output                                                 |
| -------- | -------------------------------------- | ------------------------------------------------------ |
| Quick    | small update or path/command check     | concise patch + verification note                      |
| Standard | normal playbook creation or revision   | source map + rules + bindings                          |
| Full     | first-time or large repo consolidation | full manifest + stale-doc policy + migration checklist |

Use the lightest mode that satisfies the request.

---

## How to use it

Project-local placement:

```text
.opencode/skills/agentic-project-playbook/SKILL.md
```

Agents can load it by name:

```text
agentic-project-playbook
```

Example prompts:

* "Use `agentic-project-playbook` to define our agent startup workflow."
* "Use `agentic-project-playbook` to document how this repository should run."
* "Update the repo playbook with the new test command."
* "Create a source-of-truth map for this repository."
* "Verify that the playbook still matches the current build guide."

---

## Copying to another repository

Copy the whole folder:

```text
<target-repo>/.opencode/skills/agentic-project-playbook/
```

Minimum required file:

```text
<target-repo>/.opencode/skills/agentic-project-playbook/SKILL.md
```

Recommended copy includes the bundled reference.

---

## What to customize after copying

Replace repository-specific bindings:

* project name;
* language and language versions;
* build system and canonical commands;
* repository layout and module boundaries;
* active instruction files;
* docs hub and status docs;
* style guide and naming rules;
* verification and QA expectations;
* commit policy;
* destructive git restrictions;
* generated/local artifacts to exclude;
* required OpenCode skills;
* machine-local LSP/tooling configuration.

Keep portable principles separate from repo-specific values.

---

## Source of truth

This skill package is defined by:

* `SKILL.md`;
* `references/agentic-project-playbook-reference.md`.

If the playbook evolves:

* update `SKILL.md` when operational steps or package contract change;
* update the reference when rationale, examples, or migration guidance change;
* update both when the repository's effective workflow changes.

---

## Verification after editing

* [ ] `SKILL.md` has valid YAML frontmatter.
* [ ] Folder name matches `agentic-project-playbook`.
* [ ] `metadata.source` points to an existing reference file.
* [ ] README and reference agree with the entrypoint.
* [ ] Long rationale is in the reference, not the short entrypoint.
* [ ] Repo-specific bindings are clearly labeled.
* [ ] Archived/stale docs are not treated as current rules.
