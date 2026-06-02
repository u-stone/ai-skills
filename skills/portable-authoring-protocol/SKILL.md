---
name: portable-authoring-protocol
description: Use when extracting repository conventions into a reusable engineering protocol, separating portable rules from project-local bindings, or reviewing whether a team standard is internally consistent and migration-ready.
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: engineering-governance
  source: .opencode/skills/portable-authoring-protocol/references/portable-authoring-protocol-reference.md
---

# Portable Authoring Protocol

## What I do

- Convert repository-specific engineering rules into a reusable authoring protocol.
- Help teams define consistent expectations for code writing, documentation writing, verification, and git behavior.
- Keep **portable defaults** separate from **project-specific bindings**.
- Use that separation so the result can be copied into other repositories with minimal rewriting.
- Documentation prose rules must be treated as distinct from code formatting rules unless explicitly stated otherwise.

## When to use me

Use this skill when the task involves any of the following:

- extracting local repository rules into a reusable team protocol;
- separating portable engineering rules from project-specific bindings;
- auditing whether a written protocol is internally consistent and migration-ready;
- porting code-writing, documentation, verification, and git rules to another repository;
- rewriting an existing project memo into a reusable cross-project standard.

Typical triggers:

- "turn these repo rules into a reusable team skill"
- "extract our engineering protocol from this repo"
- "separate portable rules from local bindings"
- "port our engineering standard to another repo"
- "audit whether this protocol is reusable and internally consistent"
- "rewrite this repository's rules as a portable standard"

## Scope boundary

This skill is for **protocol extraction and migration**.

Use it to:

- derive a reusable engineering standard from local rules;
- define the split between portable defaults and project bindings;
- review or rewrite protocols so they can travel between repositories.

Do **not** use it as the primary skill for:

- defining how one specific repository should operate day to day;
- writing a project startup / maintenance playbook;
- running the plan-execute-verify loop for one implementation task.

For those cases, prefer:

- `agentic-project-playbook` for repository-specific operating playbooks;
- `plan-execute-verify-workflow` for execution methodology;
- `cpp-game-sdk-coding-standard` for implementation-level C++ and CMake rules.

## Core operating model

Always structure the result in three layers:

1. **Constraint precedence**
2. **Portable authoring rules**
3. **Project-specific bindings**

Do not flatten these layers together. A protocol that mixes hard universal rules with repository-local preferences becomes much harder to transplant.

## Required output shape

When using this skill to write or revise a team protocol, keep the output in these grouped sections unless the user explicitly wants a shorter format:

1. Purpose and scope
2. Constraint precedence and non-negotiable universal rules
3. Authoring protocol: code, documentation prose, and code examples in docs
4. Execution protocol: verification, QA, git behavior, and AI-assisted work discipline
5. Project-specific bindings and migration checklist

## Non-negotiable principles

Preserve these principles unless the user explicitly overrides them:

- Read before changing.
- Prefer the smallest correct change.
- Never fabricate code behavior, test results, or tool output.
- Verification is part of the work, not a postscript.
- Manual QA should use the real user-facing surface whenever feasible.
- State clearly what was not verified and why.
- Do not let documentation prose inherit code formatting rules by accident.

## Important distinction: code rules vs documentation rules

When building a protocol, explicitly separate:

- rules for **source code**;
- rules for **documentation prose**;
- rules for **code examples inside documentation**.

Recommended stance:

- Code must follow project style rules.
- Documentation prose should optimize for clarity, structure, and accuracy.
- Documentation code examples must still be technically correct and consistent with the actual API and language level.

## How to migrate the protocol to another project

When transplanting, keep the portable core and replace the bindings.

Always ask or determine these project-local values:

- primary language and version;
- build system and canonical commands;
- style guide and naming convention;
- test framework and verification bar;
- documentation language policy;
- documentation prose formatting policy;
- public API documentation standard;
- commit policy and destructive git restrictions.

## Recommended workflow when applying this skill

1. Read the repository's current rule sources.
2. Identify contradictions between historical docs and current effective behavior.
3. Resolve precedence explicitly.
4. Write the portable core first.
5. Add project-specific bindings second.
6. Add a migration checklist last.
7. Verify the resulting protocol by reading it end-to-end and checking any linked navigation entry.

## Bundled references

- `references/portable-authoring-protocol-reference.md` - the full long-form reference version of this protocol.
- `README.md` - team-facing packaging and copy instructions.

## Assumptions

- The team wants a protocol that is reusable, not a one-off project memo.
- The resulting skill should be safe to copy into another repository with minimal edits.
- The protocol should describe both human and AI-assisted engineering workflows.
