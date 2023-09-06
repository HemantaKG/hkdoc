### System Details 
Controller/Server/Master node
  - hostname: mgn
  - ip: 10.0.10.10
Compute nodes
  - hostname n1, n2
  - ip: 10.0.10.1, 10.0.10.2

## Prerequisite installations and configuration need to be done over all nodes of the cluster
### Add user for Slurm and Munge
Slurm and Munge require same UID and GID across every node in the cluster. So do following on all the nodes including master nodes, before you install Slurm or Munge
````
groupadd -g 981 munge
useradd  -m -c "MUNGE Uid 'N' Gid Emporium" -d /var/lib/munge -u 981 -g munge  -s /sbin/nologin munge
groupadd -g 982 slurm
useradd  -m -c "SLURM workload manager" -d /var/lib/slurm -u 982 -g slurm  -s /bin/bash slurm
````

## Install dependency packages on all nodes
````

dnf --enablerepo=crb install pmix-pmi-devel rrdtool-devel lua-devel
````
