# Standard C++ Library Directory Structure

Adopting this structure ensures that `FetchContent` and `install()` work out of the box.

```text
ProjectRoot/
├── CMakeLists.txt          # Main build script
├── include/
│   └── <ProjectName>/      # Public headers (Namespaced!)
│       ├── MyClass.h
│       └── Export.h        # Visibility macros
├── src/                    # Source files and private headers
│   ├── MyClass.cpp
│   └── Internal.h
├── examples/               # Usage examples (optional but recommended)
├── tests/                  # Unit tests
└── cmake/                  # Helper scripts (optional)
```

**Why this matters:**
*   **include/ProjectName**: When users do `target_link_libraries(UserApp PRIVATE Project::Project)`, CMake adds `.../ProjectRoot/include` to their include path. They can then write `#include <ProjectName/MyClass.h>`, which avoids filename collisions with other libraries.
