## Create spack ENV usign .yaml file
'''
spack env create pluto_env_gcc112_mpich402 /home/hemanta.kumar/spack_env/pluto_env.yaml
'''

## Activate spack ENV
'''
spack env activate pluto_env_gcc112_mpich402 -p
'''

## Install packages to above created spack ENV
'''
spack concretize -Uf
spack install -U
'''

## Remvoe spack ENV
'''
spack env remove pluto_env_gcc112_mpich402
'''


# Install packages with gcc v11.2.0 support
## Install and record a new gcc version
'''
spack install gcc@11.2.0
spack load gcc@11.2.0
'''

## add gcc v11.20 to local spack compiler space 
'''
spack compiler find
'''

## Create spack ENV with .yaml file
'''
spack env create spec_gcc112 "SPACK_YAML_FILE"
spack env activate spec_gcc112 -p
'''

## Concretize the installation first.
'''
spack concretize -Uf
'''
From the output of this step, please ensure that all libraries being installed will be compiled with gcc 11.2.0.

# Final step
'''
spack install -U
'''


## Ex of .yaml file
'''
# Spack env Name: spack env activate MPICH v4.0.2 with GCC v11.2.0
# DT20231206
# For Puluto PDE solver

spack:
  definitions:
  - compilers: [gcc@11.2.0]
  specs:
  - $compilers
  - 'mpich@4.0.2'
  - hdf5+mpi+cxx+fortran+shared+szip+threadsafe
  - chombo
  concretization: together
  view: true
'''
