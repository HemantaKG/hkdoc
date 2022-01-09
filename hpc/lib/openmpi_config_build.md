## Install prerequired packages:
```bash
yum -y install gcc gcc-c++ gcc-gfortran kernel-devel
```

## Optional instalation(s)
```bash
yum group install "Development Tools"
```

## OpenMPI source configure and install
```bash
./configure --prefix=/share/openmpi --enable-mpi-fortran --enable-mpi-cxx
make
make install
```

## Add OpenMPI to system **PATH**:
```bash
nano /etc/bashrc

##OpenMPI2.0.4
export PATH="$PATH:/share/openmpi/bin"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/share/openmpi/lib/"
```

www.mpich.org (download OpenMPI tar file)
http://www.slothparadise.com/how-to-setup-mpi-on-centos-7-2-connected-virtual-machines-part-2/
