# Global scope MdtConfig.cmake

[![pipeline status](https://gitlab.com/scandyna/mdtcmakeconfig/badges/experimental/pipeline.svg)](https://gitlab.com/scandyna/mdtcmakeconfig/-/pipelines/latest)

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
MdtCMakeConfig/0.x.y@scandyna/testing
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

Note: Debian package is not implemented yet

# Work on MdtCMakeConfig

## Build and test

See [BUILD](BUILD.md).

# Rationale

## Conan

To create Conan packages that support `find_package` COMPONENTS syntax
with the new Conan generators is discussed in [Split Qt packages](ConanSplitQt.md).

## No package manager

[Here](NoPackageManager.md)
are some thought about usage without a package manager.

## Background

[Here](MdtBackground.md) are also some other discussions about Mdt.
