# c-style-api-design

A shareable skill package for designing or reviewing C-style APIs that are easy to bind into Lua, Python, C#, and JavaScript runtimes.

It focuses on the API shape that sits between internal C++ implementation and downstream binding layers.

---

## Package layout

```text
skills/c-style-api-design/
├── SKILL.md
└── references/
    ├── c-api-examples.h
    └── per-language-guidance.md
```

---

## What this skill is for

Use this skill for:

- designing a C ABI that can be wrapped cleanly by Lua/Python/C#/JS tooling;
- reviewing whether an existing API leaks C++-only semantics across the language boundary;
- defining opaque handles, error codes, callback contracts, buffer/string ownership, and versioning rules;
- reducing future binding complexity before implementing nanobind, pybind11, Cython, P/Invoke, Node-FFI, or Emscripten glue.

---

## What this skill is not for

Do not use this skill as the primary source for:

- broader C++17 SDK or native-library implementation standards;
- general CMake target design and packaging policy;
- Python wheel packaging, editable install, stub generation, or distribution workflow;
- repository-specific operating rules.

Prefer:

- `cpp-game-sdk-coding-standard` for broader C++17 SDK/native-library/CMake/ABI implementation rules;
- `cpp-python-bindings` for downstream Python binding, package layout, and wheel delivery;
- `team-ai-coding-governance` for team/repository AI coding governance, verification, docs, and git discipline.

---

## How it fits with adjacent skills

Typical sequence:

```text
internal C++ implementation
→ c-style-api-design
→ cpp-python-bindings / other runtime-specific binding work
```

Use this skill first when the main risk is API shape at the cross-language boundary.

---

## Bundled references

* `references/c-api-examples.h`
  Complete C ABI example covering opaque handles, error handling, callbacks, buffers, strings, and versioning.
* `references/per-language-guidance.md`
  Runtime-specific binding notes for Lua, Python, C#, and JavaScript.

---

## Verification after editing

* [ ] `SKILL.md` has valid YAML frontmatter.
* [ ] Folder name matches `c-style-api-design`.
* [ ] `name` in frontmatter matches the folder name.
* [ ] `metadata.source` points to `skills/c-style-api-design/SKILL.md`.
* [ ] README and SKILL agree on scope and exclusions.
* [ ] Adjacent skill boundaries are explicit.
* [ ] References listed in `SKILL.md` exist.
