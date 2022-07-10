from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain
import os

class MdtCMakeConfigTestsUserAppConan(ConanFile):
  name = "MdtCMakeConfig_Tests_UserApp"
  version = "0.0.0"
  license = "BSD 3-Clause"
  url = "https://gitlab.com/scandyna/mdtcmakeconfig"
  description = "Test user app for MdtCMakeConfig"
  settings = "os", "arch", "compiler", "build_type"
  generators = "CMakeToolchain", "CMakeDeps"

  def requirements(self):
    self.requires("MdtCMakeConfig_Tests_ItemModel/0.0.0@scandyna/testing")

  def export_sources(self):
    self.copy("CMakeLists.txt")

  #def generate(self):
    #tc = CMakeToolchain(self)
    #tc.variables["FROM_CONAN_PROJECT_VERSION"] = self.version
    #tc.variables["INSTALL_CONAN_PACKAGE_FILES"] = "ON"
    #tc.generate()

  def build(self):
    cmake = CMake(self)
    cmake.configure()
    cmake.build()
