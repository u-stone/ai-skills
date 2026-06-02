# plan-execute-verify-workflow

This folder is a shareable skill package for running complex AI-assisted work
with planner, executor, reviewer, evidence, and recovery roles.

It packages a portable version of the Prometheus/Atlas-style workflow so it can
be copied into another repository or used without the Oh My OpenCode plugin set.

## What is included

```text
.opencode/skills/plan-execute-verify-workflow/
├── SKILL.md
├── README.md
└── references/
    └── plan-execute-verify-workflow-reference.md
```

- `SKILL.md`
  - short operational entrypoint discovered by OpenCode;
  - describes when to use the workflow and the mandatory loop.
- `references/plan-execute-verify-workflow-reference.md`
  - long-form reference for copying, migration, and human review.

## What this skill is for

Use this skill when you want to:

- turn a user goal into a structured execution plan;
- run that plan through small verified tasks;
- persist evidence and decisions across sessions;
- prevent lost background work and partial task launches;
- require independent final review before completion.

## How to use it in this repository

Project-local placement:

```text
.opencode/skills/plan-execute-verify-workflow/SKILL.md
```

Agents can load it by name:

```text
plan-execute-verify-workflow
```

Typical use cases:

- "Use `plan-execute-verify-workflow` to plan and execute this feature."
- "Convert this task into a Prometheus/Atlas-style plan, but keep it portable."
- "Create a plan with evidence gates and final reviewers."

## Do not use this skill for

- defining repository-wide operating rules;
- extracting a reusable engineering protocol from local conventions;
- language-specific C++ or CMake implementation rules.

## Prefer these skills instead

- `agentic-project-playbook` for repository-specific operating playbooks;
- `portable-authoring-protocol` for protocol extraction and migration;
- `cpp-game-sdk-coding-standard` for implementation-level C++ and CMake rules.

## How to copy it to another repository

Copy the whole folder into the target repository:

```text
<target-repo>/.opencode/skills/plan-execute-verify-workflow/
```

Minimum required file:

```text
<target-repo>/.opencode/skills/plan-execute-verify-workflow/SKILL.md
```

Recommended copy is the whole folder so the long reference stays available.

## What to customize after copying

Replace project bindings:

- build and test commands;
- style and documentation rules;
- evidence directory;
- commit policy;
- task state file format;
- background task persistence mechanism;
- reviewer names or tools;
- generated/local files that must not be committed.

Keep the portable core unchanged: plan first, execute in small verified tasks,
save evidence, run independent reviews, and treat session recovery as normal.

## Source of truth

This skill is defined by:

- `SKILL.md`
- `references/plan-execute-verify-workflow-reference.md`

It was derived from:

- `docs/guides/agentic_task_execution_methodology.md`
- `.sisyphus/` plan, notepad, and evidence records

If the methodology evolves, update both the guide and this skill package.

## Verification

After editing this skill, verify:

- `SKILL.md` has valid YAML frontmatter;
- the folder name matches the skill name;
- the bundled reference path exists;
- the docs guide link in `docs/README.md` is present;
- the reference still matches the current methodology.
