===== Cluster details =====
  * master node: 1
    * master node cpu: 32
    * local **/scratch** ~700GB
  * number of compute-node: 32
    * node list: [node1, node2, node3,... node32]
    * cpu per computer-node: 32
    * local **/scratch** ~600GB
  * total number of cpu: **1024**
  * job scheduler: **Slurm**
    * Slurm partitions:

|**Slurm partition**|**No of Nodes**|**Node list**|**Default queue time (Hours)**|**Total No. of cpu**|
|<color #ed1c24>devel</color>|1|node[1]|12|32|
|short|4|node[2-5]|36|128|
|long|27|node[6-32]|no limit(inf)|864|
NOTE: <color #ed1c24>devel</color> is the default partition
  * GCC version: 4.8.5
  * Python version:

|**Python version**|**location**|**export PATH**|
|<color #ed1c24>python 2.7.5</color>|**/usr/bin/python**|defult|
|python 2.7.14|**/share/anaconda2**|''export PATH=/share/anaconda2/bin:$PATH''|
|python 3.6.4|**/share/anaconda3/bin**|''export PATH=/share/anaconda3/bin:$PATH''|

  * profiling tool:
    * Valgrind 3.13.0 ''/opt/valgrind''
  * Monitoring tool:
    * [[http://<<FQHA>>/ganglia|Ganglia]]

----
===== Slurm user guide =====
==== Serial job submit =====
slurm submit script: serial_job.sub
   #!/bin/bash
   
   #job name
   #SBATCH --job-name=hw
   #"STDOUT" file; "N" is node number and "j" job id number
   #SBATCH --output=hw_%N_%j.out
   #"STDERR" file; "N" is node number and "j" job id number
   #SBATCH --error=hw_%N_%j.err
   #number of nodes
   #SBATCH --nodes=1
   #number of taskes per node
   #SBATCH --ntasks-per-node=1
   #total memory requirment
   #SBATCH --mem 10
   #total wall-time
   #SBATCH --time=00:05:00
   #send email notification
   #SBATCH --mail-user=<<email id>>
   #SBATCH --mail-type=ALL
   
   date
   cd /home/hemanta/slurm_test
   srun ./hw
   date

----
==== Parallel job submit ====
slurm submit script: parallel_job.sub
   #!/bin/bash
   #job name
   #SBATCH --job-name=mpi_sample
   #set the output file name
   #SBATCH --output=mpi_sample.out
   #set pertition
   #SBATCH --partition=normal
   #set the number of nodes
   #SBATCH --nodes=3
   #set the number of tasks per nodes
   #SBATCH --ntasks-per-node=4
   #set the amount of memory required per task
   #SBATCH --mem-per-cpu=10
   #set the wall time
   #SBATCH --time=00:02:00
   #send email notification
   #SBATCH --mail-user=<<email id>>
   #SBATCH --mail-type=ALL
   
   mpirun /home/hemanta/slurm_test/mpi_sample
   date

----
===== More Slurm submit script flags =====
==== Slurm submit script flags ====
The table below shows a summary of some of Slurm submit script flags. These flags are described in more detail below along with links to the Slurm doc site.
|**Resource**|**Flag Syntax**|**Description**|**Notes**|
|job name|''--job-name=''hello_test|Name of job|default is the **JobID**|
|partition|''--partition=''devel|Partition is a queue for jobs|default partition maked with *, **devel** is the default partition on Mario|
|time|''--time=''01:00:00|Time limit for the job. Acceptable time formats include **minutes**, **minutes:seconds**, **hours:minutes:seconds**, **days-hours**, **days-hours:minutes** and **days-hours:minutes:seconds**|here it is given as 1 hour|
|nodes|''--nodes=''2|Number of compute nodes for the job|default is **1**  compute node|
|cpus/cores|''--ntasks-per-node=''8|Corresponds to number of cores on the compute node|default is **1** task per node|
|memory|''--mem=''32000|Memory limit per compute node for the job.  Do not use with **mem-per-cpu** flag|memory in **MB** |
|memory per CPU|''--mem-per-cpu=''1000|per core memory limit.  Do not use with **mem** flag|memory in **MB**|
|output file|''--output=''test.out|Name of file for stdout|default is the **JobID**|
|error file|''--error=''test.err|Name of file for stderr|default is the **JobID**|
|email address|''--mail-user=''username@buffalo.edu|User's email address|send email on submition and complition of job OR omit for no email|
|email notification|''--mail-type=ALL'' ''--mail-type=END''|When email is sent to user.|omit for no email|

----
===== Slurm commands =====
The table below shows a summary of some of the Slurm commands. These commands are described in more detail below along with links to the Slurm doc site.
|**Slurm Command**|**Description**|**Syntex**|
|''sbatch''|Submit a batch serial or parallel job using slurm submit script|''sbatch slurm_submit_script.sub''|
|''srun''|Run a script or application interactively|''srun --pty -p test -t 10 --mem 1000 /bin/bash [script or app]''|
|''scancel''|Kill a job by job id number|''scancel 999999''|
|''squeue''|View status of your jobs|''squeue -u hemanta'' OR ''squeue -l''|
|''sinfo''|View the cluster nodes, partitions and node status information|''sinfo'' OR ''sinfo -lNe''|
|''sacct''|Check current job by id number|''sacct -j 999999''|
**NOTE**: Run the following statement to list all the jobs currently in slurm queue. It lists the jobs with all these details jodID, how many cores the job reserved, running in which partition, job status, memory, username, time, no which node, etc
    squeue -o"%.7i %.9P %.8j %.8u %.2t %.10M %.6D %.4C %9N %11m"
    
    OUTPUT:
    JOBID PARTITION     NAME     USER ST       TIME  NODES CPUS NODELIST  MIN_MEMORY 
    1616       long somerand  hemanta R        0:04      1    3 node4     100M

----
