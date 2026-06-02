# portable-authoring-protocol

This folder is a shareable OpenCode skill package for extracting and migrating
engineering protocols.

It packages a protocol-extraction skill that helps turn repository-local rules
into a reusable engineering standard that can be copied into other repositories
or into a user's global skill directory.

## What is included

```text
.opencode/skills/portable-authoring-protocol/
├── SKILL.md
├── README.md
└── references/
    └── portable-authoring-protocol-reference.md
```

- `SKILL.md`
  - the actual skill entrypoint discovered by OpenCode;
  - contains the short operational instructions and use triggers.
- `references/portable-authoring-protocol-reference.md`
  - the full long-form reference version of the protocol;
  - intended for deeper reading or for copying into another project.

## What this skill is for

Use this skill when you want to:

- extract repository conventions into a reusable engineering protocol;
- separate portable engineering rules from project-specific bindings;
- port code, docs, verification, and git rules into another repository;
- audit whether a written protocol is reusable, internally consistent, and
  migration-ready.

## Do not use this skill for

- defining how one specific repository should operate day to day;
- writing a repository startup / maintenance playbook;
- running the execution loop for one implementation task.

## Prefer these skills instead

- `agentic-project-playbook` for repository-specific operating playbooks;
- `plan-execute-verify-workflow` for execution methodology;
- `cpp-game-sdk-coding-standard` for C++/CMake implementation rules.

## How to use it in this repository

Project-local placement is already correct:

```text
.opencode/skills/portable-authoring-protocol/SKILL.md
```

Agents can load it by name:

```text
portable-authoring-protocol
```

Typical use cases:

- "Use `portable-authoring-protocol` to extract our team coding and doc rules."
- "Use `portable-authoring-protocol` to rewrite this repo's rules as a portable standard."
- "Load `portable-authoring-protocol` and adapt it for another project."

## How to copy it to another repository

Copy the whole folder into the target repository:

```text
<target-repo>/.opencode/skills/portable-authoring-protocol/
```

Minimum required file is:

```text
<target-repo>/.opencode/skills/portable-authoring-protocol/SKILL.md
```

Recommended copy is the whole folder so the bundled reference stays available.

## What to customize after copying

After moving this skill into another repository, review and update:

- language and version bindings;
- build system and canonical commands;
- code style and naming convention;
- documentation language policy;
- documentation prose formatting policy;
- test and verification expectations;
- commit policy and destructive git restrictions.

The long-form reference file includes a migration checklist for exactly that purpose.

## Source of truth

This skill is defined by the files in this folder:

- `SKILL.md`
- `references/portable-authoring-protocol-reference.md`

If the protocol evolves, update both:

- `SKILL.md`
- `references/portable-authoring-protocol-reference.md`

## Verification

At minimum, verify these points after editing the skill:

- `SKILL.md` still has valid YAML frontmatter;
- the folder name matches the skill name;
- the bundled reference path still exists;
- the copied protocol still reflects the current effective working rules.
