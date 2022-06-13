from conans import ConanFile, CMake, tools
import os

class MdtCMakeConfigTestConan(ConanFile):
  settings = "os", "compiler", "build_type", "arch"
  generators = "cmake_find_package_multi"
  requires = "MdtCMakeConfig_Tests_ItemModel/0.0.0@scandyna/testing"

  def build(self):
    cmake = CMake(self)
    cmake.definitions["CMAKE_MESSAGE_LOG_LEVEL"] = "DEBUG"
    cmake.configure(source_folder="../test_package")
    cmake.build()

  def test(self):
    cmake = CMake(self)
    # We have no test to run, here we fake a bit..
