from conan import ConanFile
from conan.tools.env import VirtualBuildEnv
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake

# This file is only to install dependencies when woring on the project
# Packages recipes are in packaging/conan/
class MdtCMakeConfigConan(ConanFile):
  name = "mdtcmakeconfig"
  license = "BSD 3-Clause"
  url = "https://gitlab.com/scandyna/mdtcmakeconfig"
  description = "Global scope MdtConfig.cmake used in \"Multi Dev Tools\" projects"
  settings = "os", "arch", "compiler", "build_type"
  options = {"shared": [True, False]}
  default_options = {"shared": True}
  generators = "CMakeDeps", "VirtualBuildEnv"

  def build_requirements(self):
    self.test_requires("MdtCMakeModules/0.19.3@scandyna/testing")

  def generate(self):
    tc = CMakeToolchain(self)
    #tc.variables["FROM_CONAN_PROJECT_VERSION"] = self.version
    #tc.variables["INSTALL_CONAN_PACKAGE_FILES"] = "ON"
    tc.generate()
