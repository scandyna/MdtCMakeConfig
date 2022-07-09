
cmake_minimum_required(VERSION 3.15)

project(MdtCMakeConfigTest)

if(EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
  include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
  conan_basic_setup(NO_OUTPUT_DIRS)
endif()

message(DEBUG "CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
message(DEBUG "calling find_package(Mdt0 REQUIRED COMPONENTS ItemModel) ...")

find_package(Mdt0 REQUIRED COMPONENTS ItemModel NO_SYSTEM_ENVIRONMENT_PATH NO_CMAKE_PACKAGE_REGISTRY NO_CMAKE_SYSTEM_PATH)

message(DEBUG "find_package() DONE")
message(DEBUG "CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")

message(STATUS "Mdt0_FOUND: ${Mdt0_FOUND}")
message(STATUS "Mdt0_DIR: ${Mdt0_DIR}")
message(STATUS "Mdt0ItemModel_DIR: ${Mdt0ItemModel_DIR}")

if(NOT Mdt0ItemModel_FOUND)
  message(FATAL_ERROR "Test failed: Mdt0ItemModel not found using find_package(Mdt0 REQUIRED COMPONENTS ItemModel)")
endif()

# Check that Mdt0_FOUND is false if a component was not found
# See https://gitlab.com/scandyna/mdtcmakeconfig/-/issues/1

message(DEBUG "calling find_package(Mdt0 COMPONENTS NonExistingComponent) ...")
find_package(Mdt0 COMPONENTS NonExistingComponent NO_SYSTEM_ENVIRONMENT_PATH NO_CMAKE_PACKAGE_REGISTRY NO_CMAKE_SYSTEM_PATH)
message(DEBUG "find_package() DONE , Mdt0_FOUND: ${Mdt0_FOUND}")

if(Mdt0_FOUND)
  message(FATAL_ERROR "Test failed: find_package(Mdt0 COMPONENTS NonExistingComponent) should not set Mdt0_FOUND to TRUE")
endif()
