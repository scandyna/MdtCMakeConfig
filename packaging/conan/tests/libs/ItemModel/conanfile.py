from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain
import os

class MdtCMakeConfigTestsItemModelConan(ConanFile):
  name = "MdtCMakeConfig_Tests_ItemModel"
  version = "0.0.0"
  license = "BSD 3-Clause"
  url = "https://gitlab.com/scandyna/mdtcmakeconfig"
  description = "Test library for MdtCMakeConfig"
  # Using CMakeToolchain and the new CMake helper
  # should help to have a more unified build.
  # But, it requires the settings.
  # So, add them here and erase them in the package_id()
  settings = "os", "arch", "compiler", "build_type"
  requires = "MdtCMakeConfig/0.0.0@scandyna/testing"
  generators = "CMakeToolchain"

  # The export exports_sources attributes does not work if the conanfile.py is in a sub-folder.
  # See https://github.com/conan-io/conan/issues/3635
  # and https://github.com/conan-io/conan/pull/2676
  def export_sources(self):
    self.copy("*", src="../../../../../tests/libs/ItemModel", dst=".")

  #def generate(self):
    #tc = CMakeToolchain(self)
    #tc.variables["FROM_CONAN_PROJECT_VERSION"] = self.version
    #tc.variables["INSTALL_CONAN_PACKAGE_FILES"] = "ON"
    #tc.generate()

  def build(self):
    cmake = CMake(self)
    cmake.configure()
    cmake.build()

  def package(self):
    cmake = CMake(self)
    cmake.install()

  def package_id(self):
    self.info.header_only()

  def package_info(self):

    self.cpp_info.includedirs = []
    build_modules = ["mdtcmakeconfig-conan-cmake-modules.cmake"]

    # This will be used by CMakeDeps
    #self.cpp_info.set_property("cmake_build_modules", build_modules)

    # This must be added for other generators
    #self.cpp_info.build_modules["cmake_find_package"] = build_modules
    #self.cpp_info.build_modules["cmake_find_package_multi"] = build_modules
