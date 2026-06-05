# 构建模板

本文件给出 `nanobind + scikit-build-core + CMake` 的通用模板。先选 ABI 策略，再复制对应片段，避免把 Python `>=3.9` 与 `cp312` 稳定 ABI 混在一起。

## pyproject.toml：每版本构建（支持 Python 3.9+）

```toml
[build-system]
requires = ["scikit-build-core>=0.10", "nanobind>=2.0"]
build-backend = "scikit_build_core.build"

[project]
name = "mypackage"
version = "0.1.0"
description = "Python bindings for My Native Library"
requires-python = ">=3.9"

[tool.scikit-build]
wheel.packages = ["src/mypackage"]
build-dir = "build/{wheel_tag}"
# cmake.verbose = true  # enable only when debugging configure/build issues
```

## pyproject.toml：稳定 ABI（Python 3.12+）

```toml
[build-system]
requires = ["scikit-build-core>=0.10", "nanobind>=2.0"]
build-backend = "scikit_build_core.build"

[project]
name = "mypackage"
version = "0.1.0"
description = "Python bindings for My Native Library"
requires-python = ">=3.12"

[tool.scikit-build]
wheel.packages = ["src/mypackage"]
build-dir = "build/{wheel_tag}"
wheel.py-api = "cp312"
# cmake.verbose = true  # enable only when debugging configure/build issues
```

## CMakeLists.txt（双模式）

```cmake
cmake_minimum_required(VERSION 3.18)
project(MyBindings LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(PY_PACKAGE "mypackage")
set(PY_SUBPACKAGE "platform")
set(EXT_MODULE "_core")
set(MODULE_INSTALL_DIR "${PY_PACKAGE}/${PY_SUBPACKAGE}")

if(TARGET NativeLibrary)
    # 集成模式：绑定作为上层 CMake 工程的一部分构建。
    set(NATIVE_LIBRARY_TARGETS NativeLibrary)
else()
    # 独立模式：绑定包查找已经构建好的 C++ 库。
    include(cmake/FindNativeLibrary.cmake)
endif()

find_package(Python 3.9 COMPONENTS Interpreter Development.Module REQUIRED)
execute_process(
    COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
    OUTPUT_VARIABLE nanobind_ROOT
    OUTPUT_STRIP_TRAILING_WHITESPACE)
find_package(nanobind CONFIG REQUIRED)

set(BINDING_SOURCES
    bindings/platform/module.cpp
)

nanobind_add_module(${EXT_MODULE}
    # Add STABLE_ABI only when pyproject.toml uses requires-python >=3.12
    # and wheel.py-api = "cp312".
    ${BINDING_SOURCES})

target_link_libraries(${EXT_MODULE} PRIVATE ${NATIVE_LIBRARY_TARGETS})
target_include_directories(${EXT_MODULE} PRIVATE ${NATIVE_LIBRARY_INCLUDES})

if(MSVC)
    target_compile_options(${EXT_MODULE} PRIVATE /MP /utf-8)
    target_compile_definitions(${EXT_MODULE} PRIVATE NOMINMAX WIN32_LEAN_AND_MEAN)
endif()

if(APPLE)
    set_target_properties(${EXT_MODULE} PROPERTIES
        BUILD_RPATH "@loader_path"
        INSTALL_RPATH "@loader_path")
elseif(UNIX)
    set_target_properties(${EXT_MODULE} PROPERTIES
        BUILD_RPATH "$ORIGIN"
        INSTALL_RPATH "$ORIGIN")
endif()

install(TARGETS ${EXT_MODULE}
    LIBRARY DESTINATION ${MODULE_INSTALL_DIR}
    RUNTIME DESTINATION ${MODULE_INSTALL_DIR})
```

启用稳定 ABI 时，把 `nanobind_add_module` 改成：

```cmake
nanobind_add_module(${EXT_MODULE}
    STABLE_ABI
    ${BINDING_SOURCES})
```

Free-threaded Python 需要单独构建，并添加 `FREE_THREADED`；不要把它和 `STABLE_ABI` 视为同一个产物。

## FindNativeLibrary.cmake（预编译库发现）

```cmake
find_library(NATIVE_LIBRARY_FILE NAMES NativeLibrary
    PATHS
        "${NATIVE_LIBRARY_BUILD_DIR}/lib"
        "${NATIVE_LIBRARY_BUILD_DIR}/lib/Debug")

find_path(NATIVE_LIBRARY_SRC_INCLUDE NAMES NativeLibrary/PublicHeader.h
    PATHS "${CMAKE_CURRENT_SOURCE_DIR}/../NativeLibrary/include")

find_path(NATIVE_LIBRARY_GEN_INCLUDE NAMES NativeLibrary/Export.h
    PATHS "${NATIVE_LIBRARY_BUILD_DIR}/generated/include")

add_library(NativeLibrary_imported SHARED IMPORTED)
set_target_properties(NativeLibrary_imported PROPERTIES
    IMPORTED_LOCATION "${NATIVE_LIBRARY_FILE}")
target_include_directories(NativeLibrary_imported INTERFACE
    "${NATIVE_LIBRARY_SRC_INCLUDE}"
    "${NATIVE_LIBRARY_GEN_INCLUDE}")

set(NATIVE_LIBRARY_TARGETS NativeLibrary_imported)
set(NATIVE_LIBRARY_INCLUDES
    "${NATIVE_LIBRARY_SRC_INCLUDE}"
    "${NATIVE_LIBRARY_GEN_INCLUDE}")
```

注意：

- 将 `NativeLibrary`、`mypackage`、`platform` 和 `_core` 替换为项目实际名称。
- 如果依赖库已安装到系统路径，可以保留默认搜索；不要默认使用 `NO_DEFAULT_PATH`。
- 需要随 wheel 分发的动态库应安装到 native 扩展所在目录或平台约定目录，并配合 rpath / DLL 搜索路径。
