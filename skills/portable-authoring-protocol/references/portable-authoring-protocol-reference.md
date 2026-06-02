# Portable Authoring Protocol for Code and Documentation

This document is a transplantable specification for engineering work. It is designed to be copied into other repositories and adapted with minimal changes.

It captures the **currently effective** constraints I am operating under when writing code and documentation in this repository, while clearly separating:

- rules that are broadly portable to other projects;
- rules that are project-specific and should be reconfigured after migration;
- the current user override that **documentation prose is not constrained by code style rules**, especially line length.

To make migration easier, this document is written as a protocol rather than as a GAP-only policy.

## 1. What This Protocol Covers

This protocol covers four things:

1. how to decide which constraint wins when rules conflict;
2. how code should be written, reviewed, and verified;
3. how documentation should be written and maintained;
4. how changes should be managed in git and in a shared working tree.

It is intended for AI-assisted engineering work, but most of it is also useful as a human team convention.

## 2. Constraint Precedence

When two rules conflict, use this order:

1. **Direct user instruction**
2. **Safety, integrity, and non-fabrication rules**
3. **Project-specific repository policy**
4. **This protocol's default behavior**

Examples:

- If the repository says "all docs must be English" but the user explicitly asks for a Chinese migration document, the user instruction wins.
- If the repository says "commit after every atomic point" but the active
  operating policy forbids commits without approval, do not commit until the
  user asks. If an active workflow rule requires verified auto-commit after
  completed work, follow that rule but stage only intended files.
- If a style guide says one thing but the real codebase consistently uses another pattern in the touched area, match the working code unless the user explicitly wants a broader cleanup.

## 3. Non-Negotiable Universal Rules

These are the rules that should survive migration to almost any project.

### 3.1 Read Before Changing

- Never speculate about code you have not read.
- If a user mentions a file, read it before discussing or editing it.
- If a change depends on callers, configuration, build targets, or related docs, inspect them first.

### 3.2 Prefer the Smallest Correct Change

- Fix the problem at the right level, but do not expand scope casually.
- Do not refactor unrelated code just because you are nearby.
- Prefer an explicit local solution over speculative abstraction.

### 3.3 No Fabrication

- Never invent build results, test results, QA results, or tool output.
- Never claim a file says something you did not read.
- Never claim a workflow works unless you actually drove it through the relevant surface in the current turn.

### 3.4 Verification Is Part of the Work

- A change is not done when the edit is written.
- It is done only after the change is verified through the surfaces that matter.

Typical verification stack:

- diagnostics / type checking on changed code;
- build;
- tests, when relevant;
- manual QA through the real surface.

### 3.5 Manual QA Through the Real Surface

Use the matching surface for the artifact:

- CLI / shell tool: run it and inspect the real output;
- API / service: hit it with a request or a driver script;
- library: write a minimal caller and execute it;
- documentation: read the final rendered markdown and verify discoverability, commands, file paths, and identifiers.

### 3.6 State Limits Explicitly

If something could not be verified, say exactly what was not verified and why.

Good:

- "The doc link was verified, but the CLI binary was not executed because the tool target was not built in this worktree."

Bad:

- "Should work."

## 4. Code Authoring Protocol

This section describes the default behavior for writing code.

## 4.1 Operating Loop

For any non-trivial task, use this loop:

1. Explore
2. Plan
3. Implement
4. Verify
5. Manually QA

The loop is short and practical. It is not a request for ceremony.

### Explore

- read the relevant files;
- search for existing patterns before inventing new ones;
- inspect examples, tests, and public headers when they define the real integration surface.

### Plan

- identify the files to touch;
- identify the exact behavior to change;
- identify what must be verified afterward.

### Implement

- match the style and architectural level of the surrounding code;
- prefer surgical edits;
- avoid unrelated cleanup.

### Verify

- run diagnostics, build, tests, and targeted searches as needed;
- verify every changed file with the cheapest reliable mechanism first;
- if the build or tests fail because of unrelated pre-existing issues, say so explicitly rather than hiding the problem.

### Manually QA

- use the deliverable as a real user would discover it;
- if the artifact is documentation, read the document itself and the navigation entry that should lead users to it.

## 4.2 Design Defaults for Code

These are the current default engineering preferences.

- Write the smallest correct change.
- Prefer root fixes over symptom patches when the root cause is clear and the scope stays reasonable.
- Do not add speculative fallbacks, retries, compatibility layers, or feature flags unless the problem truly requires them.
- Keep obvious single-use logic inline.
- Do not introduce helpers or abstractions just to make the code look more "architected".
- Preserve existing public behavior unless the user asked to change it.

## 4.3 Error-Handling Defaults

- Validate at real boundaries: user input, external files, network input, or untrusted data.
- Do not add defensive code for impossible states that are already guaranteed by surrounding contracts.
- Prefer explicit error reporting over silent swallowing.

## 4.4 Testing Defaults

Portable default:

- do not add tests automatically just to look complete;
- add or update tests when one of these is true:
  - the user asked for tests;
  - the change fixes a subtle bug;
  - the change protects an important behavioral boundary.

Project-specific overrides may require stronger test discipline. If the repository already has an established test suite and local verification workflow, run the relevant tests before declaring completion.

## 4.5 Code Style: Portable Rule vs Project Rule

Portable rule:

- code must match the active project's style, naming, and architectural conventions.

This protocol does **not** force one universal code style across all repositories. Instead, it requires strict style consistency **within** the current project.

That means these items should be configured per project:

- language version (`C++17`, `C++20`, Rust edition, TypeScript target, etc.);
- naming style;
- line width for code;
- header / import ordering;
- documentation style for public APIs;
- ownership and concurrency idioms.

## 5. Documentation Authoring Protocol

This section describes the currently effective rules for writing docs.

## 5.1 Documentation Prose Is Not Code

Current effective override:

- **documentation prose is not constrained by code style rules**;
- **documentation prose is not bound by code line-width limits**;
- specifically, there is **no requirement** to wrap prose at 100 characters just because the code style says 100 columns.

This override applies to:

- explanatory prose;
- guides;
- architecture notes;
- migration notes;
- checklists;
- narrative sections of markdown documents.

It does **not** mean documentation can be sloppy.

## 5.2 Documentation Must Still Be Exact

Even when prose style is flexible, documentation must remain precise.

Required:

- exact file paths;
- exact type names and identifiers;
- exact command names and flags;
- statements that match the real implementation, examples, or build system.

If a command in old documentation is stale but the actual tool entrypoint says otherwise, use the real tool entrypoint as the source of truth.

## 5.3 Documentation Code Examples Must Be Semantically Correct

Documentation prose may ignore code-style formatting constraints, but code examples must still:

- match the current API surface;
- respect the language level actually used by the project;
- avoid pseudo-code that pretends to compile when it does not.

Example:

- in a `C++17` project, do not use a `C++20` designated initializer in a "copy-paste" setup example unless the example is clearly labeled as pseudo-code.

## 5.4 Documentation Update Strategy

Default behavior:

- update existing docs surgically when the task is a targeted correction;
- write a new doc when the new content has a distinct audience or purpose;
- do not rewrite large documents unless the user explicitly wants a rewrite.

Good reasons to create a new doc:

- a new audience exists (for example, user guide vs architecture reference);
- the content is portable and should survive transplant to another project;
- adding the content to an existing doc would make that doc unclear.

## 5.5 Language Policy for Docs

Portable default:

- documentation language is configurable per project and per user request.

Current effective behavior:

- if the user explicitly wants a document in a particular language, that request wins;
- if the repository has a strict documentation language policy and the user did not override it, follow the repository.

## 5.6 Recommended Documentation Quality Checks

For any new or changed document, verify at least:

- the document reads coherently from top to bottom;
- links point to real files;
- commands match actual binaries or build targets;
- code snippets are consistent with the current public API;
- the doc is discoverable from the expected hub or index page when appropriate.

## 6. Git and Change-Management Protocol

These rules are highly portable.

### 6.1 Commit Discipline

Current effective rule:

- Commit only when the user explicitly asks, or when an applicable repository or
  session workflow rule requires verified auto-commit after completed work.

This rule is stronger than repository habits like "commit every atomic step"
because it protects the user's control over history while still allowing an
explicit auto-commit policy to apply when it is active. In all cases, inspect
`git status`, inspect the intended diff, and stage only files that belong to the
completed work.

### 6.2 Destructive Git Operations

Never do these without explicit approval:

- hard reset;
- force push;
- checkout/restore that discards someone else's work;
- history rewrite operations that could destroy context.

### 6.3 Dirty Worktree Discipline

- assume the worktree may contain other people's changes;
- do not revert unrelated edits just to get a clean diff;
- work around unrelated modifications when possible;
- if unrelated changes block the task directly, ask one precise question.

### 6.4 Commit Scope

- do not stage build artifacts, editor caches, or local scratch files unless the user explicitly wants them versioned;
- do not silently broaden the commit to unrelated changes;
- if the worktree contains unrelated modifications, either leave them alone or call them out clearly.

## 7. AI-Assisted Execution Discipline

This section is useful when migrating the protocol to another AI-assisted project.

## 7.1 Investigate Before Acting

- do not start coding from memory when the file can be read;
- do not answer architecture questions from guesses;
- inspect examples, tests, and public surfaces before deciding how users are expected to integrate.

## 7.2 Parallelize Independent Context Gathering

- independent reads, searches, and diagnostics should happen in parallel;
- do not serialize unrelated searches when tools allow batching.

## 7.3 Use Task Tracking for Non-Trivial Work

- if the task has multiple meaningful steps, track them explicitly;
- keep exactly one active step in progress at a time.

## 7.4 Consult Specialists When Complexity Is Real

Examples:

- use architecture/debugging consultation for hard design tradeoffs;
- use external-doc research for unfamiliar packages or framework behavior;
- use focused codebase search for broad pattern discovery.

Do not escalate trivial work just to look thorough.

## 7.5 No Duplicate Exploration

- once a background search or specialist task is gathering a class of facts, do not duplicate the same search locally unless the original result was insufficient.

## 8. GAP-Specific Current Bindings

This section records how the portable protocol is currently bound in this repository.

These are **project-specific** and should be reviewed before transplanting elsewhere.

### 8.1 Current Code Constraints in GAP

- language: `C++17`
- build system: `CMake`
- code style: Google C++ Style Guide
- code line width: 100 columns
- naming:
  - classes / enums / methods: `PascalCase`
  - variables / parameters / locals: `camelCase`
  - private members: trailing underscore
- encoding: UTF-8
- ownership: RAII first, no raw owning pointers in public APIs
- concurrency: `std::shared_mutex` for read-heavy state, `std::atomic` for flags / counters where appropriate
- exceptions: prohibited
- public headers: Doxygen required
- library code logging: use project logging, not `std::cout` / `printf`

### 8.2 Current Documentation Constraints in GAP

Repository-level defaults historically say:

- docs should be English;
- doc updates should be surgical;
- public API docs should use Doxygen where relevant.

Current effective override from the user:

- documentation prose is **not** constrained by the code style guide;
- documentation prose is **not** constrained by the 100-column rule;
- documentation should optimize for clarity and portability rather than prose formatting uniformity.

### 8.3 Current Verification Expectations in GAP

- changed code should be validated with diagnostics where supported;
- build and relevant tests should be run when the task affects code behavior;
- the artifact should be exercised through the real user-facing surface whenever feasible.

### 8.4 Current Git Expectations in GAP

Even though some repository docs describe an atomic-commit cadence, the active
session policy may be stricter or may require verified auto-commit after
completed work. Resolve this through precedence:

- direct user instructions and active session workflow rules decide whether a
  commit is allowed or required;
- commits must be atomic and limited to intended files;
- local/session artifacts such as `.sisyphus/**`, `.remember/**`, generated
  evidence logs, `gui_module.md`, and `imgui.ini` stay out of normal commits.

## 9. Migration Checklist for Another Project

When moving this protocol to a new repository, update these fields first:

### Required Project Bindings

- primary programming language(s)
- language version(s)
- build system and canonical commands
- code style and naming convention
- error-handling policy
- concurrency policy
- testing framework and minimum verification bar
- documentation language policy
- documentation line-width policy for prose
- public API documentation expectations
- commit policy
- allowed / forbidden git operations

### Recommended One-Page Project Header

When transplanting, fill in a small header like this at the top of the copied file:

```text
Project Name:
Primary Languages:
Build System:
Code Style:
Documentation Language:
Documentation Prose Line Limit:
Public API Doc Standard:
Testing Standard:
Commit Policy:
Manual QA Requirement:
Special Safety Constraints:
```

That makes the portable protocol immediately usable in the new repository.

## 10. Short Version

If you only keep ten rules from this protocol, keep these:

1. Read before changing.
2. Match the active project's conventions.
3. Prefer the smallest correct fix.
4. Do not fabricate anything.
5. Verify through the real surface.
6. State what was not verified.
7. Do not commit unless the user asks.
8. Do not destroy unrelated work.
9. Documentation prose does not need to obey code formatting rules.
10. Documentation examples must still be technically correct.
