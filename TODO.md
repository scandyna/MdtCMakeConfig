
Issue title ideas:
- CMake find_package() COMPONENTS across Conan packages
- Express Conan component syntax across multiple packages


Read https://docs.conan.io/en/latest/reference/generators/cmake_find_package_multi.html


Document what we want in README.md:
- CMake find_package() COMPONENTS syntax
- Do not confuse with Conan components in package_info()
- Document how we could split Qt conan packages (could become a issue if..)


Idea:
make MdtConfig.cmake.in
from it, generate Mdt0Config.cmake or a other name ?
include it as a build-module in conan

