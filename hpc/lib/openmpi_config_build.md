  - Ref1: www.mpich.org (download OpenMPI tar file)
  - Ref2: http://www.slothparadise.com/how-to-setup-mpi-on-centos-7-2-connected-virtual-machines-part-2/

Install prerequired packages:
<code>
yum -y install gcc gcc-c++ gcc-gfortran kernel-devel
## Optional instalation(s)
yum group install "Development Tools"
</code>
OpenMPI source configure and install:
<code>
./configure --prefix=/share/openmpi --enable-mpi-fortran --enable-mpi-cxx
make
make install
</code>
Add OpenMPI to system **PATH**:
<code>
nano /etc/bashrc

##OpenMPI2.0.4
export PATH="$PATH:/share/openmpi/bin"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/share/openmpi/lib/"
</code>