[[_TOC_]]

# Split Qt packages

As example, imagine we want to split Qt into several Conan packages.

In the user conanfile.txt:
```txt
[requires]
QtWidgets/5.15.2
QtSql/5.15.2
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
    PATHS "${CMAKE_CURRENT_LIST_DIR}" NO_DEFAULT_PATH
  )
endforeach()
```

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

Because the only thing we need is to support the CMake
`find_package()` COMPONENTS syntax,
we can create a package that loads a CMake module:
```python
class QtConan(ConanFile):

  name = "Qt"

  def package(self):

    self.copy("Qt5Config.cmake")

  def package_info(self):

    self.cpp_info.set_property("cmake_file_name", "Qt5")

    build_modules = ["Qt5Config.cmake"]

    self.cpp_info.set_property("cmake_build_modules", build_modules)
    # Note: how can we tell Conan to not generate a fake Qt::Qt target ?
```

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
