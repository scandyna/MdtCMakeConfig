from conans import ConanFile, CMake, tools
import os

class MdtCMakeConfigTestConan(ConanFile):
  settings = "os", "compiler", "build_type", "arch"
  generators = "cmake_paths"
  requires = "MdtCMakeConfig_Tests_ItemModel/0.0.0@scandyna/testing"

  def build(self):
    self.output.info("Building with cmake_paths")
    cmake = CMake(self)
    cmake.definitions["CMAKE_MESSAGE_LOG_LEVEL"] = "DEBUG"
    cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = "%s/conan_paths.cmake" % (self.build_folder)
    cmake.configure()

  def test(self):
    cmake = CMake(self)
    # We have no test to run, here we fake a bit..
