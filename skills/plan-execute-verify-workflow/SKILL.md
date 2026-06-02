---
name: plan-execute-verify-workflow
description: Use when one complex task or feature needs a planner/executor/reviewer workflow with evidence gates, session recovery, and final independent verification — especially when direct ad-hoc implementation would be too risky or too large.
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: plan-execute-verify
  source: .opencode/skills/plan-execute-verify-workflow/references/plan-execute-verify-workflow-reference.md
---

# Plan Execute Verify Workflow

## Use me when

- a task is too large for one direct edit;
- the user wants a Prometheus-style plan and Atlas-style execution process;
- work must survive multiple sessions or agents;
- evidence, review gates, and scope control matter;
- you need a portable workflow that can run without Oh My OpenCode.

Typical triggers:

- "turn this feature into a plan and execute it step by step"
- "run this migration with evidence gates and review waves"
- "I need a planner/executor/reviewer workflow for this task"
- "make this multi-session task recoverable and verifiable"

Do **not** use this as the primary skill for:

- repository-wide operating rules;
- extracting a reusable engineering protocol from local conventions;
- language-specific C++ / CMake implementation rules.

Prefer instead:

- `agentic-project-playbook` for repository-specific operating playbooks;
- `portable-authoring-protocol` for protocol extraction and migration;
- `cpp-game-sdk-coding-standard` for implementation-level C++ and CMake rules.

## Core model

Use roles, not tool assumptions:

1. **Planner**: converts the user goal into an executable contract.
2. **Executor**: completes one task at a time and records evidence.
3. **Reviewers**: independently verify compliance, quality, real QA, and scope.
4. **Recorder**: persists decisions, issues, evidence, and recovery notes.

## Non-negotiable rules

- Read before planning; reread before editing.
- Every task needs acceptance criteria and a real verification surface.
- Checkboxes are progress markers, not proof.
- Evidence must include commands or observed behavior.
- Background task IDs are not durable unless you persist them yourself.
- If a review rejects, fix the issue and rerun the relevant review.
- Keep portable workflow rules separate from project-specific bindings.

## Planner protocol

Produce a plan with:

1. goal, non-goals, and success criteria;
2. concrete deliverables;
3. explicit Must NOT list;
4. dependency graph and parallel waves;
5. per-task contracts with references, acceptance criteria, QA scenarios,
   evidence paths, and commit boundaries;
6. final review wave with required verdict formats;
7. session recovery steps for lost background tasks and interrupted launches.

## Executor protocol

For each task:

1. read the task contract and relevant files;
2. implement the smallest correct change;
3. run diagnostics on changed files;
4. run focused tests, then broader tests if risk requires;
5. use the real surface manually when applicable;
6. save evidence;
7. commit only intended files if the plan requires a commit;
8. mark the task complete only after evidence passes;
9. record reusable lessons in the notepad.

## Review protocol

Run independent reviewers for substantial plans:

- **Plan compliance**: must-haves and must-nots.
- **Quality**: build, format/lint, diagnostics, maintainability.
- **Real QA**: user-facing scenarios and edge cases.
- **Scope fidelity**: actual diff versus plan.

All reviewers must approve before the plan is complete.

## Session recovery protocol

When resuming work:

1. read the active plan and current state manifest;
2. read decisions, learnings, issues, and problems;
3. verify the last claimed task before proceeding;
4. collect current-session background results;
5. relaunch missing or expired background tasks;
6. inspect dirty worktree state;
7. continue from the first unchecked or rejected item.

## Output contract

When asked to create or revise this workflow, produce:

1. a portable methodology guide;
2. a short skill entrypoint;
3. a long reference file;
4. project-specific binding notes or a migration checklist;
5. verification that the files and links exist.

## Bundled files

- `README.md` explains package layout and copying.
- `references/plan-execute-verify-workflow-reference.md` contains the long-form
  method and templates.
