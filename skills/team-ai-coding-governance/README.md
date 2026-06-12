# team-ai-coding-governance

A shareable OpenCode skill package for team-wide AI-assisted coding governance.

It replaces the previous split between:

- `agentic-project-playbook`
- `portable-authoring-protocol`

The new skill is language-neutral by default and is meant to be used across projects and teams. It defines how AI agents should start coding work, decide source-of-truth precedence, add tests/examples/docs, verify no-warning/no-error builds, and keep git history clean.

---

## Package layout

```text
team-ai-coding-governance/
├── SKILL.md
├── README.md
├── references/
│   └── team-ai-coding-governance-reference.md
└── evals/
    └── evals.json
```

---

## What this skill is for

Use this skill for:

- new module creation;
- code changes by AI agents;
- deciding whether unit tests, examples, and docs are required;
- enforcing warning/error-free first-party builds;
- requiring examples and tests to run without crash or unhandled exception;
- initializing and maintaining git history for AI-assisted code;
- documenting module architecture, implementation details, algorithms, and third-party libraries;
- defining repository-local source-of-truth maps and binding manifests.

---

## C/C++ association

This skill does not duplicate C/C++ implementation rules.

For C, C++, CMake, native library, SDK, public header, exported symbol, static/shared library, plugin, or GoogleTest work, also use:

```text
cpp-game-sdk-coding-standard
```

That skill owns C++ naming, formatting, CMake, public header/export, ownership, lifetime, threading, performance, and native packaging rules.

---

## What this skill does not replace

- `cpp-game-sdk-coding-standard` for C/C++/CMake/native SDK implementation rules.
- `c-style-api-design` for cross-language C-style API design for scripting bindings.
- `plan-execute-verify-workflow` for complex planner/executor/reviewer task execution.
- Skill creation or skill-audit workflows.

---

## How to use

Install the package under the skills directory used by the host environment.

Minimum skill entrypoint:

```text
team-ai-coding-governance/SKILL.md
```

Example prompts:

- "Use team-ai-coding-governance for this new module."
- "Create a new module and make sure tests, examples, docs, build, and git are handled."
- "Standardize our AI-assisted coding workflow for this repository."
- "Before changing this C++ library, apply team governance and the C++ coding standard."

---

## What to customize after copying

Replace repository-specific bindings:

- primary languages and versions;
- canonical configure/build/test/lint/format commands;
- unit-test framework and example runner;
- documentation folder and docs hub;
- warning policy and third-party warning handling;
- generated/intermediate/local artifact exclusions;
- commit message style;
- required language-specific skills;
- manual QA surfaces.

Keep portable governance rules separate from project-specific values.

---

## Verification after editing

- [ ] `SKILL.md` has valid YAML frontmatter.
- [ ] Folder name matches `team-ai-coding-governance`.
- [ ] `metadata.source` points to the bundled reference.
- [ ] README and reference agree with the entrypoint.
- [ ] Old skill names are not used as active recommendations.
- [ ] C/C++ work routes to `cpp-game-sdk-coding-standard` without duplicating its rules.
- [ ] Unit-test, example, docs, build, and git requirements remain explicit.
