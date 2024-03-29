## Master node
File location: /etc/slurm/slurm.conf
```` bash
# slurm.conf file generated by configurator easy.html.
# Put this file on all nodes of your cluster.
# See the slurm.conf man page for more information.
#
#
ControlMachine=master
ControlAddr=10.10.0.100
#
# 
#MailProg=/bin/mail 
MpiDefault=none
#MpiParams=ports=#-# 
ProctrackType=proctrack/cgroup
ReturnToService=2
SlurmctldPidFile=/var/run/slurmctld.pid
#SlurmctldPort=6817 
SlurmdPidFile=/var/run/slurmd.pid
#SlurmdPort=6818 
SlurmdSpoolDir=/var/spool/slurmd
SlurmUser=slurm
#SlurmdUser=root 
StateSaveLocation=/var/spool/slurmctld
SwitchType=switch/none
TaskPlugin=task/none
# 
# 
# TIMERS 
#KillWait=30 
#MinJobAge=300 
#SlurmctldTimeout=120 
#SlurmdTimeout=300 
# 
# 
# SCHEDULING 
FastSchedule=1
SchedulerType=sched/backfill
SelectType=select/cons_res
#SelectType=select/linear
SelectTypeParameters=CR_CPU_Memory
# 
# Default Memory limits
#DefMemPerCPU=1000
#DefMemPerNode=30000
#
# 
# LOGGING AND ACCOUNTING 
AccountingStorageHost=localhost
#AccountingStorageType=accounting_storage/none
#AccountingStorageType=accounting_storage/filetxt
AccountingStorageType=accounting_storage/slurmdbd
AccountingStorageLoc=/var/log/slurm/accounting
JobCompType=jobcomp/slurmdbd
JobCompLoc=/var/log/slurm/job_completions
#
#
# Slurm Cluster Name
ClusterName=mariocluster
#
#
#JobAcctGatherFrequency=30 
#JobAcctGatherType=jobacct_gather/none
JobAcctGatherType=jobacct_gather/linux
#SlurmctldDebug=3 
SlurmctldLogFile=/var/log/slurm/slurmctld.log
#SlurmdDebug=3 
SlurmdLogFile=/var/log/slurm/slurmd.log
#
#
# COMPUTE NODES
NodeName=node1 NodeAddr=10.10.0.1 CPUs=48 Sockets=2 CoresPerSocket=12 ThreadsPerCore=2 RealMemory=96404 State=UNKNOWN
NodeName=node2 NodeAddr=10.10.0.2 CPUs=48 Sockets=2 CoresPerSocket=12 ThreadsPerCore=2 RealMemory=96404 State=UNKNOWN
NodeName=node3 NodeAddr=10.10.0.3 CPUs=48 Sockets=2 CoresPerSocket=12 ThreadsPerCore=2 RealMemory=96404 State=UNKNOWN
NodeName=node4 NodeAddr=10.10.0.4 CPUs=48 Sockets=2 CoresPerSocket=12 ThreadsPerCore=2 RealMemory=96404 State=UNKNOWN
NodeName=node5 NodeAddr=10.10.0.5 CPUs=48 Sockets=2 CoresPerSocket=12 ThreadsPerCore=2 RealMemory=96404 State=UNKNOWN
#
#
# PARTITIONS
PartitionName=normal Nodes=node[1-3] Default=YES MaxTime=24:00:00 State=UP
PartitionName=long Nodes=node[4-5] Default=NO MaxTime=INFINITE State=UP
````
----
File location: /etc/slurm/slurmdbd.conf
````bash
#
# Example slurmdbd.conf file.
#
# See the slurmdbd.conf man page for more information.
#
# Archive info
#ArchiveJobs=yes
#ArchiveDir="/tmp"
#ArchiveSteps=yes
#ArchiveScript=
#JobPurge=12
#StepPurge=1
#
# Authentication info
AuthType=auth/munge
#AuthInfo=/var/run/munge/munge.socket.2
#
# slurmDBD info
DbdAddr=localhost
DbdHost=localhost
#DbdPort=7031
SlurmUser=slurm
#MessageTimeout=300
DebugLevel=4
#DefaultQOS=normal,standby
LogFile=/var/log/slurm/slurmdbd.log
PidFile=/var/run/slurmdbd.pid
#PluginDir=/usr/lib/slurm
PluginDir=/usr/lib64/slurm
#PrivateData=accounts,users,usage,jobs
#TrackWCKey=yes
#
# Database info
StorageType=accounting_storage/mysql
StorageHost=localhost
#StoragePort=1234
StoragePass=*****
StorageUser=slurm
StorageLoc=slurm_mario_db
````
----
## Compute Node
File location: /etc/slurm/cgroup.conf
```` bash
CgroupMountpoint="/sys/fs/cgroup"
CgroupAutomount=yes
CgroupReleaseAgentDir="/etc/slurm/cgroup"
AllowedDevicesFile="/etc/slurm/cgroup_allowed_devices_file.conf"
ConstrainCores=no
TaskAffinity=no
ConstrainRAMSpace=yes
ConstrainSwapSpace=no
ConstrainDevices=no
AllowedRamSpace=100
AllowedSwapSpace=0
MaxRAMPercent=100
MaxSwapPercent=100
MinRAMSpace=30
````
----
File location: /etc/slurm/cgroup_allowed_devices_file.conf
```` bash
/dev/null
/dev/urandom
/dev/zero
/dev/sda*
/dev/cpu/*/*
/dev/pts/*
````
