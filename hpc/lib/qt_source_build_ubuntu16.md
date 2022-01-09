# Compile Qt source code and install
## Basic steps
Here are the basic steps for building Qt on any platform
* 64-bit Ubuntu desktop Linux version 16.04
* Download the source code archive
* Extract the source code into a working directory
* Install the required development packages and other build dependencies for Qt
* Configure Qt for the desired options and ensure that all dependencies are met
* Build Qt (i.e. compile and link)
* Install and test the new version

## Download the source code
download the file directly from the Linux command line from http://download.qt.io/archive/qt/5.11/5.11.1/single/|link
```bash
wget http://download.qt.io/archive/qt/5.11/5.11.1/single/qt-everywhere-src-5.11.1.tar.xz
```

## Extract the source code into a working directory
```bash
tar -xf qt-everywhere-src-5.11.1.tar.xz
cd qt-everywhere-src-5.11.1
```

## Install the required development packages and other build dependencies for Qt
Qt is dependent on a number of tools and libraries
```bash
sudo apt-get install bison build-essential flex gperf ibgstreamer-plugins-base0.10-dev libasound2-dev libatkmm-1.6-dev libbz2-dev libcap-dev libcups2-dev libdrm-dev libegl1-mesa-dev libfontconfig1-dev libfreetype6-dev libgcrypt11-dev libglu1-mesa-dev libgstreamer0.10-dev libicu-dev libnss3-dev libpci-dev libpulse-dev libssl-dev libudev-dev libx11-dev libx11-xcb-dev libxcb-composite0 libxcb-composite0-dev libxcb-cursor-dev libxcb-cursor0 libxcb-damage0 libxcb-damage0-dev libxcb-dpms0 libxcb-dpms0-dev libxcb-dri2-0 libxcb-dri2-0-dev libxcb-dri3-0 libxcb-dri3-dev libxcb-ewmh-dev libxcb-ewmh2 libxcb-glx0 libxcb-glx0-dev libxcb-icccm4 libxcb-icccm4-dev libxcb-image0 libxcb-image0-dev libxcb-keysyms1 libxcb-keysyms1-dev libxcb-present-dev libxcb-present0 libxcb-randr0 libxcb-randr0-dev libxcb-record0 libxcb-record0-dev libxcb-render-util0 libxcb-render-util0-dev libxcb-render0 libxcb-render0-dev libxcb-res0 libxcb-res0-dev libxcb-screensaver0 libxcb-screensaver0-dev libxcb-shape0 libxcb-shape0-dev libxcb-shm0 libxcb-shm0-dev libxcb-sync-dev libxcb-sync0-dev libxcb-sync1 libxcb-util-dev libxcb-util0-dev libxcb-util1 libxcb-xevie0 libxcb-xevie0-dev libxcb-xf86dri0 libxcb-xf86dri0-dev libxcb-xfixes0 libxcb-xfixes0-dev libxcb-xinerama0 libxcb-xinerama0-dev libxcb-xkb-dev libxcb-xkb1 libxcb-xprint0 libxcb-xprint0-dev libxcb-xtest0 libxcb-xtest0-dev libxcb-xv0 libxcb-xv0-dev libxcb-xvmc0 libxcb-xvmc0-dev libxcb1 libxcb1-dev libxcomposite-dev libxcursor-dev libxdamage-dev libxext-dev libxfixes-dev libxi-dev libxrandr-dev libxrender-dev libxslt-dev libxss-dev libxtst-dev perl python ruby
```

## Configure Qt for the desired options and ensure that all dependencies are meet
configure, compile, link amd install Qt
```bash
./configure --prefix=/home/hemanta.kumar/opt
make -j4
make install
```
Built the documentation, which will be available from Qt Assistant. We can build and install it as follows
```bash
make docs
make install_docs
```

## Launch Qt Assistant
```bash
/home/hemanta.kumar/opt/qt/bin/assistant
```

## Why would you want to build Qt from source
* you may want to build Qt using a different configuration
* you may want to enable or disable different options or modules to match the requirements of your platform and application
* you may need to build Qt against a different C++ compiler or run-time library
* you may want to test an Alpha release of Qt, these are typically only provided as source code
* You may also want to build Qt from a development version in the git repository, which only provides source code

# Reference
https://www.ics.com/blog/how-compile-qt-source-code-linux
