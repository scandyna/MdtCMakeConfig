[[_TOC_]]

# Split Qt packages

As example, imagine we want to split Qt into several Conan packages.

In the user conanfile.txt:
```txt
[requires]
QtWidgets/5.15.2
QtSql/5.15.2

[generators]
CMakeDeps
CMakeToolchain
```

In the user CMakeLists.txt:
```cmake
find_package(Qt5 REQUIRED COMPONENTS Widgets Sql)
# OR
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Sql REQUIRED)
```

For the COMPONENTS syntax of `find_package()`,
Cmake requires a file, named `Qt5Config.cmake`.

For the other syntax in obove example,
CMake requires 2 files, respectively `Qt5WidgetsConfig.cmake` and `Qt5SqlConfig.cmake`.


# What result should we have

After `conan install`, we should end up with CMake package config files
for all required Qt libraries, and also `Qt5Config.cmake`.

This example lists the result.
It only lists a set of CMake package config files
(`*-Targets*`, `*-data*`, also other dependencies are omitted):
```bash
Qt5Config.cmake
Qt5CoreConfig.cmake
Qt5SqlConfig.cmake
Qt5WidgetsConfig.cmake
```

In `Qt5CoreConfig.cmake`, `Qt5::Core` target will be defined.
The 2 other libraries (Qt5Widgets and Qt5Sql) are defined the same way.

The simplified content of `Qt5Config.cmake` looks like this:
```cmake
set(_Qt5_FIND_PARTS_REQUIRED)
if (Qt5_FIND_REQUIRED)
  set(_Qt5_FIND_PARTS_REQUIRED REQUIRED)
endif()

foreach(component ${Qt5_FIND_COMPONENTS})
  find_package(Qt5${component}
    QUIET CONFIG
    ${_Qt5_FIND_PARTS_REQUIRED}
    NO_CMAKE_ENVIRONMENT_PATH NO_SYSTEM_ENVIRONMENT_PATH NO_CMAKE_PACKAGE_REGISTRY NO_CMAKE_SYSTEM_PATH NO_CMAKE_SYSTEM_PACKAGE_REGISTRY
  )
endforeach()
```

Above code will tell `find_package()` to locate the components
package config files in `CMAKE_PREFIX_PATH`.

For more informations about the CONFIG mode search procedure, see also
[find_package() search procedure](https://cmake.org/cmake/help/latest/command/find_package.html#config-mode-search-procedure).

# Express Qt5Config.cmake

Qt:
```python
class QtConan(ConanFile):

  name = "Qt"

  def package_info(self):

    self.cpp_info.set_property("cmake_file_name", "Qt5")
    # ??
```

How can we tell Conan CMake generators to provide
the `find_package(Qt5 COMPONENTS ...)` syntax ?

It could be tempting to describe the components
in some Qt meta-package:
```python
class QtConan(ConanFile):

  name = "Qt"

  def package_info(self):

    self.cpp_info.set_property("cmake_file_name", "Qt5")

    self.cpp_info.components["QtWidgets"].set_property("cmake_target_name", "Qt5::Widgets")
    # Will this even work ?
    self.cpp_info.components["QtWidgets"].requires = ["QtWidgets"]

    # Put all other Qt components here..
```

At first, I don't know if above example even could work.

More important: if it can work, we will end up with a package,
named `Qt`, that depends on all other Qt packages
(QtCore, QtWidgets, QtSql, ...).
So we are back to the monolitic package.
Even if we put options to enable components or not,
the problem of combinatorial builds is back.

# Workaround

With modern Conan CMake generators, all CMake config files are generated in the users build directory.

We have to provide some CMake code that will locate Qt components
in the build directory of the user.

We can use what Conan calls a `build_module`,
that will be included by the generated `Qt5Config.cmake`.

For some details about `build_modules` and some rules to follow,
see [Conan and CMake](https://scandyna.gitlab.io/mdt-cmake-modules/ConanAndCMake.html).

Here is a simplified example of the build module, named `conan-qt5-config.cmake`:
```cmake
# Prevent for multiple inclusion
if(Qt5_CONFIG_INCLUDED)
  return()
endif()
set(Qt5_CONFIG_INCLUDED TRUE)

set(_Qt5_FIND_PARTS_REQUIRED)
if (Qt5_FIND_REQUIRED)
  set(_Qt5_FIND_PARTS_REQUIRED REQUIRED)
endif()

foreach(component ${Qt5_FIND_COMPONENTS})
  # Limit the search to CMAKE_PREFIX_PATH
  find_package(Qt5${component}
    QUIET CONFIG
    ${_Qt5_FIND_PARTS_REQUIRED}
    NO_CMAKE_ENVIRONMENT_PATH NO_SYSTEM_ENVIRONMENT_PATH NO_CMAKE_PACKAGE_REGISTRY NO_CMAKE_SYSTEM_PATH NO_CMAKE_SYSTEM_PACKAGE_REGISTRY
  )
endforeach()
```

For this example, the (installed) package layout looks like this:
```
package-root
  |-conan-qt5-config.cmake
```

In the conanfile, we declare `conan-qt5-config.cmake` as build module:
```python
class QtConan(ConanFile):

  name = "Qt"

  def package_info(self):

    self.cpp_info.set_property("cmake_file_name", "Qt5")

    build_modules = ["conan-qt5-config.cmake"]

    self.cpp_info.set_property("cmake_build_modules", build_modules)
    # Note: how can we tell Conan to not generate a fake Qt::Qt target ?
```

The installation of the files is omitted in above example.

The other Qt packages will not use the Conan component syntax anymore.

Simplified example for QtWidgets:
```python
class QtWidgetsConan(ConanFile):

  name = "QtWidgets"
  requires = "QtGui", "Qt"

  def package_info(self):

    self.cpp_info.set_property("cmake_file_name", "Qt5Widgets")
    self.cpp_info.set_property("cmake_target_name", "Qt5::Widgets")
    self.cpp_info.libs = ["Qt5Widgets"]
```

# Rationale

Here are described some things I have tried.

All examples refers to Qt5 as example,
because it is a known library.

In reallity, I'm inspired by Qt,
but all that I have tried is for Mdt.

## find_package() search procedure

This is what I understand, it could be wrong, and it is not complete.

Take a example of a user project that depends on QtCore:
```txt
[requires]
QtCore/5.15.2

[generators]
CMakeDeps
CMakeToolchain
```

In the CMakeLists.txt:
```cmake
find_package(Qt5 REQUIRED COMPONENTS Core)
```

After `conan install` the build directory contains at least those files
(simplified):
```bash
conan_toolchain.cmake
Qt5Config.cmake
Qt5CoreConfig.cmake
```

The user configures the project:
```bash
cmake -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake pathToSourceDir
```

The `CMAKE_PREFIX_PATH` only contains the path to the build directly.

`find_package()` locates `Qt5Config.cmake` in the build directory.
This file, generated by Conan, does not contain the stuff we really need,
bacause we cannot express it in the `conanfile.py` (as far as I know).
At this point, `Qt5_FOUND` is set and `find_package()` stops.
If we did not do any workaround, Qt5Core will not be available to the user project.

But, because we declared `conan-qt5-config.cmake` as build module, it will be included.
This one will include the upstream `Qt5Config.cmake`,
which contains the code to find the components:
```cmake
foreach(component ${Qt5_FIND_COMPONENTS})
  # Simplified call (see above example for missing arguments)
  find_package(Qt5${component})
endforeach()
```

`find_package()` will now be called to find Qt5Widgets.
It will locate `Qt5WidgetsConfig.cmake` in the users build directory,
because it is in the `CMAKE_PREFIX_PATH`.

## Set Qt5_DIR or include ?

As first idea, I tough that the build module `conan-qt5-config.cmake`
should set `Qt5_DIR` so that it references the upstream `Qt5Config.cmake`.
This did not work.
The reason is explained above in the find_package() search procedure.

## Reuse upstream Qt5Config.cmake ?

First idea was to create one Qt5Config.cmake and reuse it for the Conan package.

Looking a bit deeper, I realized that the upstream and the Conan version are slightly different.

Simplified version of upstream `Qt5Config.cmake`:
```cmake
get_filename_component(_qt5_install_prefix "${CMAKE_CURRENT_LIST_DIR}/.." ABSOLUTE)

foreach(component ${Qt5_FIND_COMPONENTS})
  find_package(Qt5${component}
    PATHS ${_qt5_install_prefix} NO_DEFAULT_PATH
  )
endforeach()
```
Above version will find the components in the Qt distribution.

Simplified version of `conan-qt5-config.cmake`:
```cmake
foreach(component ${Qt5_FIND_COMPONENTS})
  find_package(Qt5${component}
    NO_CMAKE_ENVIRONMENT_PATH NO_SYSTEM_ENVIRONMENT_PATH NO_CMAKE_PACKAGE_REGISTRY NO_CMAKE_SYSTEM_PATH NO_CMAKE_SYSTEM_PACKAGE_REGISTRY
  )
endforeach()
```
Above version will find the components in the `CMAKE_PREFIX_PATH`,
which will be set to the user build directory by Conan.

## Define Conan recipes with components ?

We could define components as described
in [Define the package information](https://docs.conan.io/en/latest/creating_packages/package_information.html),
in [cmake_find_package_multi](https://docs.conan.io/en/latest/reference/generators/cmake_find_package_multi.html)
and in [CMakeDeps](https://docs.conan.io/en/latest/reference/conanfile/tools/cmake/cmakedeps.html).

Lets try to define `QtWidgets` and `QtSql`.

Examples will be simplified, only containing the minimum for the purpose
and do not take care of the `cmake_find_package` and `cmake_find_package_multi` generators.

QtWidgets:
```python
class QtWidgetsConan(ConanFile):

  name = "QtWidgets"
  requires = "QtGui"

  def package_info(self):

    self.cpp_info.set_property("cmake_file_name", "Qt5")
    self.cpp_info.components["QtWidgets"].set_property("cmake_target_name", "Qt5::Widgets")
    self.cpp_info.components["QtWidgets"].libs = ["Qt5Widgets"]
    self.cpp_info.components["QtWidgets"].requires = ["QtGui"]
```

QtSql:
```python
class QtSqlConan(ConanFile):

  name = "QtSql"
  requires = "QtCore"

  def package_info(self):

    self.cpp_info.set_property("cmake_file_name", "Qt5")
    self.cpp_info.components["QtSql"].set_property("cmake_target_name", "Qt5::Sql")
    self.cpp_info.components["QtSql"].libs = ["Qt5Sql"]
    self.cpp_info.components["QtSql"].requires = ["QtCore"]
```

In the user project:
```txt
[requires]
QtWidgets/5.15.2
QtSql/5.15.2

[generators]
CMakeDeps
CMakeToolchain
```

Here we have 2 problems.

First, we tell Conan to generate `Qt5Config.cmake` multiple times.
So, in the build directory of the user project,
we end up with only 1 target defined.
It could be Qt5::Widgets, Qt5::Sql, Qt5::Core
(it probably depends on the resolution/generation order).

Second, we don't have `Qt5WidgetsConfig.camke` and `Qt5SqlConfig.cmake` files.
This syntax will then not work:
```cmake
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Sql REQUIRED)
```
