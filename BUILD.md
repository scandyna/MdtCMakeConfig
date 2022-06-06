[[_TOC_]]

# Build and test MdtCMakeConfig

This section describes how to
configure, build and run the tests.

For simplicity,
it is assumed that you are in a build sub-directory of the source tree
(complete out of source build is supported and also recommended).

## Configure MdtCMakeConfig

This is a example on Linux using gcc.

Install the dependencies:
```bash
conan install --profile linux_gcc7_x86_64 -s build_type=Debug --build=missing ../packaging/conan
```

Configure MdtCMakeConfig:
```bash
source conanbuild.sh
cmake -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DBUILD_TESTS=ON ..
cmake-gui .
```

## Build and run the tests

Those examples use cmake to run the build,
which should work everywhere.

Build:
```bash
cmake --build . --config Debug -j4
```

To run the tests:
```bash
ctest --output-on-failure -C Debug -j4
```
