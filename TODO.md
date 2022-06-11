
should work with cmake generator ans CMakeDeps generator !

usage with and without a package manager !

TODO: later, will have to generate 2 variants.
See `PATHS "${CMAKE_CURRENT_LIST_DIR}" NO_DEFAULT_PATH`
and `PATHS "${CMAKE_CURRENT_LIST_DIR}/.." NO_DEFAULT_PATH`

Issue title ideas:
- CMake find_package() COMPONENTS across Conan packages
- Express Conan component syntax across multiple packages


Idea:
make MdtConfig.cmake.in
from it, generate Mdt0Config.cmake or a other name ?
include it as a build-module in conan
