# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.14)

##################################################################
# Project definition with versionning got from git tag or by Conan
##################################################################

# TODO: implement !

project(MdtCMakeConfig)


option(BUILD_TESTS "Build the tests" OFF)

if(BUILD_TESTS)
  enable_testing()
  add_subdirectory(tests)
endif()

