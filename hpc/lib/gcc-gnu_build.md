=== GCC-GNU installation (gcc-7-1-0 version) ===
gmp, mpfr, mpc are required for GCC source installation

== gmp-4.3.2.tar.bz2 INSTALLATION:==
<code>
wget https://ftp.gnu.org/gnu/gmp/gmp-4.3.2.tar.bz2
tar xfj gmp-4.3.2.tar.bz2
cd gmp-4.3.2
./configure --prefix=/home/hemanta/opt/gmp-4.3.2
make
make check
make install
</code>

==mpfr-2.4.2.tar.bz2 INSTALLATION:==
<code>
wget --no-check-certificate https://www.mpfr.org/mpfr-2.4.2/mpfr-2.4.2.tar.bz2
tar xfj mpfr-2.4.2.tar.bz2
cd mpfr-2.4.2
./configure --prefix=/home/hemanta/opt/mpfr-2.4.2 --with-gmp=/home/hemanta/opt/gmp-4.3.2/
make
make check
make install
</code>

==mpc-0.8.1.tar.gz INSTALLATION:==
<code>
wget https://mirror.math.princeton.edu/pub/gcc/infrastructure/mpc-0.8.1.tar.gz
tar -xzvf mpc-0.8.1.tar.gz
cd mpc-0.8.1
./configure --prefix=/home/hemanta/opt/mpc-0.8.1 --with-gmp=/home/hemanta/opt/gmp-4.3.2/ --with-mpfr=/home/hemanta/opt/mpfr-2.4.2/
make
make check
make install
</code>

==gcc-4.8.1.tar.gz INSTALLATION:==
<code>
wget http://mirrors-usa.go-parts.com/gcc/releases/gcc-4.8.1/gcc-4.8.1.tar.gz
tar xzvf gcc-4.8.1.tar.gz
cd gcc-4.8.1
mkdir build-gcc
cd build-gcc
../configure --prefix=/home/hemanta/opt/gcc-4.8.1 --with-mpfr=/home/hemanta/opt/mpfr-2.4.2 --with-mpc=/home/hemanta/opt/mpc-0.8.1 --with-gmp=/home/hemanta/opt/gmp-4.3.2 --disable-multilib
make -j4
make install
</code>

EXPORT GCC 4.8.1 PATH(s):
<code>
export PATH=/home/hemanta/opt/gcc-4.8.1/bin:/home/hemanta/opt/gcc-4.8.1/include:$PATH
export LD_LIBRARY_PATH=/home/hemanta/opt/gcc-4.8.1/lib64:/home/hemanta/opt/gcc-4.8.1/lib:$LD_LIBRARY_PATH
</code>

  - REF: https://gcc.gnu.org/install/
  - REF: [[https://ftp.gnu.org/gnu/gcc/|gcc source download link]]
  - REF: [[https://linuxcluster.wordpress.com/2013/07/07/compiling-gnu-4-8-1-on-centos-6/|]]
  - REF: [[https://gcc.gnu.org/install/configure.html|]]
  - REF: [[http://www.linuxfromscratch.org/lfs/view/7.4/chapter06/gcc.html|]]