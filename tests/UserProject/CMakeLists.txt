
cmake_minimum_required(VERSION 3.15)

project(UserProject)

find_package(Mdt0 REQUIRED COMPONENTS ItemModel NO_SYSTEM_ENVIRONMENT_PATH NO_CMAKE_PACKAGE_REGISTRY NO_CMAKE_SYSTEM_PATH)

message(DEBUG "Mdt0_FOUND: ${Mdt0_FOUND}")
message(DEBUG "Mdt0ItemModel_FOUND: ${Mdt0ItemModel_FOUND}")

if(NOT Mdt0ItemModel_FOUND)
  message(FATAL_ERROR "Test failed: Mdt0ItemModel not found using find_package(Mdt0 REQUIRED COMPONENTS ItemModel)")
endif()
