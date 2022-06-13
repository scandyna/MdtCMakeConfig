from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
import os

class MdtCMakeConfigTestConan(ConanFile):
  settings = "os", "compiler", "build_type", "arch"
  generators = "CMakeToolchain", "CMakeDeps"
  requires = "MdtCMakeConfig_Tests_ItemModel/0.0.0@scandyna/testing"


  # TODO: try source() method ?
  def layout(self):
    cmake_layout(self, src_folder="../test_package")

  def generate(self):
    tc = CMakeToolchain(self)
    tc.variables["CMAKE_SOURCE_DIR"] = "../test_package"
    tc.variables["CMAKE_MESSAGE_LOG_LEVEL"] = "DEBUG"
    tc.generate()

  def build(self):
    cmake = CMake(self)
    cmake.configure()
    cmake.build()

  def test(self):
    cmake = CMake(self)
    # We have no test to run, here we fake a bit..
