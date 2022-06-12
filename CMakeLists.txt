# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.14)

# CMAKE_PREFIX_PATH is empty before any call to project()
# Because set_project_version() does not exist,
# we call the project command twice (is there a cleaner solution?)
project(MdtCMakeConfig)

##################################################################
# Project definition with versionning got from git tag or by Conan
##################################################################

find_package(Git REQUIRED)
find_package(MdtCMakeModules REQUIRED)

include(MdtVersionUtils)

message(STATUS "FROM_CONAN_PROJECT_VERSION: ${FROM_CONAN_PROJECT_VERSION}")

set(INITIAL_PROJECT_VERSION)
if(FROM_CONAN_PROJECT_VERSION)
  set(INITIAL_PROJECT_VERSION ${FROM_CONAN_PROJECT_VERSION})
else()
  mdt_cmake_project_version_from_git_tag(INITIAL_PROJECT_VERSION DEFAULT_VERSION 0.0.1)
endif()

project(MdtCMakeConfig VERSION ${INITIAL_PROJECT_VERSION})

unset(INITIAL_PROJECT_VERSION)

message(STATUS "PROJECT_VERSION: ${PROJECT_VERSION}")

#######################
# Options
#######################

option(BUILD_TESTS "Build the tests" OFF)
option(INSTALL_CONAN_PACKAGE_FILES "Install files required for recent conan generators, like CMakeDeps" OFF)

if(BUILD_TESTS)
  enable_testing()
  add_subdirectory(tests)
endif()

#######################
# Install
#######################

set(MDT_INSTALL_PACKAGE_NAME Mdt${PROJECT_VERSION_MAJOR})
include(GNUInstallDirs)
include(MdtInstallDirs)

set(MDT_CMAKE_MODULE_INSTALL_CONFIG_DIR "${MDT_INSTALL_DATADIR}/cmake")

function(mdt_install_mdt_config)

  set(options)
  set(oneValueArgs COMPONENTS_RELATIVE_PATH DESTINATION)
  set(multiValueArgs)
  cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  if(NOT ARG_COMPONENTS_RELATIVE_PATH)
    message(FATAL_ERROR "mdt_install_mdt_config(): mandatory argument COMPONENTS_RELATIVE_PATH missing")
  endif()
  if(NOT ARG_DESTINATION)
    message(FATAL_ERROR "mdt_install_mdt_config(): mandatory argument DESTINATION missing")
  endif()
  if(ARG_UNPARSED_ARGUMENTS)
    message(FATAL_ERROR "mdt_install_mdt_config(): unknown arguments passed: ${ARG_UNPARSED_ARGUMENTS}")
  endif()

  set(packageConfigFile "${CMAKE_CURRENT_BINARY_DIR}/${ARG_DESTINATION}/Mdt${PROJECT_VERSION_MAJOR}Config.cmake")

  set(MDT_CONFIG_INSTALL_NAMESPACE Mdt${PROJECT_VERSION_MAJOR})
  set(MDT_CONFIG_COMPONENTS_RELATIVE_PATH "${ARG_COMPONENTS_RELATIVE_PATH}")

  include(CMakePackageConfigHelpers)

  configure_package_config_file(MdtConfig.cmake.in
    "${packageConfigFile}"
    NO_SET_AND_CHECK_MACRO
    NO_CHECK_REQUIRED_COMPONENTS_MACRO
    INSTALL_DESTINATION "${ARG_DESTINATION}"
  )

  install(
    FILES "${packageConfigFile}"
    DESTINATION "${ARG_DESTINATION}"
  )

endfunction()

mdt_install_mdt_config(
  COMPONENTS_RELATIVE_PATH ..
  DESTINATION "${MDT_CMAKE_MODULE_INSTALL_CONFIG_DIR}"
)

if(INSTALL_CONAN_PACKAGE_FILES)
  mdt_install_mdt_config(
    COMPONENTS_RELATIVE_PATH .
    DESTINATION "conan"
  )
endif()
