# Bundled Config Files

This directory contains config files bundled with the `cpp-game-sdk-coding-standard` skill.

## Files

- `.clang-format` - formatting rules for C/C++ and related languages.
- `.editorconfig` - editor-neutral charset, indentation, whitespace, and line-ending rules.
- `.gitattributes` - Git text normalization and binary/LFS tracking rules.

## How to apply

For a new repository, copy the files to the repository root:

```text
<repo>/.clang-format
<repo>/.editorconfig
<repo>/.gitattributes
```

Before copying, compare them with any existing files in the target repository. Existing project-specific rules take precedence over these bundled defaults.

## Migration checks

- Confirm the indentation width matches the target team's code style.
- Confirm the formatter language sections match the languages used by the repository.
- Confirm line endings are compatible with platform scripts.
- Confirm Git LFS patterns match the target repository's asset and binary policy.
- Confirm generated directories, third-party binaries, and package artifacts are not accidentally tracked as text.
