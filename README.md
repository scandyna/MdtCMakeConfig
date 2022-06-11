# Global scope MdtConfig.cmake

[[_TOC_]]

# Usage

This illustrates what a Mdt library should do
so that the user can use the CMake `find_package()`
component syntax:
```cmake
find_package(Mdt0 REQUIRED COMPONENTS PlainText)
```

## Project using Conan

The library should depend on `MdtCMakeConfig`:
```txt
[requires]
# TODO: check if 0 is ok for Conan
MdtCMakeConfig/0@scandyna/testing
```

The user project will then use the library:
```txt
[requires]
MdtPlainText/0.x.y@scandyna/testing
```

## Install the Debian package

The library should depend on `MdtCMakeConfig`:
```bash
sudo apt-get install mdt0plaintext
# Will also install mdt0cmakeconfig
```

# CMake find_package() component syntax

# Conan and find_package() component syntax

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

## Define Conan recipes with components ?

We could define components as described
in [Define the package information](https://docs.conan.io/en/latest/creating_packages/package_information.html),
in [cmake_find_package_multi](https://docs.conan.io/en/latest/reference/generators/cmake_find_package_multi.html)
and in [CMakeDeps](https://docs.conan.io/en/latest/reference/conanfile/tools/cmake/cmakedeps.html).

Lets try to define `QtWidgets` and `QtSql`.

Examples will be simplified, only containing the minimum for the purpose
and do not take care of the `cmake_find_package` and `cmake_find_package_multi` generators.

QtWidgets:
```conan
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
```conan
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

## What result should we have

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

## Express Qt5Config.cmake

Qt:
```conan
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
```conan
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

## Workaround

Because the only thing we need is to support the CMake
`find_package()` COMPONENTS syntax,
we can create a package that loads a CMake module:
```conan
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
```conan
class QtWidgetsConan(ConanFile):

  name = "QtWidgets"
  requires = "QtGui", "Qt"

  def package_info(self):

    self.cpp_info.set_property("cmake_file_name", "Qt5Widgets")
    self.cpp_info.set_property("cmake_target_name", "Qt5::Widgets")
    self.cpp_info.libs = ["Qt5Widgets"]
```


TODO: decribe how to make conan generate Qt5Config.cmake
Or, workaround

TODO: later, will have to generate 2 variants.
See `PATHS "${CMAKE_CURRENT_LIST_DIR}" NO_DEFAULT_PATH`
and `PATHS "${CMAKE_CURRENT_LIST_DIR}/.." NO_DEFAULT_PATH`

# OTHER

After calling conan install, the build directory will, of course,
only contains 1 `Qt5Config.cmake` file.
This is because each package describes it own.

As result, only 1 Qt library will be defined
(maybe QtSql, probably depends of the resolution/generation order).

## Remember what we need

TODO: remeber find_package() COMPONENTS syntax

## Possible solution


TODO: x overwrites y depends on resolution process ?

TODO: what we should have when generated (f.ex. with CMakeDeps)

TODO: conan component syntax and conflict of Qt5Config.cmake

# Background

Mdt is a namespace used in my personal projects (naming things is hard).

It has no real name today.
After a project, named "Linux Diag Tools"
(that was finally just a tiny, basic, badly working, application communicating with a instrument via a RS232 serial port),
I renamed it "Multiplatorm Diag Tools".

Working on my dream, and realizing a bit what such project requires,
it became more a set of libraries that helps solve various common problems.

Today, I think that Mdt could mean "Multiplatform Development Tools",
despite, only Linux and Windows is supported for now.

## Monolitic repository

Because of the lack of C++ package manager,
all the code was in a [monolitic repository](https://github.com/scandyna/multidiagtools).

## Splitting to projects

One day, I had to use a library from Mdt.
I don't remeber exactly, but it was not easy.
And more, I had to get a elephant to use a flea.

Discovering the [Conan](https://conan.io/) package manager,
I decided to start to split the tools and libraries
(and yeah.. rewrite most of their parts, because.. I was young).

# CMake find_package() component syntax

All my libraries are in the `Mdt` namespace in the C++ source code.

Using Qt, I like the CMake component syntax:
```cmake
find_package(Qt5 COMPONENTS Widgets SerialPort)
find_package(Mdt0 COMPONENTS ItemModel Sql)
```

While this is natural for a monolitic repository,
I made it the wrong way while splitting the projects.

In the project's main CMakeLists.txt:
```cmake
include(GNUInstallDirs)
include(MdtInstallDirs)
include(MdtPackageConfigHelpers)

if(NOT MDT_INSTALL_IS_UNIX_SYSTEM_WIDE)
  mdt_install_namespace_package_config_file(
    INSTALL_NAMESPACE Mdt0
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/Mdt0"
  )
endif()
```

More informations are available
in the [MdtPackageConfigHelpers](https://scandyna.gitlab.io/mdt-cmake-modules/Modules/MdtPackageConfigHelpers.html) documentation.

Notice the `if(NOT MDT_INSTALL_IS_UNIX_SYSTEM_WIDE)`:
I already know that, at some point,
it will be required to create some package to make a system wide install on Linux,
otherwise there will be conflicts
(each package will install `/usr/lib/cmake/Mdt0/Mdt0Config.cmake` for example).

Recently, while porting some project to use the new
Conan [CMakeDeps](https://docs.conan.io/en/latest/reference/conanfile/tools/cmake/cmakedeps.html),
I was stuck.

# ????

Here is basically what is in `Mdt0Config.cmake`:
```cmake
foreach(component ${Mdt0_FIND_COMPONENTS})
  find_package(
    Mdt0${component}
    ${Mdt0_FIND_VERSION}
    QUIET CONFIG
    PATHS "${CMAKE_CURRENT_LIST_DIR}/.." NO_DEFAULT_PATH
  )
  if(NOT Mdt0${component}_FOUND AND ${Mdt0_FIND_REQUIRED_${component}})
    find_package(
      Mdt0${component}
      ${Mdt0_FIND_VERSION}
      QUIET CONFIG
    )
    if(NOT Mdt0${component}_FOUND AND ${Mdt0_FIND_REQUIRED_${component}})
      set(Mdt0_NOT_FOUND_MESSAGE "Failed to find Mdt0::${component}")
      set(Mdt0_FOUND False)
      break()
    endif()
  endif()
endforeach()
```

At first, it will try to find the package locally,
independently of `CMAKE_PREFIX_PATH`.
If not found, it will then try other paths.

Note: calling 2x find_package() as above
seems to be obselete since CMake 3.12.

## Conan package

```txt
[requires]
Mdt/0@scandyna/testing # TODO: check if 0 is ok for Conan
# OR
MdtCMakeConfig/0@scandyna/testing # TODO: check if 0 is ok for Conan
```

TODO: should work with cmake generator ans CMakeDeps generator !

TODO: usage with and without a package manager !

# Work on MdtCMakeModules

## Build and test

See [BUILD](BUILD.md).
