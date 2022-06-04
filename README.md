# Global scope MdtConfig.cmake

[[_TOC_]]

## Usage

### Project using Conan

```txt
[requires]
Mdt/0@scandyna/testing # TODO: check if 0 is ok for Conan
# OR
MdtCMakeConfig/0@scandyna/testing # TODO: check if 0 is ok for Conan
```

### Install the Debian package

```bash
sudo apt-get install mdt0
# OR
sudo apt-get install mdt0CMakeConfig
```

## Background

Mdt is a namespace used in my personal projects (naming things is hard).

It has no real name today.
After a project, named "Linux Diag Tools"
(that was finally just a tiny, basic, badly working, application communicating with a instrument via a RS232 serial port),
I renamed it "Multiplatorm Diag Tools".

Working on my dream, and realizing a bit what such project requires,
it became more a set of libraries that helps solve various common problems.

Today, I think that Mdt could mean "Multiplatform Development Tools",
despite, only Linux and Windows is supported for now.

### Monolitic repository

Because of the lack of C++ package manager,
all the code was in a [monolitic repository](https://github.com/scandyna/multidiagtools).

### Splitting to projects

One day, I had to use a library from Mdt.
I don't remeber exactly, but it was not easy.
And more, I had to get a elephant to use a flea.

Discovering the [Conan](https://conan.io/) package manager,
I decided to start to split the tools and libraries
(and yeah.. rewrite most of their parts, because.. I was young).

## CMake find_package() component syntax

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

## ????

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

### Conan package

```txt
[requires]
Mdt/0@scandyna/testing # TODO: check if 0 is ok for Conan
# OR
MdtCMakeConfig/0@scandyna/testing # TODO: check if 0 is ok for Conan
```

TODO: should work with cmake generator ans CMakeDeps generator !

### Debian package

### No package manager

# TODO: usage with and without a package manager !

Each project will be 


Working on my dream, I finally realized 

It started with a idea to create 
At the start, it was a idea

explain cmake component syntax, but multiple projects and packages

for global installs, otherwise MdtCMakeModules one


