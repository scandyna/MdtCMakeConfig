from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout
from conan.tools.files import copy
import os

class MdtCMakeConfigConan(ConanFile):
  name = "mdtcmakeconfig"
  license = "BSD 3-Clause"
  url = "https://gitlab.com/scandyna/mdtcmakeconfig"
  description = "Global scope MdtConfig.cmake used in \"Multi Dev Tools\" projects"
  # We use CMake to configure/build/(test)/install
  # We also have dependencies we manage with Conan
  # We then use CMakeDeps and CMakeToolchain generators.
  # This requires the settings.
  # We will remove them in the package_id()
  # See: https://docs.conan.io/2/tutorial/creating_packages/other_types_of_packages/header_only_packages.html
  settings = "os", "arch", "compiler", "build_type"
  generators = "CMakeDeps", "VirtualBuildEnv"

  # See: https://docs.conan.io/en/latest/reference/conanfile/attributes.html#short-paths
  # Should only be enabled if building with MSVC on Windows causes problems
  short_paths = False

  def set_version(self):
    if not self.version:
      self.version = "0.0.0"

  def build_requirements(self):
    self.test_requires("MdtCMakeModules/0.19.3@scandyna/testing")

  def export_sources(self):
    source_root = os.path.join(self.recipe_folder, "../../../")
    copy(self, "CMakeLists.txt", source_root, self.export_sources_folder)
    copy(self, "MdtConfig.cmake.in", source_root, self.export_sources_folder)
    copy(self, "conan-mdt-config.cmake.in", source_root, self.export_sources_folder)
    copy(self, "LICENSE", source_root, self.export_sources_folder)

  def layout(self):
    cmake_layout(self)

  def generate(self):
    tc = CMakeToolchain(self)
    tc.variables["FROM_CONAN_PROJECT_VERSION"] = self.version
    tc.variables["INSTALL_CONAN_PACKAGE_FILES"] = "ON"
    tc.generate()

  def build(self):
    cmake = CMake(self)
    cmake.configure()
    cmake.build()

  def package(self):
    cmake = CMake(self)
    cmake.install()

  def package_id(self):
    self.info.clear()

  def package_info(self):
    self.cpp_info.bindirs = []
    self.cpp_info.libdirs = []
    self.cpp_info.includedirs = []
    build_modules = ["conan-mdt0-config.cmake"]
    self.cpp_info.set_property("cmake_file_name", "Mdt0")
    self.cpp_info.set_property("cmake_build_modules", build_modules)
