# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

###################################
# Install MdtCMakeConfig
# Will be used by several tests
###################################

add_test(NAME MdtCMakeConfig_Configure
  COMMAND "${CMAKE_COMMAND}"
    -S "${CMAKE_SOURCE_DIR}"
    -B "${CMAKE_CURRENT_BINARY_DIR}/build/MdtCMakeConfig"
    -G "${CMAKE_GENERATOR}"
    -A "${CMAKE_GENERATOR_PLATFORM}"
    -T "${CMAKE_GENERATOR_TOOLSET}"
    -DCMAKE_MESSAGE_LOG_LEVEL=DEBUG
    "-DCMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}"
    "-DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_BINARY_DIR}/myHome/opt/MdtCMakeConfig"
)

add_test(NAME MdtCMakeConfig_Build
  COMMAND "${CMAKE_COMMAND}"
    --build "${CMAKE_CURRENT_BINARY_DIR}/build/MdtCMakeConfig"
    --config $<CONFIG>
)
set_tests_properties(MdtCMakeConfig_Build PROPERTIES DEPENDS MdtCMakeConfig_Configure)

add_test(NAME MdtCMakeConfig_Install
  COMMAND "${CMAKE_COMMAND}"
    --install "${CMAKE_CURRENT_BINARY_DIR}/build/MdtCMakeConfig"
    --config $<CONFIG>
)
set_tests_properties(MdtCMakeConfig_Install PROPERTIES DEPENDS MdtCMakeConfig_Build)

###################################
# Build and install MdtItemModel
###################################

add_test(NAME MdtItemModel_Configure
  COMMAND "${CMAKE_COMMAND}"
    -S "${CMAKE_SOURCE_DIR}/tests/libs/ItemModel"
    -B "${CMAKE_CURRENT_BINARY_DIR}/build/libs/ItemModel"
    -G "${CMAKE_GENERATOR}"
    -A "${CMAKE_GENERATOR_PLATFORM}"
    -T "${CMAKE_GENERATOR_TOOLSET}"
    -DCMAKE_MESSAGE_LOG_LEVEL=DEBUG
    "-DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_BINARY_DIR}/myHome/opt/MdtItemModel"
)

add_test(NAME MdtItemModel_Build
  COMMAND "${CMAKE_COMMAND}"
    --build "${CMAKE_CURRENT_BINARY_DIR}/build/libs/ItemModel"
    --config $<CONFIG>
)
set_tests_properties(MdtItemModel_Build PROPERTIES DEPENDS MdtItemModel_Configure)

add_test(NAME MdtItemModel_Install
  COMMAND "${CMAKE_COMMAND}"
    --install "${CMAKE_CURRENT_BINARY_DIR}/build/libs/ItemModel"
    --config $<CONFIG>
)
set_tests_properties(MdtItemModel_Install PROPERTIES DEPENDS MdtItemModel_Build)

###################################
# Build the user project
###################################

add_test(NAME UserProject_Configure
  COMMAND "${CMAKE_COMMAND}"
    -S "${CMAKE_SOURCE_DIR}/tests/UserProject"
    -B "${CMAKE_CURRENT_BINARY_DIR}/build/UserProject"
    -G "${CMAKE_GENERATOR}"
    -A "${CMAKE_GENERATOR_PLATFORM}"
    -T "${CMAKE_GENERATOR_TOOLSET}"
    -DCMAKE_MESSAGE_LOG_LEVEL=DEBUG
    "-DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_BINARY_DIR}/myHome/opt/UserProject"
    "-DCMAKE_PREFIX_PATH=${CMAKE_CURRENT_BINARY_DIR}/myHome/opt/MdtCMakeConfig;${CMAKE_CURRENT_BINARY_DIR}/myHome/opt/MdtItemModel"
)
set_tests_properties(UserProject_Configure PROPERTIES DEPENDS "MdtItemModel_Install;MdtCMakeConfig_Install")
