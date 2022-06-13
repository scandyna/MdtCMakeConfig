
cmake_minimum_required(VERSION 3.15)

project(MdtCMakeConfigTest)

if(EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
  include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
  conan_basic_setup(NO_OUTPUT_DIRS)
endif()

message(DEBUG "CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
message(DEBUG "calling find_package() ...")

find_package(Mdt0 REQUIRED COMPONENTS ItemModel NO_SYSTEM_ENVIRONMENT_PATH NO_CMAKE_PACKAGE_REGISTRY NO_CMAKE_SYSTEM_PATH)

message(DEBUG "find_package() DONE")
message(DEBUG "CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")

message(STATUS "Mdt0_DIR: ${Mdt0_DIR}")
message(STATUS "Mdt0ItemModel_DIR: ${Mdt0ItemModel_DIR}")

if(NOT Mdt0ItemModel_FOUND)
  message(FATAL_ERROR "Test failed: Mdt0ItemModel not found using find_package(Mdt0 REQUIRED COMPONENTS ItemModel)")
endif()
