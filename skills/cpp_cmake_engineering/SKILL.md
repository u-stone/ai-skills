---
name: cpp_cmake_engineering
description: Add complete engineering infrastructure to an existing C++ CMake project (C++17, cross-platform macOS/Linux/Windows), including: GitHub Actions CI/CD, code quality tools, modern CMake build configuration, and open-source community files.
---

# C++ CMake Project Engineering Infrastructure Setup

## Environment Prerequisites

### macOS

```bash
# Build tools
brew install cmake ninja

# Code quality tools (clang-tidy/clang-format require LLVM — the bundled Apple Clang version is limited)
brew install llvm
# Add LLVM toolchain to PATH (Homebrew does NOT override system tools automatically)
echo 'export PATH="/usr/local/opt/llvm/bin:$PATH"' >> ~/.zshrc   # Intel Mac
# echo 'export PATH="/opt/homebrew/opt/llvm/bin:$PATH"' >> ~/.zshrc  # Apple Silicon
source ~/.zshrc
# Verify — should show LLVM/Clang version, NOT Apple clang
clang-tidy --version

# Coverage tool
brew install lcov
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y cmake ninja-build clang clang-tidy clang-format lcov
```

### Windows

- Install CMake 3.15+, Visual Studio 2019+ (with Clang tools) or LLVM
- Ninja: `winget install Ninja-build.Ninja`
- lcov is not natively supported on Windows — use WSL or skip the coverage preset

---

## Platform Limitations at a Glance

| Feature | macOS | Linux | Windows |
|---------|-------|-------|---------|
| AddressSanitizer (`asan`) | ✅ | ✅ | ❌ |
| LeakSanitizer (`lsan`) | ❌ Not supported | ✅ | ❌ |
| UBSanitizer (`ubsan`) | ✅ | ✅ | ❌ |
| lcov code coverage | ✅ (requires `.lcovrc` for 2.x compatibility) | ✅ | ❌ |
| clang-tidy | ✅ (requires `brew install llvm`) | ✅ | ✅ |
| clang-format | ✅ (requires `brew install llvm`) | ✅ | ✅ |
| GitHub Actions CI | ✅ | ✅ | ✅ |

---

## Files to Create

```
<project-root>/
├── LICENSE                                  # MIT License
├── CONTRIBUTING.md                          # Contribution guide
├── SECURITY.md                              # Security vulnerability reporting policy
├── CODE_OF_CONDUCT.md                       # Code of conduct
├── CMakePresets.json                        # Modernized build presets
├── .clang-format                            # Code formatting rules
├── .clang-tidy                              # Static analysis configuration
├── .lcovrc                                  # lcov 2.x compatibility config
├── cmake/
│   └── <ProjectName>Config.cmake.in        # find_package support
└── .github/
    ├── workflows/
    │   ├── ci.yml                           # Continuous integration
    │   └── release.yml                      # Automated release
    ├── dependabot.yml                        # Dependency auto-updates
    ├── pull_request_template.md             # PR template
    └── ISSUE_TEMPLATE/
        ├── bug_report.md                    # Bug report template
        └── feature_request.md               # Feature request template
```

Also modify:
- `CMakeLists.txt` — add install targets, CPack, compile_commands
- `README.md` — add CI badge and License section

---

## File Templates

### 1. `LICENSE` (MIT)

```
MIT License

Copyright (c) <YEAR> <PROJECT_NAME> Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### 2. `CMakePresets.json`

⚠️ **Critical platform notes:**
- The `asan` preset does **NOT** include `-fsanitize=leak` because macOS/Apple Clang does not support LeakSanitizer
- The `lsan` preset includes LeakSanitizer and is **Linux only**
- All presets use the Ninja generator — install Ninja before use

```json
{
  "version": 3,
  "configurePresets": [
    {
      "name": "base",
      "hidden": true,
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
      }
    },
    {
      "name": "debug",
      "displayName": "Debug",
      "inherits": "base",
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Debug" }
    },
    {
      "name": "release",
      "displayName": "Release",
      "inherits": "base",
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Release" }
    },
    {
      "name": "ci",
      "displayName": "CI (RelWithDebInfo)",
      "inherits": "base",
      "cacheVariables": { "CMAKE_BUILD_TYPE": "RelWithDebInfo" }
    },
    {
      "name": "asan",
      "displayName": "AddressSanitizer (macOS + Linux)",
      "inherits": "debug",
      "cacheVariables": {
        "CMAKE_CXX_FLAGS": "-fsanitize=address -fno-omit-frame-pointer",
        "CMAKE_EXE_LINKER_FLAGS": "-fsanitize=address"
      }
    },
    {
      "name": "lsan",
      "displayName": "LeakSanitizer (Linux only)",
      "inherits": "debug",
      "cacheVariables": {
        "CMAKE_CXX_FLAGS": "-fsanitize=address,leak -fno-omit-frame-pointer",
        "CMAKE_EXE_LINKER_FLAGS": "-fsanitize=address,leak"
      }
    },
    {
      "name": "ubsan",
      "displayName": "UndefinedBehaviorSanitizer",
      "inherits": "debug",
      "cacheVariables": {
        "CMAKE_CXX_FLAGS": "-fsanitize=undefined -fno-omit-frame-pointer",
        "CMAKE_EXE_LINKER_FLAGS": "-fsanitize=undefined"
      }
    },
    {
      "name": "coverage",
      "displayName": "Code Coverage",
      "inherits": "debug",
      "cacheVariables": {
        "CMAKE_CXX_FLAGS": "--coverage",
        "CMAKE_EXE_LINKER_FLAGS": "--coverage"
      }
    }
  ],
  "buildPresets": [
    { "name": "debug",    "configurePreset": "debug" },
    { "name": "release",  "configurePreset": "release" },
    { "name": "ci",       "configurePreset": "ci" },
    { "name": "asan",     "configurePreset": "asan" },
    { "name": "lsan",     "configurePreset": "lsan" },
    { "name": "ubsan",    "configurePreset": "ubsan" },
    { "name": "coverage", "configurePreset": "coverage" }
  ],
  "testPresets": [
    {
      "name": "default",
      "configurePreset": "debug",
      "output": { "outputOnFailure": true }
    },
    {
      "name": "ci",
      "configurePreset": "ci",
      "output": { "outputOnFailure": true },
      "execution": { "jobs": 4 }
    }
  ]
}
```

---

### 3. Additions to `CMakeLists.txt`

Append to the end of your existing `CMakeLists.txt`, replacing `<ProjectName>`, `<lib>`, and `<namespace>` with actual values:

```cmake
# ── Add after project() at the top of the file ─────────────────────────────
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# ── target_include_directories must use generator expressions for install ───
# Change existing:
#   target_include_directories(<lib> PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
# To:
target_include_directories(<lib> PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

# ── Append to the end of the file ──────────────────────────────────────────
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

install(TARGETS <lib>
    EXPORT <ProjectName>Targets
    LIBRARY  DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE  DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME  DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(DIRECTORY include/<namespace>
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(EXPORT <ProjectName>Targets
    FILE <ProjectName>Targets.cmake
    NAMESPACE <ProjectName>::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/<ProjectName>
)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/<ProjectName>Config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/<ProjectName>Config.cmake"
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/<ProjectName>
)

write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/<ProjectName>ConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/<ProjectName>Config.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/<ProjectName>ConfigVersion.cmake"
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/<ProjectName>
)

set(CPACK_PACKAGE_NAME "<ProjectName>")
set(CPACK_PACKAGE_VERSION ${PROJECT_VERSION})
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE")
set(CPACK_RESOURCE_FILE_README  "${CMAKE_CURRENT_SOURCE_DIR}/README.md")
include(CPack)
```

---

### 4. `cmake/<ProjectName>Config.cmake.in`

```cmake
@PACKAGE_INIT@

include("${CMAKE_CURRENT_LIST_DIR}/<ProjectName>Targets.cmake")
check_required_components(<ProjectName>)
```

---

### 5. `.clang-format`

```yaml
---
BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 100
AccessModifierOffset: -4
AlignConsecutiveAssignments: false
AlignConsecutiveDeclarations: false
AllowShortFunctionsOnASingleLine: Inline
AllowShortIfStatementsOnASingleLine: false
AlwaysBreakTemplateDeclarations: Yes
BraceWrapping:
  AfterClass: false
  AfterFunction: false
  AfterNamespace: false
BreakBeforeBraces: Attach
IncludeBlocks: Regroup
NamespaceIndentation: None
PointerAlignment: Left
SortIncludes: CaseSensitive
SpaceAfterCStyleCast: false
SpaceBeforeParens: ControlStatements
Standard: c++17
```

---

### 6. `.clang-tidy`

```yaml
---
Checks: >
  clang-diagnostic-*,
  clang-analyzer-*,
  cppcoreguidelines-*,
  modernize-*,
  performance-*,
  readability-*,
  bugprone-*,
  -modernize-use-trailing-return-type,
  -cppcoreguidelines-avoid-magic-numbers,
  -readability-magic-numbers,
  -cppcoreguidelines-pro-bounds-pointer-arithmetic
WarningsAsErrors: ''
HeaderFilterRegex: 'include/<namespace>/.*'
FormatStyle: file
CheckOptions:
  - key: readability-identifier-naming.ClassCase
    value: CamelCase
  - key: readability-identifier-naming.FunctionCase
    value: camelCase
  - key: readability-identifier-naming.VariableCase
    value: camelCase
  - key: readability-identifier-naming.MemberCase
    value: camelCase
  - key: readability-identifier-naming.ParameterCase
    value: camelCase
```

⚠️ **macOS setup required before running clang-tidy:**
```bash
# Must use the Homebrew LLVM toolchain, NOT the Apple-bundled one
brew install llvm
export PATH="/usr/local/opt/llvm/bin:$PATH"   # Intel Mac
# export PATH="/opt/homebrew/opt/llvm/bin:$PATH"  # Apple Silicon

# Verify — should NOT say "Apple clang"
clang-tidy --version

# Generate compile_commands.json (required by clang-tidy)
cmake --preset debug
ln -sf build/debug/compile_commands.json compile_commands.json

# Run analysis
run-clang-tidy -p build/debug 'src/.*\.cpp'
```

---

### 7. `.lcovrc`

⚠️ **lcov 2.x produces multiple compatibility errors with Apple Clang.** This file suppresses them all:
- `inconsistent`: compiler-generated functions (destructors/lambdas) have no corresponding line data
- `unsupported`: Apple Clang's gcov does not support function begin/end line features (requires GCC 9+)
- `corrupt`: cascades from an unhandled `inconsistent` error
- `category`: unknown coverage data category in Apple Clang system headers

```ini
# lcov/genhtml configuration
# Disable function end-line derivation (lcov)
derive_function_end_line = 0
# Disable strict data consistency checks (genhtml)
check_data_consistency = 0
# Suppress Apple Clang / lcov 2.x compatibility errors
ignore_errors = inconsistent,unsupported,corrupt,category
```

**Usage** — lcov does NOT auto-load `.lcovrc` from the project directory; you must specify it explicitly or copy it to your home directory:
```bash
# Option A: specify per command (recommended for project-level use)
lcov    --config-file .lcovrc --capture --directory . --output-file coverage.info
genhtml --config-file .lcovrc coverage.info --output-directory coverage_html

# Option B: global — set once, applies everywhere
cp .lcovrc ~/.lcovrc
```

---

### 8. `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    name: ${{ matrix.os }} / ${{ matrix.build_type }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        build_type: [Debug, Release]

    steps:
      - uses: actions/checkout@v4

      - name: Configure CMake
        run: cmake -B build -DCMAKE_BUILD_TYPE=${{ matrix.build_type }}

      - name: Build
        run: cmake --build build --config ${{ matrix.build_type }} --parallel

      - name: Test
        working-directory: build
        run: ctest -C ${{ matrix.build_type }} --output-on-failure --parallel 4

  clang-format:
    name: Code Formatting
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install clang-format
        run: sudo apt-get install -y clang-format
      - name: Check formatting
        run: |
          find include src tests -name '*.cpp' -o -name '*.hpp' | \
            xargs clang-format --dry-run --Werror
```

---

### 9. `.github/workflows/release.yml`

```yaml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

permissions:
  contents: write

jobs:
  build-artifacts:
    name: Build / ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            artifact_name: <project-id>-linux-x64
          - os: macos-latest
            artifact_name: <project-id>-macos-universal
          - os: windows-latest
            artifact_name: <project-id>-windows-x64

    steps:
      - uses: actions/checkout@v4
      - name: Configure CMake
        run: cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=install
      - name: Build
        run: cmake --build build --config Release --parallel
      - name: Install
        run: cmake --install build --config Release
      - name: Package (Unix)
        if: runner.os != 'Windows'
        run: cd install && tar czf ../${{ matrix.artifact_name }}.tar.gz .
      - name: Package (Windows)
        if: runner.os == 'Windows'
        run: cd install && Compress-Archive -Path * -DestinationPath ../${{ matrix.artifact_name }}.zip
      - uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.artifact_name }}
          path: ${{ matrix.artifact_name }}.*

  create-release:
    needs: build-artifacts
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          path: artifacts
      - uses: softprops/action-gh-release@v2
        with:
          files: artifacts/**/*
          generate_release_notes: true
```

---

### 10. `.github/dependabot.yml`

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
    commit-message:
      prefix: "ci"
```

---

### 11. `.github/ISSUE_TEMPLATE/bug_report.md`

```markdown
---
name: Bug Report
about: Report a bug to help us improve
title: '[Bug] '
labels: bug
---

## Bug Description

## Steps to Reproduce
1.
2.

## Expected Behavior

## Actual Behavior

## Environment
- **OS**:
- **Compiler**:
- **CMake version**:
- **<ProjectName> version/commit**:

## Minimal Reproducible Example
```cpp
// code here
```
```

---

### 12. `.github/ISSUE_TEMPLATE/feature_request.md`

```markdown
---
name: Feature Request
about: Suggest a new feature or improvement
title: '[Feature] '
labels: enhancement
---

## Problem Statement

## Proposed Solution

## Use Case

## Alternatives Considered
```

---

### 13. `.github/pull_request_template.md`

```markdown
## Description

## Related Issue
Closes #

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Refactoring
- [ ] Documentation
- [ ] CI/build improvement

## Testing

## Checklist
- [ ] Compiles without warnings on all platforms
- [ ] All tests pass (`cmake --build --preset debug && ctest --preset default`)
- [ ] New tests added for new functionality
- [ ] Code formatted (`clang-format`)
- [ ] Documentation updated if needed
```

---

### 14. `CONTRIBUTING.md`

```markdown
# Contributing to <ProjectName>

## Prerequisites

```bash
# macOS
brew install cmake ninja llvm lcov
export PATH="/usr/local/opt/llvm/bin:$PATH"

# Linux
sudo apt-get install cmake ninja-build clang clang-tidy clang-format lcov
```

## Building

```bash
cmake --preset debug
cmake --build --preset debug
ctest --preset default
```

## Running Sanitizers

```bash
# AddressSanitizer (macOS + Linux)
cmake --preset asan && cmake --build --preset asan
cd build/asan && ctest --output-on-failure

# LeakSanitizer (Linux only — not supported on macOS)
cmake --preset lsan && cmake --build --preset lsan

# UndefinedBehaviorSanitizer
cmake --preset ubsan && cmake --build --preset ubsan
```

## Code Style

```bash
find include src tests -name '*.cpp' -o -name '*.hpp' | xargs clang-format -i
```

## Submitting a PR

1. Fork and branch from `main`
2. Make changes and add tests
3. Run `clang-format` and verify all tests pass
4. Open a PR with a clear description

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
```

---

### 15. `SECURITY.md`

```markdown
## Security Policy

### Reporting a Vulnerability

**Do not** open a public GitHub Issue for security vulnerabilities.

Report privately via [GitHub Security Advisories](../../security/advisories/new).

Please include: a description of the vulnerability, steps to reproduce, impact assessment, and any suggested mitigations.

We will acknowledge receipt within 48 hours and provide a fix timeline within 7 days for critical issues.
```

---

### 16. `CODE_OF_CONDUCT.md`

Use the Contributor Covenant 2.1 standard template. Obtain it directly from https://www.contributor-covenant.org/version/2/1/code_of_conduct/ or ask the AI Agent to generate the full content.

---

## README.md — Badges to Add

Add the following directly after the `#` title at the top of the file:

```markdown
[![CI](https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/actions/workflows/ci.yml/badge.svg)](https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
```

---

## Recommended Git Commit Sequence

```bash
git add LICENSE
git commit -m "chore: add MIT License"

git add .github/workflows/ .github/dependabot.yml
git commit -m "ci: add GitHub Actions CI/CD workflows and Dependabot"

git add .github/ISSUE_TEMPLATE/ .github/pull_request_template.md
git add CONTRIBUTING.md SECURITY.md CODE_OF_CONDUCT.md
git commit -m "docs: add GitHub community health files"

git add CMakePresets.json cmake/ CMakeLists.txt
git commit -m "build: modernize CMake with presets, install targets, and CPack"

git add .clang-format .clang-tidy .lcovrc
git commit -m "style: add clang-format, clang-tidy, and lcovrc configuration"

git add README.md
git commit -m "docs: update README with CI badge and MIT license"
```

---

## Troubleshooting

| Error | Root Cause | Fix |
|-------|-----------|-----|
| `cmake --preset asan` → `unsupported option '-fsanitize=leak'` | macOS does not support LeakSanitizer | Use the `asan` preset (no leak); use `lsan` on Linux only |
| `lcov: ERROR: (inconsistent)` | lcov 2.x strict mode + Apple Clang | Use `--config-file .lcovrc` or `cp .lcovrc ~/.lcovrc` |
| `genhtml: ERROR: (corrupt)` | Cascades from an unhandled `inconsistent` error | Same fix — `.lcovrc` already includes `corrupt` in the ignore list |
| `genhtml: ERROR: (category)` | Incompatible coverage data format in Apple Clang system headers | Same fix — `.lcovrc` already includes `category` in the ignore list |
| `clang-tidy: command not found` or wrong version | Using Apple's bundled toolchain | `brew install llvm` and add `/usr/local/opt/llvm/bin` (Intel) or `/opt/homebrew/opt/llvm/bin` (Apple Silicon) to PATH |
| `target_include_directories` install error | Absolute source-tree paths are not allowed in exported targets | Switch to generator expressions: `$<BUILD_INTERFACE:...>` / `$<INSTALL_INTERFACE:...>` |
| CI Windows build fails | Sanitizer flags are not supported on Windows | The `ci.yml` uses plain `cmake` commands (not presets) to avoid injecting sanitizer flags |
