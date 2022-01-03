=== Cluster details ===
  * Number of nodes: 5
    * node list: [node1, node2, node3, node4, node5]
    * cpu per node: 48
  * Total number of cpus: 240 (+48 master node)

===== Slurm run job =====
==== Serial job submit script ====
slurm submit script: **serial_job.sub**
    #!/bin/bash
    # job name
    #SBATCH --job-name=hw
    # STDOUT file; "N" is node number and "j" job id number
    #SBATCH --output=hw_%N_%j.out
    # STDERR file; "N" is node number and "j" job id number
    #SBATCH --error=hw_%N_%j.err
    # number of nodes
    #SBATCH --nodes=1
    # number of taskes per node
    #SBATCH --ntasks-per-node=1
    # total memory requirment
    #SBATCH --mem 10
    # total wall-time
    #SBATCH --time=00:05:00
    
    date
    /bin/hostname
    cd /home/hemanta/slurm_test
    srun ./hw
    date
==== Parallel job submit script ====
slurm submit script: **parallel_job.sub**

    #!/bin/bash
    # job name
    #SBATCH --job-name=mpi_sample
    # set the output file name
    #SBATCH --output=mpi_sample.out
    # set pertition
    #SBATCH --partition=normal
    # set the number of nodes
    #SBATCH --nodes=3
    # set the number of tasks per nodes
    #SBATCH --ntasks-per-node=4
    # set the amount of memory required per task
    #SBATCH --mem-per-cpu=10
    # set the wall time
    #SBATCH --time=00:02:00
    # send email notification
    #SBATCH --mail-user=<<email id>>
    #SBATCH --mail-type=ALL
    
    mpirun /home/hemanta/slurm_test/mpi_sample
    date
===== Slurm submit script flags =====
The table below shows a summary of some of Slurm submit script flags. These flags are described in more detail below along with links to the Slurm doc site.
|**Resource**|**Flag Syntax**|**Description**|**Notes**|
|job name|--job-name=hello_test|Name of job|default is the JobID|
|partition|--partition=normal|Partition is a queue for jobs|default on Mario is **normal** partition|
|time|--time=01:00:00|Time limit for the job|here 1 hour. On Mario cluster: 24 hours on default partition **normal** and not time limit on partition **long**|
|nodes|--nodes=2|Number of compute nodes for the job|default is 1;  compute nodes|
|cpus/cores|--ntasks-per-node=8|Corresponds to number of cores on the compute node|default is 1|
|memory|--mem=24000|Memory limit per compute node for the job.  Do not use with mem-per-cpu flag.|memory in MB; default limit is 3000MB per core|
|memory per CPU|--mem-per-cpu=4000|Per core memory limit.  Do not use the mem flag,|memory in MB; default limit is 3000MB per core|
|output file|--output=test.out|Name of file for stdout|default is the JobID|
|error file|--error=test.err|Name of file for stderr|default is the JobID|
|email address|--mail-user=username@buffalo.edu|User's email address|send email on submition and complition of job OR omit for no email|
|email notification|--mail-type=ALL --mail-type=END|When email is sent to user.|omit for no email|
===== Slurm commands =====
The table below shows a summary of some of the Slurm commands. These commands are described in more detail below along with links to the Slurm doc site.
|**Slurm Command**|**Description**|**Syntex**|
|''sbatch''|Submit a batch serial or parallel job using slurm submit script|''sbatch slurm_submit_script.sub''|
|''srun''|Run a script or application interactively|''srun --pty -p test -t 10 --mem 1000 /bin/bash [script or app]''|
|''scancel''|Kill a job by job id number|''scancel 999999''|
|''squeue''|View status of your jobs|''squeue -u hemanta'' OR ''squeue -l''|
|''sinfo''|View the cluster nodes, partions and node status information|''sinfo'' OR ''sinfo -lNe''|
|''sacct''|Check current job by id number|''sacct -j 999999''|
