[[_TOC_]]

# Introduction

Without a package manager,
each dependency is installed to some location.

The user project then has to pass the location
of each one to `CMAKE_PREFIX_PATH`.

Example:
```
~/opt
   |-MdtCMakeConfig
   |    |-cmake
   |        |-Mdt0Config.cmake
   |-MdtItemModel
        |-lib
           |-cmake
               |-Mdt0ItemModel
                    |-Mdt0ItemModelConfig.cmake
```

From the user project:
```bash
cmake -DCMAKE_PREFIX_PATH="/home/user/opt/MdtCMakeConfig;/home/user/opt/MdtItemModel" ..
```

# Monolitic distribution

The idea is to install Mdt libraries like Qt:
```
~/opt
   |-multidevtools
        |-Mdt0.1.2
           |-gcc_64
               |-lib
                  |-cmake
                      |-Mdt0
                      |  |-Mdt0Config.cmake
                      |-Mdt0ItemModel
                      |  |-Mdt0ItemModelConfig.cmake
```

From the user project:
```bash
cmake -DCMAKE_PREFIX_PATH="/home/user/opt/multidevtools/Mdt0.1.2/gcc_64" ..
```

This would require a adaptation in MdtCMakeConfig to install
`Mdt0Config.cmake` also in the lib subdirectory.

Some other libraries must potentially be adapted.

Then, all libraries must be installed to the same location:
```bash
cmake -DCMAKE_INSTALL_PREFIX="/home/user/opt/multidevtools/Mdt0.1.2/gcc_64" ..
```

This is currently not supported.
and it probably won't be.

A package manager should really be used,
because it solves a lot of problems,
like multiple binary/builds, transitive dependencies, etc...
