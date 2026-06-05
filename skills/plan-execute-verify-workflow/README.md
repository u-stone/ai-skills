# plan-execute-verify-workflow

A portable OpenCode skill package for reliable AI-assisted work using planning, bounded execution, evidence, recovery, and targeted review.

It is designed to avoid two common failure modes:

1. ad-hoc implementation with no verification;
2. heavyweight workflow bureaucracy for tasks that should stay lightweight.

Default to Lite mode. Escalate only when the task risk justifies it.

---

## Package layout

```text
.opencode/skills/plan-execute-verify-workflow/
├── SKILL.md
├── README.md
└── references/
    └── plan-execute-verify-workflow-reference.md
```

Minimum required file:

```text
.opencode/skills/plan-execute-verify-workflow/SKILL.md
```

Recommended copy is the whole folder so the long reference stays available.

---

## What this skill is for

Use this skill to:

* convert a complex user goal into an executable plan;
* execute one verified task at a time;
* keep work recoverable across sessions;
* preserve evidence for completed work;
* prevent hidden scope creep;
* run targeted independent review before closure.

---

## What this skill is not for

Do not use it as the primary skill for:

* tiny direct edits;
* repository-wide coding standards;
* language-specific implementation rules;
* extracting reusable methodology from one project;
* quick explanations or Q&A.

Prefer specialized skills for those cases.

---

## Workflow modes

| Mode     | Use when                                                          | Review level                 | Recovery level          |
| -------- | ----------------------------------------------------------------- | ---------------------------- | ----------------------- |
| Lite     | localized, low-risk work                                          | none or self-check           | minimal                 |
| Standard | medium multi-file work                                            | one focused review if needed | compact state           |
| Critical | high-risk, multi-session, migration, infra, security, concurrency | targeted reviewers           | snapshot-first recovery |

Use the lightest mode that is safe.

---

## Core artifacts

### Compact state

A short resume pointer for active work.

```json
{
  "plan_id": "",
  "mode": "standard",
  "active_task": "T2",
  "completed_tasks": ["T1"],
  "blocked_tasks": [],
  "pending_reviews": [],
  "last_verified_task": "T1",
  "next_action": "continue T2"
}
```

### Structured evidence

A compact proof record.

```json
{
  "task_id": "T1",
  "type": "test",
  "command_or_surface": "npm test -- auth",
  "result": "pass",
  "summary": "Auth tests passed.",
  "artifacts": []
}
```

### Shared review manifest

A reviewer input summary that prevents repeated full-context reads.

```json
{
  "plan_summary": {},
  "diff_summary": {},
  "evidence_summary": {},
  "risk_summary": {},
  "review_requests": {}
}
```

---

## Recommended repository bindings

When copying this skill into a repository, define:

* where plans live;
* where compact state lives;
* where evidence lives;
* canonical build/test/lint commands;
* manual QA surfaces;
* commit policy;
* reviewer roles;
* generated files that must not be committed;
* local artifacts that must be ignored.

Example layout:

```text
plans/
state/
evidence/
notepads/
```

---

## Migration checklist

After copying:

* [ ] Folder name matches `plan-execute-verify-workflow`.
* [ ] `SKILL.md` has valid YAML frontmatter.
* [ ] Reference path in metadata exists.
* [ ] Repository-specific build/test/lint commands are documented.
* [ ] Evidence and state locations are defined.
* [ ] Commit policy is defined.
* [ ] Generated/local files are excluded from commits.
* [ ] One pilot task has been run in Lite or Standard mode.

---

## Verification checklist

After editing this package:

* [ ] `SKILL.md` remains short and operational.
* [ ] Long examples stay in the reference file.
* [ ] Workflow modes remain clear.
* [ ] Retry budget exists.
* [ ] Recovery starts from compact state.
* [ ] Reviewers consume shared manifests before raw context.
* [ ] Evidence remains structured and compact.
