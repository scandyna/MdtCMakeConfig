
# Conan build_module

Explain set(Mdt0_DIR ) not work, or search if could work

Understand multpile inclusion

find_package() searches in CMAKE_PREFIX_PATH to find Mdt0Config.cmake
CMAKE_PREFIX_PATH only contains user's build dir
It find the Conan generated Mdt0Config.cmake
This lat one includes the code of upstream Mdt0Config.cmake

Put this to Rationale:
If not including Mdt0Config.cmake code, but set Mdt0_DIR:
find_package() finds the Conan generated Mdt0Config.cmake,
so it does not execute the code of upstream Mdt0Config.cmake

multi inclusion protect:
Seems to be specific to Conan cmake_find_package* generators ?

Maybe: test find_package(Mdt0ItemModel ...)

# Other

Remove searching in . relative PATH (has no sense to search in the conan package of MdtCMakeConfig !)
ALSO fix example in ConanSplitQt.md !

should work with cmake generator ans CMakeDeps generator !

usage with and without a package manager !

TODO: later, will have to generate 2 variants.
See `PATHS "${CMAKE_CURRENT_LIST_DIR}" NO_DEFAULT_PATH`
and `PATHS "${CMAKE_CURRENT_LIST_DIR}/.." NO_DEFAULT_PATH`

Issue title ideas:
- CMake find_package() COMPONENTS across Conan packages   <-- Winner
- Express Conan component syntax across multiple packages


Idea:
make MdtConfig.cmake.in
from it, generate Mdt0Config.cmake or a other name ?
include it as a build-module in conan
