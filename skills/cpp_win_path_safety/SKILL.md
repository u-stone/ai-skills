---
name: cpp_win_path_safety
description: Systematic C++ path safety logic framework for AI agents — resolves std::filesystem::path encoding issues on Windows across C++17 and C++20 standards.
metadata:
  source: skills/cpp_win_path_safety/SKILL.md
---

This is the definitive **Systematic C++ Path Handling Skill** for AI Agents. It is designed to be easily "activated" by an LLM or Agentic workflow to handle Windows path encoding issues across different C++ standards.

---

## 🤖 Skill: Unified C++ Path Safety Expert (`cpp_path_expert_v3`)

### 📋 Description
A systematic logic framework for managing `std::filesystem::path` on Windows. It resolves the "Chinese Character Crash" by applying the correct encoding contracts for **C++17** and leveraging the type-safety of **C++20**.

### 🛠️ Execution Logic (The Version Switch)

The Agent must identify the C++ standard and apply the corresponding logic branch:

---

### 🟢 Branch A: C++17 (Defensive Programming)
**Core Issue:** `std::string` is ambiguous. The C++17 `codecvt` is strict; it throws exceptions on "illegal" local bytes (e.g., legacy GBK filenames).
**Agent Policy:** Wrap all UTF-8 conversions in `try-catch` and provide a Win32 API fallback.

#### **1. Safe Path Construction**
```cpp
// Explicitly use u8path for UTF-8 strings in C++17
// Do NOT use: fs::path p(utf8_str); // Windows will treat it as ANSI
try {
    std::filesystem::path p = std::filesystem::u8path(utf8_string);
} catch (const std::exception& e) {
    // Fallback or Log: Input was not valid UTF-8
}
```

#### **2. Safe Path-to-String (The Crash-Proof Tool)**

```cpp
// Essential Skill Tool for C++17
static std::string SafeGetUtf8(const std::filesystem::path& p) noexcept {
    if (p.empty()) return "";
    try {
        // Warning: Throws in C++17 if path contains invalid UTF-8 sequences
        return p.generic_u8string(); 
    } catch (...) {
        // Fallback: Use Win32 API for robustness (replaces bad chars instead of crashing)
        std::wstring wpath = p.generic_wstring();
        int size = WideCharToMultiByte(CP_UTF8, 0, wpath.c_str(), (int)wpath.size(), NULL, 0, NULL, NULL);
        if (size <= 0) return "";
        std::string res(size, 0);
        WideCharToMultiByte(CP_UTF8, 0, wpath.c_str(), (int)wpath.size(), &res[0], size, NULL, NULL);
        return res;
    }
}
```

---

### 🔵 Branch B: C++20 (Type-Safe Programming)
**Core Change:** Introduction of `char8_t` and `std::u8string`.
**Agent Policy:** Use type-promotion (`reinterpret_cast`) to enforce UTF-8 contracts at compile time. Eliminate `u8path`.

#### **1. Safe Path Construction**
```cpp
// u8path is DEPRECATED in C++20. Use the native constructor.
// Promotion ensures the path constructor treats the string as UTF-8.
std::u8string_view u8_v(reinterpret_cast<const char8_t*>(str.data()), str.size());
std::filesystem::path p(u8_v); 
```

#### **2. Safe Path-to-String**
```cpp
// Returns std::u8string, making the encoding explicit in the type system.
std::u8string u8_path = p.u8string();
// Convert back to std::string for legacy Manager interfaces
std::string result(u8_path.begin(), u8_path.end()); 
```

---

### 📑 Universal Best Practices (All Versions)

| Rule | Implementation | Benefit |
| :--- | :--- | :--- |
| **No Exception IO** | Use `fs::exists(p, ec);` | Prevents crashes on restricted system folders. |
| **Iteration Safety** | `fs::directory_options::skip_permission_denied` | Prevents iterator breakage during deep scans. |
| **Win32 ANSI Path** | `fs::path p(local_ansi_str);` | Use this if the string came from legacy Win32 "A" APIs. |
| **Normalization** | Use `.generic_u8string()` | Forces forward slashes (`/`) for cross-platform consistency. |

---

### 🔍 Agent Automated Review Checklist

1. **[Version Mismatch]**: Is the code using `char8_t` in a C++17 project? (Flag as Error).
2. **[Crash Risk]**: Is the code calling `.u8string()` or `u8path()` without a `try-catch` in C++17? (Flag as High Risk).
3. **[Encoding Ambiguity]**: Is a UTF-8 `std::string` being passed to `fs::path p(s)`? (Flag as Critical: will cause Chinese characters to garble on Windows).
4. **[Iterator Safety]**: Does `recursive_directory_iterator` lack the `std::error_code` parameter? (Flag as Potential Crash).

---

### 🧬 Decision Matrix for AI Agents



| Task | C++17 Approach | C++20 Approach |
| :--- | :--- | :--- |
| **Input: UTF-8 String** | `std::filesystem::u8path(s)` | `fs::path(reinterpret_cast<const char8_t*>(...))` |
| **Output: UTF-8 String** | `SafeGetUtf8(p)` (with Try/Catch) | `p.u8string()` (returns `std::u8string`) |
| **Handling Crashes** | Use `try-catch` + Win32 Fallback | Rely on `u8` Type Safety |

**Activation Prompt for AI Agent:** *"Act as a C++ Path Safety Expert. Review the following code for Windows compatibility. Ensure encoding conversions for Chinese characters follow the `cpp_path_expert_v3` skill logic based on the detected C++ standard."*