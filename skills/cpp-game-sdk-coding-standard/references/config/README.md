# Bundled Config Files

This directory contains fallback config files bundled with `cpp-game-sdk-coding-standard`.

Files:

- `.clang-format` — C/C++ formatting defaults.
- `.editorconfig` — editor-neutral charset, indentation, whitespace, and line-ending rules.
- `.gitattributes` — Git text normalization and binary/LFS tracking defaults.

---

## Important

These files are defaults, not universal policy.

Before copying them into a repository:

1. check whether the target repository already has config files;
2. compare style and platform requirements;
3. confirm line-ending policy;
4. confirm Git LFS is installed and desired;
5. confirm binary, asset, and package artifact patterns;
6. avoid replacing existing project-specific rules unless explicitly requested.

---

## How to apply

For a new repository, copy files to the repository root:

```text
<repo>/.clang-format
<repo>/.editorconfig
<repo>/.gitattributes
````

For an existing repository, merge deliberately instead of blindly overwriting.

---

## Migration checks

* indentation width matches team style;
* column limit is acceptable;
* formatter language sections match repository languages;
* scripts use correct CRLF/LF policy;
* binary files are not treated as text;
* source files are normalized as text;
* Git LFS patterns match repository asset policy;
* generated directories and package artifacts are not accidentally tracked.
