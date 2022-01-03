===== Running Linpack (HPL) Test on Linux Cluster with OpenMPI =====
HPL is a software package that solves a (random) dense linear system in double precision (64 bits) arithmetic on distributed-memory computers. It can thus be regarded as a portable as well as the freely available implementation of the High-Performance Computing Linpack Benchmark.

The algorithm used by HPL can be summarized by the following keywords: Two-dimensional block-cyclic data distribution – Right-looking variant of the LU factorization with row partial pivoting featuring multiple look-ahead depths – Recursive panel factorization with pivot search and column broadcast combined – Various virtual panel broadcast topologies – bandwidth reducing swap-broadcast algorithm – backward substitution with look-ahead of depth 1.

Requirements:
  * [[openmpi_installation_and_configuration|OpenMPI]]
  * [[an_automated_benchmarking_tool_for_hpc_clusters#Building BLAS library|BLAS library]]
  * [[an_automated_benchmarking_tool_for_hpc_clusters#Building LAPACK library|LAPACK library]]
  * [[an_automated_benchmarking_tool_for_hpc_clusters#Building VSIPL library|VSIPL library]]
  * [[an_automated_benchmarking_tool_for_hpc_clusters#Compile and Build ATLAS library|ATLAS library]]
  * [[an_automated_benchmarking_tool_for_hpc_clusters#HPL package compile and run benchmarking|HPL package]]
==== Building OpenMPI ====
I am using [[https://www.open-mpi.org/software/ompi/v2.0/|OpenMPI 2.0.4]]
==== Building BLAS library ====
Download The [[http://www.netlib.org/blas/|current latest version of BLAS]], I am using BLAS 3.8.0 version.
<note>The BLAS (Basic Linear Algebra Subprograms) are routines that provide standard building blocks for performing basic vector and matrix operations. The Level 1 BLAS perform scalar, vector and vector-vector operations, the Level 2 BLAS perform matrix-vector operations, and the Level 3 BLAS perform matrix-matrix operations. Because the BLAS are efficient, portable, and widely available, they are commonly used in the development of high-quality linear algebra software, LAPACK for example.</note>
building BLAS library using ''mpifort'' compiler:
<code>
cd ~/src
wget http://www.netlib.org/blas/blas-3.8.0.tgz
tar -xzvf blas-3.8.0.tgz 
mv BLAS-3.8.0 BLAS
cd BLAS/
mpifort -O3 -std=legacy -m64 -fno-second-underscore -fPIC -c *.f
ar r libfblas.a *.o
ranlib libfblas.a
rm -rf *.o
export BLAS=~/src/BLAS/libfblas.a
ln -s libfblas.a libblas.a
</code>
==== Building LAPACK library ====
Download [[http://www.netlib.org/lapack/index.html#_lapack_version_3_8_0_2|current latest version of LAPACK]], I am using LAPACK 3.8.0 version
<note>
LAPACK is written in Fortran 90 and provides routines for solving systems of simultaneous linear equations, least-squares solutions of linear systems of equations, eigenvalue problems, and singular value problems. The associated matrix factorizations (LU, Cholesky, QR, SVD, Schur, generalized Schur) are also provided, as are related computations such as reordering of the Schur factorizations and estimating condition numbers. Dense and banded matrices are handled, but not general sparse matrices. In all areas, similar functionality is provided for real and complex matrices, in both single and double precision.

LAPACK relied on BLAS.
</note>
building LAPACK library using ''mpifort'' compiler*
<code>
cd src
wget http://www.netlib.org/lapack/lapack-3.8.0.tar.gz
tar -xzvf lapack-3.8.0.tar.gz 
cd lapack-3.8.0/
cp INSTALL/make.inc.gfortran make.inc
</code>
Edit PLAT, OPTS, NOOPT properties in LAPACK **make.inc** file
<code>
nano make.inc
  PLAT = _LINUX
  OPTS = -O2 -m64 -fPIC
  NOOPT = -m64 -fPIC
</code>
now make and export LAPACK library
<code>
make
export LAPACK=/home/hemanta.kumar/src/lapack-3.8.0/liblapack.a
</code>
==== Building VSIPL library ====
not done...
==== Compile and Build ATLAS library ====
Download [[https://sourceforge.net/projects/math-atlas/files/Stable/|current latest stable ATLAS library package]], I am using ATLAS 3.10.3 version
<note>
ATLAS The Automatically Tuned Linear Algebra Software (ATLAS) provides a complete implementation of the BLAS API 3 and a subset of LAPACK 3. A big number of instruction-set specific optimizations are used throughout the library to achieve peak-performance on a wide variety of HW-platforms.

ATLAS provides both C and Fortran interfaces.
</note>
building ATLAS library and add to your **LD_LIBRARY_PATH**
<code>
cd ~/src
wget wget https://sourceforge.net/projects/math-atlas/files/Stable/3.10.3/atlas3.10.3.tar.bz2
tar -xvjf atlas3.10.3.tar.bz2 
cd ATLAS/
mkdir ATLAS_BUILD
ATLAS_BUILD/
../configure --prefix=/home/hemanta.kumar/opt/atlas --cripple-atlas-performance
make
make check
make ptcheck
make time
make install
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/hemanta.kumar/opt/atlas/lib
</code>
<note important>
You need to turn off **CPU Throttling** to get better performace banchmarking report. To turn off CPU throotting use <code>/usr/bin/cpufreq-selector -g performance</code>

If you don't want to turn off CPU throttling and want to build ATLAS library use ''--cripple-atlas-performance'' option while running ATLAS **configure file**. Here I am compiling ATLAS library without turning off CPU throttling.

If you didn't turn off CPU throttling (or) not using the configure option, then configure will through error {{:atlas_library_configure_err.png?200|error}}

For more information:
  * [[http://linuxtoolkit.blogspot.com/2011/03/switching-off-cpu-throttling-on-centos.html|Switching off CPU Throttling on CentOS or Fedora]]
  * [[https://en.wikipedia.org/wiki/Dynamic_frequency_scaling|Dynamic frequency scaling]]
</note>
==== HPL package compile and run benchmarking ====
To compile HPL benchmarking package you need BLAS, LAPACK and ATLAS libraries. Download [[http://www.netlib.org/benchmark/hpl/|current latest HPL]], I am using HPL 2.2 benchmarking package.
compile HPL package
<code>
cd ~/src
wget http://www.netlib.org/benchmark/hpl/hpl-2.2.tar.gz
tar -xzvf hpl-2.2.tar.gz
mv hpl-2.2 hpl
cd hpl
</code>
check system architecture (useing ''arch'' (or) ''uname -a'') and copy appropreate make file from **~/hpl/setup/** derictory to **~/hpl/** derictory
<code>
cp setup/Make.Linux_PII_CBLAS Make.Linux_Intel64
nano Make.Linux_Intel64
</code>
<file make Make.Linux_Intel64>
#  
#  -- High Performance Computing Linpack Benchmark (HPL)                
#     HPL - 2.2 - February 24, 2016                          
#     Antoine P. Petitet                                                
#     University of Tennessee, Knoxville                                
#     Innovative Computing Laboratory                                 
#     (C) Copyright 2000-2008 All Rights Reserved                       
#                                                                       
#  -- Copyright notice and Licensing terms:                             
#                                                                       
#  Redistribution  and  use in  source and binary forms, with or without
#  modification, are  permitted provided  that the following  conditions
#  are met:                                                             
#                                                                       
#  1. Redistributions  of  source  code  must retain the above copyright
#  notice, this list of conditions and the following disclaimer.        
#                                                                       
#  2. Redistributions in binary form must reproduce  the above copyright
#  notice, this list of conditions,  and the following disclaimer in the
#  documentation and/or other materials provided with the distribution. 
#                                                                       
#  3. All  advertising  materials  mentioning  features  or  use of this
#  software must display the following acknowledgement:                 
#  This  product  includes  software  developed  at  the  University  of
#  Tennessee, Knoxville, Innovative Computing Laboratory.             
#                                                                       
#  4. The name of the  University,  the name of the  Laboratory,  or the
#  names  of  its  contributors  may  not  be used to endorse or promote
#  products  derived   from   this  software  without  specific  written
#  permission.                                                          
#                                                                       
#  -- Disclaimer:                                                       
#                                                                       
#  THIS  SOFTWARE  IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES,  INCLUDING,  BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE UNIVERSITY
#  OR  CONTRIBUTORS  BE  LIABLE FOR ANY  DIRECT,  INDIRECT,  INCIDENTAL,
#  SPECIAL,  EXEMPLARY,  OR  CONSEQUENTIAL DAMAGES  (INCLUDING,  BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA OR PROFITS; OR BUSINESS INTERRUPTION)  HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT,  STRICT LIABILITY,  OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
# ######################################################################
#  
# ----------------------------------------------------------------------
# - shell --------------------------------------------------------------
# ----------------------------------------------------------------------
#
SHELL        = /bin/sh
#
CD           = cd
CP           = cp
LN_S         = ln -s
MKDIR        = mkdir
RM           = /bin/rm -f
TOUCH        = touch
#
# ----------------------------------------------------------------------
# - Platform identifier ------------------------------------------------
# ----------------------------------------------------------------------
#
ARCH         = Linux_Intel64
#
# ----------------------------------------------------------------------
# - HPL Directory Structure / HPL library ------------------------------
# ----------------------------------------------------------------------
#
TOPdir       = $(HOME)/hpl
INCdir       = $(TOPdir)/include
BINdir       = $(TOPdir)/bin/$(ARCH)
LIBdir       = $(TOPdir)/lib/$(ARCH)
#
HPLlib       = $(LIBdir)/libhpl.a 
#
# ----------------------------------------------------------------------
# - Message Passing library (MPI) --------------------------------------
# ----------------------------------------------------------------------
# MPinc tells the  C  compiler where to find the Message Passing library
# header files,  MPlib  is defined  to be the name of  the library to be
# used. The variable MPdir is only used for defining MPinc and MPlib.
#
MPdir        = /share/openmpi
MPinc        = -I$(MPdir)/include
MPlib        = $(MPdir)/lib/libmpi.so
#
# ----------------------------------------------------------------------
# - Linear Algebra library (BLAS or VSIPL) -----------------------------
# ----------------------------------------------------------------------
# LAinc tells the  C  compiler where to find the Linear Algebra  library
# header files,  LAlib  is defined  to be the name of  the library to be
# used. The variable LAdir is only used for defining LAinc and LAlib.
#
LAdir        = $(HOME)/opt/atlas/lib
LAinc        =
LAlib        = $(LAdir)/libcblas.a $(LAdir)/libatlas.a
#
# ----------------------------------------------------------------------
# - F77 / C interface --------------------------------------------------
# ----------------------------------------------------------------------
# You can skip this section  if and only if  you are not planning to use
# a  BLAS  library featuring a Fortran 77 interface.  Otherwise,  it  is
# necessary  to  fill out the  F2CDEFS  variable  with  the  appropriate
# options.  **One and only one**  option should be chosen in **each** of
# the 3 following categories:
#
# 1) name space (How C calls a Fortran 77 routine)
#
# -DAdd_              : all lower case and a suffixed underscore  (Suns,
#                       Intel, ...),                           [default]
# -DNoChange          : all lower case (IBM RS6000),
# -DUpCase            : all upper case (Cray),
# -DAdd__             : the FORTRAN compiler in use is f2c.
#
# 2) C and Fortran 77 integer mapping
#
# -DF77_INTEGER=int   : Fortran 77 INTEGER is a C int,         [default]
# -DF77_INTEGER=long  : Fortran 77 INTEGER is a C long,
# -DF77_INTEGER=short : Fortran 77 INTEGER is a C short.
#
# 3) Fortran 77 string handling
#
# -DStringSunStyle    : The string address is passed at the string loca-
#                       tion on the stack, and the string length is then
#                       passed as  an  F77_INTEGER  after  all  explicit
#                       stack arguments,                       [default]
# -DStringStructPtr   : The address  of  a  structure  is  passed  by  a
#                       Fortran 77  string,  and the structure is of the
#                       form: struct {char *cp; F77_INTEGER len;},
# -DStringStructVal   : A structure is passed by value for each  Fortran
#                       77 string,  and  the  structure is  of the form:
#                       struct {char *cp; F77_INTEGER len;},
# -DStringCrayStyle   : Special option for  Cray  machines,  which  uses
#                       Cray  fcd  (fortran  character  descriptor)  for
#                       interoperation.
#
F2CDEFS      =
#
# ----------------------------------------------------------------------
# - HPL includes / libraries / specifics -------------------------------
# ----------------------------------------------------------------------
#
HPL_INCLUDES = -I$(INCdir) -I$(INCdir)/$(ARCH) $(LAinc) $(MPinc)
HPL_LIBS     = $(HPLlib) $(LAlib) $(MPlib)
#
# - Compile time options -----------------------------------------------
#
# -DHPL_COPY_L           force the copy of the panel L before bcast;
# -DHPL_CALL_CBLAS       call the cblas interface;
# -DHPL_CALL_VSIPL       call the vsip  library;
# -DHPL_DETAILED_TIMING  enable detailed timers;
#
# By default HPL will:
#    *) not copy L before broadcast,
#    *) call the BLAS Fortran 77 interface,
#    *) not display detailed timing information.
#
HPL_OPTS     = -DHPL_CALL_CBLAS
#
# ----------------------------------------------------------------------
#
HPL_DEFS     = $(F2CDEFS) $(HPL_OPTS) $(HPL_INCLUDES)
#
# ----------------------------------------------------------------------
# - Compilers / linkers - Optimization flags ---------------------------
# ----------------------------------------------------------------------
#
CC           = /share/openmpi/bin/mpicc
CCNOOPT      = $(HPL_DEFS)
CCFLAGS      = $(HPL_DEFS) -fomit-frame-pointer -O3 -funroll-loops
#
# On some platforms,  it is necessary  to use the Fortran linker to find
# the Fortran internals used in the BLAS library.
#
LINKER       = /share/openmpi/bin/mpicc
LINKFLAGS    = $(CCFLAGS)
#
ARCHIVER     = ar
ARFLAGS      = r
RANLIB       = echo
#
# ----------------------------------------------------------------------
</file>
make the HPL
<code>
make arch=Linux_Intel64
</code>
running the **LinPack** on multiple Nodes
<code>
cd ~/hpl/bin/Linux.Intel64
mpirun --hostfile /home/hemanta.kumar/my_hostfile -np 32 -H cn1,cn2,cn3,cn4 ./xhpl
</code>
HPL run results: {{:hpl_test_result.png?200|output}}
==== Reference ====
  * [[https://www.hpcwire.com/2011/02/23/clusternumbers_an_automated_benchmarking_tool_for_hpc_clusters/|An Automated Benchmarking Tool for HPC Clusters]]
  * [[https://linuxcluster.wordpress.com/2013/02/28/running-linpack-hpl-test-on-linux-cluster-with-openmpi-and-intel-compilers/|Running Linpack (HPL) Test on Linux Cluster with OpenMPI and Intel Compilers]]
<note>The classical Linpack measures floating point operations per second (FLOPS) across the whole cluster. HPL is a software package that solves a (random) dense linear system in double precision (64 bits) arithmetic on distributed-memory computers. It can thus be regarded as a portable as well as the freely available implementation of the High-Performance Computing Linpack Benchmark</note>
  * [[https://www.spec.org/|Standard Performance Evaluation Corporation (SPEC)]]
<note>The Standard Performance Evaluation Corporation (SPEC) is a non-profit corporation formed to establish, maintain and endorse standardized benchmarks and tools to evaluate performance and energy efficiency for the newest generation of computing systems. SPEC develops benchmark suites and also reviews and publishes submitted results.</note>
  * [[https://linuxcluster.wordpress.com/2012/04/08/building-blas-library-using-intel-and-gnu-compiler/|Building BLAS Library using Intel and GNU Compiler]]
  * [[https://linuxcluster.wordpress.com/2012/04/09/building-lapack-3-4-with-intel-and-gnu-compiler/|Building LAPACK 3.4 with Intel and GNU Compiler]]
  * [[https://linuxcluster.wordpress.com/2011/03/25/compiling-atlas-on-centos5/|Compiling ATLAS on CentOS 5]]
  * [[https://linuxcluster.wordpress.com/2010/05/28/building-openmpi-with-intel-compilers/|Building OpenMPI with Intel Compilers]]