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
  generators = "CMakeToolchain"

  def requirements(self):
    self.requires("MdtCMakeConfig/0.0.0@scandyna/testing")

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

    self.cpp_info.set_property("cmake_file_name", "Mdt0ItemModel")

    self.cpp_info.names["cmake_find_package"] = "Mdt0ItemModel"
    self.cpp_info.names["cmake_find_package_multi"] = "Mdt0ItemModel"

    self.cpp_info.set_property("cmake_target_name", "Mdt0::ItemModel")
