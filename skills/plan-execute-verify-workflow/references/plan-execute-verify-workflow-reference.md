# Plan Execute Verify Workflow Reference

This reference describes a portable method for running complex AI-assisted
software work. It is based on lessons from `.sisyphus` execution records, but it
does not require `.sisyphus`, Oh My OpenCode, Prometheus, or Atlas.

## 1. Roles

### Planner

The planner converts a user goal into a task contract. A good planner is
skeptical: it reads the repository, identifies hidden dependencies, and writes
acceptance criteria that can be verified by commands or real user behavior.

Planner responsibilities:

- define the goal and non-goals;
- list deliverables and prohibited changes;
- map dependencies and parallel waves;
- define evidence for each task;
- define final review gates;
- include recovery instructions.

### Executor

The executor performs the work. It owns the final result even when it delegates
search or review to other agents.

Executor responsibilities:

- read the task contract and relevant files;
- edit surgically;
- run diagnostics and tests;
- manually exercise the correct surface;
- save evidence;
- commit only intended files when required;
- update task state after verification.

### Reviewers

Reviewers are independent checks against self-confirmation.

Recommended reviewer set:

1. plan compliance;
2. quality and maintainability;
3. real QA;
4. scope fidelity.

### Recorder

The recorder can be a file, database, issue tracker, or wiki. It must persist:

- plan state;
- decisions;
- issues and blockers;
- reusable learnings;
- evidence artifacts;
- background task IDs or replacement runs.

## 2. Planner Template

```markdown
# Plan: <name>

## Goal
Observable user-facing outcome.

## Non-goals / Must NOT
- prohibited compatibility paths
- prohibited files or layers
- prohibited broad refactors

## Deliverables
- file/API/doc/test/example output

## Dependency Graph
- T1 blocks T2
- T3 can run in parallel with T4

## Execution Waves
- Wave 1: T1, T2
- Wave 2: T3
- Final: F1-F4 reviewers

## Tasks
- [ ] T1. Title
  What to do:
  - exact changes
  Must NOT do:
  - explicit constraints
  Acceptance Criteria:
  - command or behavior checks
  QA Scenarios:
  - surface, steps, expected result, evidence path
  Commit:
  - intended files and message

## Final Review
- F1 Plan Compliance
- F2 Quality
- F3 Real QA
- F4 Scope Fidelity

## Recovery
- where state is recorded
- what to do if background IDs are lost
- what to do if a reviewer rejects
```

## 3. Executor Loop

Use this loop for every task:

1. Read the task and relevant history.
2. Read files before changing them.
3. Make the smallest correct edit.
4. Run local diagnostics on changed files.
5. Run focused verification.
6. Run broader verification when the change crosses module boundaries.
7. Use the real surface manually.
8. Save evidence.
9. Inspect the diff.
10. Commit intended files only if required.
11. Mark task state complete.
12. Record reusable learnings.

## 4. Evidence Design

Evidence must answer: "What exactly proved this task works?"

Good evidence examples:

- focused unit test output;
- full test suite summary;
- build log with exit code;
- format/lint output;
- grep output proving required strings exist or forbidden strings are absent;
- CLI transcript;
- HTTP response;
- browser screenshot or console log;
- reviewer verdict.

Evidence should include:

- command or surface used;
- timestamp if available;
- exact pass/fail result;
- short explanation if the command has expected non-zero output;
- links or paths to related files.

## 5. Final Review Gates

Final review catches errors that tests miss.

### F1 Plan Compliance

Checks that every deliverable exists and every Must NOT rule holds.

Verdict format:

```text
Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT
```

### F2 Quality Review

Checks build, diagnostics, formatting, maintainability, security, and style.

Verdict format:

```text
Build [PASS/FAIL] | Tests [N pass/N fail] | Files [N clean/N issues] | VERDICT
```

### F3 Real QA

Runs the user-facing surface and important edge cases.

Verdict format:

```text
Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT
```

### F4 Scope Fidelity

Compares the actual diff to the plan.

Verdict format:

```text
Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT
```

## 6. Recovery Rules

### Lost Background Task IDs

If a background ID cannot be retrieved:

1. record the loss;
2. do not assume success;
3. relaunch the task;
4. collect the new result;
5. update the notepad with the prevention rule.

### Interrupted Parallel Launch

If a batch launch is interrupted:

1. list intended tasks;
2. list returned IDs;
3. relaunch missing tasks;
4. cap future launch batches;
5. avoid ending the session until all critical IDs are collected or persisted.

### Reviewer Rejection

If any reviewer rejects:

1. classify each finding as real, false positive, or out of scope;
2. fix real issues;
3. document false positives with evidence;
4. rerun the rejecting reviewer or the relevant focused checks;
5. present consolidated results only after all reviewers approve.

## 7. Common Failure Modes and Controls

| Failure mode | Control |
|---|---|
| Helper-level test replaces surface-level test | Require QA surface in task contract |
| Raw grep false positive | Read file context before rejecting |
| Checkbox not updated | Reread plan after marking complete |
| Background ID lost across session | Persist IDs and relaunch missing tasks |
| Parallel launch partially interrupted | Cap batches and count returned IDs |
| Dirty worktree contamination | Stage intended files only |
| Fixture missing new runtime metadata | Add fixture validation and document required fields |
| Lock held across callback | Include concurrency constraints in plan and review |

## 8. Portable Implementation Without Plugins

You can implement this workflow with simple files:

```text
project/
  plans/<plan-name>.md
  notepads/<plan-name>/decisions.md
  notepads/<plan-name>/issues.md
  notepads/<plan-name>/learnings.md
  notepads/<plan-name>/problems.md
  evidence/<plan-name>/...
  state/<plan-name>.json
```

Minimum state JSON:

```json
{
  "active_plan": "plans/example.md",
  "sessions": ["session-1"],
  "background_tasks": {
    "F1": "task-id-or-null"
  },
  "last_verified_task": "T4"
}
```

The tools can vary. The invariants should not:

- plan before execution;
- evidence before completion;
- review before closure;
- recovery before continuation;
- project bindings separated from portable workflow rules.

## 9. Migration Checklist

For each new repository, define:

- where plans live;
- where evidence lives;
- where session state lives;
- canonical build/test/lint commands;
- manual QA surface per artifact type;
- commit policy;
- reviewer roles;
- forbidden scope creep patterns;
- generated files and local artifacts to exclude.

Then run one pilot task and update the workflow with any local lessons before
using it for a large project.
