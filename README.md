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

# Work on MdtCMakeConfig

## Build and test

See [BUILD](BUILD.md).
