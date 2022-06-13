
# This file is only used by conan generators that generates CMake package config files
# (like CMakeDeps)

# We have to add the root of the package to CMAKE_PREFIX_PATH (if not already exists)
# so that find_package() can find MdtvConfig.cmake.
# This file is installed at the root of the package
# (see the conanfile.py)

# TODO: use XXX_mdt_find_path_in_list() !

# TODO: probably not usefull !!

# message("*** adding ${CMAKE_CURRENT_LIST_DIR} to CMAKE_PREFIX_PATH")
# 
# list(PREPEND CMAKE_PREFIX_PATH "${CMAKE_CURRENT_LIST_DIR}")

# message("*** set Mdt0_DIR to ${CMAKE_CURRENT_LIST_DIR}/conan")
# 
# set(Mdt0_DIR "${CMAKE_CURRENT_LIST_DIR}/conan")

message("*** include ${CMAKE_CURRENT_LIST_DIR}/conan/Mdt0Config.cmake")

include("${CMAKE_CURRENT_LIST_DIR}/conan/Mdt0Config.cmake")

# set(Mdt0_DIR "${CMAKE_CURRENT_LIST_DIR}/conan")
