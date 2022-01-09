# Cmake Build from Source
## Download source, compile and install
Note: [Ref install with ccmake](https://askubuntu.com/questions/736198/how-to-install-cmake-ccmake-from-source)
Install following package if you want to ''ccmake'' otherwise not required
```bash
apt-get install libncurses5-dev
```
## Configure, Compile and Install
```bash
wget https://cmake.org/files/v3.12/cmake-3.12.1.tar.gz
tar -xzvf cmake-3.12.1.tar.gz
cd cmake-3.12.1

./configure --prefix=/opt/cmake
make
make install
```
## Why cmake?
CMake is an open-source, cross-platform family of tools designed to build, test and package software. CMake is used to control the software compilation process using simple platform and compiler independent configuration files, and generate native makefiles and workspaces that can be used in the compiler environment of your choice. The suite of CMake tools were created by Kitware in response to the need for a powerful, cross-platform build environment for open-source projects such as ITK and VTK

## Reference
[](https://geeksww.com/tutorials/operating_systems/linux/installation/downloading_compiling_and_installing_cmake_on_linux.php)
[](https://cmake.org/)
