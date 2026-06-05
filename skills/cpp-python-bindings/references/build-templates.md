# 构建模板

## pyproject.toml

```toml
[build-system]
requires = ["scikit-build-core>=0.10", "nanobind>=2.0"]
build-backend = "scikit_build_core.build"

[project]
name = "myengine"
version = "0.1.0"
description = "Python bindings for MyEngine"
requires-python = ">=3.9"

[tool.scikit-build]
wheel.packages = ["src/myengine"]
cmake.verbose = true
build-dir = "build/{wheel_tag}"
minimum-version = "0.4"
wheel.py-api = "cp312"  # STABLE_ABI: 一个 wheel 覆盖 3.12+
```

## CMakeLists.txt（双模式）

```cmake
cmake_minimum_required(VERSION 3.18)
project(MyBindings LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ── 模式检测 ────────────────────────────
if(TARGET ExistingModule)
    # 引擎集成模式：直接链接 CMake target
    set(ENGINE_LIBS ExistingModule DepModule)
    set(ENGINE_INCLUDES "${CMAKE_SOURCE_DIR}/../ExistingModule/source/public")
else()
    # 独立模式：查找预编译引擎
    include(cmake/FindEngine.cmake)
endif()

# ── Python + nanobind ─────────────────────
find_package(Python 3.9 COMPONENTS Interpreter Development.Module REQUIRED)
execute_process(
    COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
    OUTPUT_VARIABLE nanobind_ROOT OUTPUT_STRIP_TRAILING_WHITESPACE)
find_package(nanobind CONFIG REQUIRED)

# ── 扩展模块 ─────────────────────────────
nanobind_add_module(_core bindings/module.cpp
    STABLE_ABI)
target_link_libraries(_core PRIVATE ${ENGINE_LIBS})
target_include_directories(_core PRIVATE ${ENGINE_INCLUDES})

# ── 平台设置 ─────────────────────────────
if(MSVC)
    target_compile_options(_core PRIVATE /MP /utf-8)
    target_compile_definitions(_core PRIVATE NOMINMAX WIN32_LEAN_AND_MEAN)
endif()

# ── rpath ─────────────────────────────────
if(APPLE)
    set_target_properties(_core PROPERTIES
        BUILD_WITH_INSTALL_RPATH TRUE
        INSTALL_RPATH "@loader_path")
elseif(UNIX)
    set_target_properties(_core PROPERTIES
        BUILD_WITH_INSTALL_RPATH TRUE
        INSTALL_RPATH "$ORIGIN")
endif()

# ── Install ───────────────────────────────
install(TARGETS _core
    LIBRARY DESTINATION myengine
    RUNTIME DESTINATION myengine)
```

## FindEngine.cmake（预编译库发现）

```cmake
# 搜索库文件
find_library(MODULE_LIB NAMES ExistingModule
    PATHS "${ENGINE_BUILD_DIR}/lib" "${ENGINE_BUILD_DIR}/lib/Debug"
    NO_DEFAULT_PATH)

# 搜索源码头文件
find_path(MODULE_SRC_INCLUDE NAMES ExistingModule/SomeClass.h
    PATHS "${CMAKE_CURRENT_SOURCE_DIR}/../ExistingModule/source/public")

# 搜索生成头文件（导出宏、平台配置）
find_path(MODULE_GEN_INCLUDE NAMES ExistingModule/Export.h
    PATHS "${ENGINE_BUILD_DIR}/ExistingModule/gen/public")

# 创建 IMPORTED target
add_library(ExistingModule_imported SHARED IMPORTED)
set_target_properties(ExistingModule_imported PROPERTIES
    IMPORTED_LOCATION "${MODULE_LIB}")
target_include_directories(ExistingModule_imported INTERFACE
    "${MODULE_SRC_INCLUDE}" "${MODULE_GEN_INCLUDE}")
```

注意：
- 生成头文件（`Export.h`、`Config.h`）与源码头文件可能在**不同目录**
- 引擎库可能在 `lib/Debug/` 而非 `lib/`
- 独立模式下需要将所有传递依赖 DLL 打包进 wheel
