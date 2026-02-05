#ifndef MY_PROJECT_EXPORT_H
#define MY_PROJECT_EXPORT_H

// STATIC BUILD: No export/import needed
#ifdef MY_PROJECT_STATIC
    #define MY_PROJECT_API
#else
    // WINDOWS DYNAMIC LINKING
    #ifdef _WIN32
        #ifdef MyProject_EXPORTS // Defined by CMake when building the DLL
            #define MY_PROJECT_API __declspec(dllexport)
        #else
            #define MY_PROJECT_API __declspec(dllimport)
        #endif
    
    // LINUX/MACOS VISIBILITY (GCC/CLANG 4+)
    #else
        #if __GNUC__ >= 4
            #define MY_PROJECT_API __attribute__((visibility("default")))
        #else
            #define MY_PROJECT_API
        #endif
    #endif
#endif

#endif // MY_PROJECT_EXPORT_H
