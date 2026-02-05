# Cross-Platform Export Macros

Use this standard block to handle symbol visibility for Windows (DLL) and Linux/macOS (ELF).

```cpp
#pragma once

#if defined(_WIN32) || defined(__CYGWIN__)
    #ifdef MYLIB_EXPORTS // Define this macro when compiling the library itself
        #define MYLIB_API __declspec(dllexport)
    #else
        #define MYLIB_API __declspec(dllimport)
    #endif
    #define MYLIB_LOCAL
#else
    #if __GNUC__ >= 4
        #define MYLIB_API __attribute__ ((visibility ("default")))
        #define MYLIB_LOCAL  __attribute__ ((visibility ("hidden")))
    #else
        #define MYLIB_API
        #define MYLIB_LOCAL
    #endif
#endif
```

## Usage
- Apply `MYLIB_API` to public classes and functions.
- Apply `MYLIB_LOCAL` to internal helper classes to prevent symbol pollution.
