===== Cluster details =====
  * cluster name: **Mario**
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

^Slurm partition^No of Nodes^Node list^Default queue time (Hours)^Total No. of cpu^
^<color #ed1c24>devel</color>|1|node[1]|12|32|
^short|4|node[2-5]|36|128|
^long|27|node[6-32]|no limit(inf)|864|
**NOTE:** <color #ed1c24>devel</color> is the default partition
  * GCC version: 4.8.5
  * Python version:

^Python version^location^export PATH^
^<color #ed1c24>python 2.7.5</color>|/usr/bin/python|defult|
^python 2.7.14|/share/anaconda2|''export PATH=/share/anaconda2/bin:$PATH''|
^python 3.6.4|/share/anaconda3/bin|''export PATH=/share/anaconda3/bin:$PATH''|

  * profiling tool:
    * Valgrind 3.13.0 ''/opt/valgrind''
  * Monitoring tool:
    * [[http://<<FQHN>>/ganglia|Ganglia]]

----
===== Slurm user guide =====
**Slurm** is a queue management system and stands for **Simple Linux Utility for Resource Management**. Slurm is similar in many ways to most other queue systems. You write a batch script then submit it to the queue manager. The queue manager then schedules your job to run on the queue (or partition in Slurm parlance) that you designate. Below we will provide an outline of how to submit jobs to Slurm, how Slurm decides when to schedule your job, and how to monitor progress.

  * It waits for jobs to be cleared before scheduling the high priority job. It also does kill and requeue on memory rather than just on core count.
  * The amount of memory you request at runtime is guaranteed to be there. No one can infringe on that memory space and you cannot exceed the amount of memory that you request.
  * Accounting Tools Slurm has a back-end database which stores historical information about the cluster. This information can be queried by the users who are curious about how much resources they have used. It is used for adjudicating job priority on the cluster.
===== Slurm commands =====
The table below shows a summary of some of the Slurm commands. These commands are described in more detail below along with links to the Slurm doc site.
^Slurm Command^Description^Syntex^
^''sbatch''|Submit a batch serial or parallel job using slurm submit script|''sbatch slurm_submit_script.sub''|
^''srun''|Run a script or application interactively|''srun --pty -p test -t 10 --mem 1000 /bin/bash [script or app]''|
^''scancel''|Kill a job by job id number|''scancel 999999''|
^''squeue''|View status of your jobs|''squeue -u hemanta'' OR ''squeue -l''|
^''sinfo''|View the cluster nodes, partitions and node status information|''sinfo'' OR ''sinfo -lNe''|
^''sacct''|Check current job by id number|''sacct -j 999999''|

==== Some useful commands ====
Lists partitions and nodes with core wise allocation:
<code>
sinfo --format="%9P %l %10n %.14C %.10T"
</code>
Run the following statement to list all the jobs currently in Slurm queue. It lists the jobs with all these details jodID, how many cores the job reserved, running in which partition, job status, memory, username, time, no which node, etc
<code>
squeue -o"%.7i %.9P %.8j %.8u %.2t %.10M %.6D %.4C %9N %11m"
</code>
===== Run jobs using Slurm submit script =====
==== Slurm submit script flags ====
The table below shows a summary of some of Slurm submit script flags. These flags are described in more detail below along with links to the Slurm doc site.
^Resource^Flag Syntax^Description^Notes^
^job name|''--job-name=''hello_test|Name of job|default is the **JobID**|
^partition|''--partition=''devel|Partition is a queue for jobs|default partition maked with *, **devel** is the default partition on Mario|
^time|''--time=''01:00:00|Time limit for the job. Acceptable time formats include **minutes**, **minutes:seconds**, **hours:minutes:seconds**, **days-hours**, **days-hours:minutes** and **days-hours:minutes:seconds**|here it is given as 1 hour|
^nodes|''--nodes=''2|Number of compute nodes for the job|default is **1**  compute node|
^cpus/cores|''--ntasks-per-node=''8|Corresponds to number of cores on the compute node|default is **1** task per node|
^memory|''--mem=''32000|Memory limit per compute node for the job.  Do not use with **mem-per-cpu** flag|memory in **MB** |
^memory per CPU|''--mem-per-cpu=''1000|per core memory limit.  Do not use with **mem** flag|memory in **MB**|
^output file|''--output=''test.out|Name of file for stdout|default is the **JobID**|
^error file|''--error=''test.err|Name of file for stderr|default is the **JobID**|
^email address|''--mail-user=''username@buffalo.edu|User's email address|send email on submition and complition of job OR omit for no email|
^email notification|''--mail-type=ALL'' ''--mail-type=END''|When email is sent to user.|omit for no email|
==== Run serial jobs ====
==== Serial job sample01 [Submitting a Single Serial Job] ====
  * source file: **hw.c**
  * slurm submit script: **hw.sub**
source file: **hw.c**
<file c hw.c>
#include <stdio.h>
int main(void){
  printf("Hello world\n");
  return 0;
}
</file>
slurm submit script: **hw.sub**
<file bash hw.sub>
#!/bin/bash
# job name
#SBATCH --job-name=hw
# STDOUT file
#SBATCH --output=hw.out
# number of nodes
#SBATCH --nodes=1
# number of tasks per node
#SBATCH --ntasks-per-node=1
# total memory requirment
#SBATCH --mem 10
# total wall-time
#SBATCH --time=00:05:00

cd /home/hemanta/slurm_test
./hw
</file>
**NOTE:** output file **hw.out**
----
slurm submit script: **hw1.sub**
<file bash hw_mul.sub>
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
</file>
**NOTE:** output file **hw_node#_#.out** and **hw_node#_#.err**; where ''#'' node and process number
----
==== Serial job sample02 [Submitting Multiple Serial jobs using slurm submit script] ====
  * source file: **hw.c**
  * slurm script: **hw.sh**
  * job submit script: **hw.sub**

source file: **hw.c**
<file c hw.c>
#include <stdio.h>
int main(void){
  printf("Hello world\n");
  return 0;
}
</file>
slurm script: **hw.sub**
<file bash hw.sub>
#!/bin/bash
#
#SBATCH --job-name=hw
#SBATCH --output=hw_%N_%j.out
#SBATCH --error=hw_%N_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --time=00:05:00

cd /home/hemanta/slurm_test
hn=`/bin/hostname`
# Run instance of the serial job with unique parameters
for ((myproc=1; myproc<=$SLURM_NPROCS; myproc++)) do
srun ./hw $myproc > hw-$myproc-${hn}.out &
done
wait
</file>
**NOTE:** output file are **hw-1-node1.out, hw-2-node2.out, hw-3-node3.out, hw_node#_#.out, hw_node#_#.err**. where as ''#'' node number and job id number number
----
==== Run parallel jobs ====
=== Parallel job sample01 ===
  * source file: **mpi_sample.c**
  * slurm submit script: **mpi_sample.sub**

source file **mpi_sample.c**
<file c mpi_sample.c>
#include <mpi.h>
#include <stdio.h>
int main(int argc, char** argv) {
  // Initialize the MPI environment
  MPI_Init(NULL, NULL);
  
  // Get the number of processes
  int world_size;
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);
  
  // Get the rank of the process
  int world_rank;
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
  
  // Get the name of the processor
  char processor_name[MPI_MAX_PROCESSOR_NAME];
  int name_len;
  MPI_Get_processor_name(processor_name, &name_len);
  
  // Print off a hello world message
  printf("Hello world from processor %s, rank %d"
   " out of %d processors\n",
   processor_name, world_rank, world_size);
  
  // Finalize the MPI environment.
  MPI_Finalize();
}
</file>
slurm submit script: **mpi_sample.sub**
<file bash mpi_sample.sub>
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
</file>
----
==== Submit serial jobs ====
Serial job sample script – sample.sub
<file bash sample.sub>
#!/bin/bash

# Job name
#SBATCH --job-name=test-serial
#
# Set partition
#SBATCH --partition=short
#
# STDOUT file; "N" is node number and "j" job id number
#SBATCH --output=test-serial_%N_%j.out
# STDERR file; "N" is node number and "j" job id number
#SBATCH --error=test-serial_%N_%j.err
#
# Number of processes
#SBATCH --ntasks=64
# Memory requirement per CPU
#SBATCH --mem-per-cpu=3
#
# Total wall-time
#SBATCH --time=00:05:00
#
# Uncomment to get email alert
### SBATCH --mail-user=<<email id>
### SBATCH --mail-type=ALL

date
cd /home/hemanta.kumar/slurm_test
./long_run
date
</file>
----
==== Submitting OpenMP jobs (multi-threaded) ====
OpenMP (multi-threaded) job sample script – sample.sub
<file bash sample.sub>
#!/bin/bash
#
# Job name
#SBATCH --job-name=ompi_lws
# STDOUT file; "N" is node number and "j" job id number
#SBATCH --output=ompi-lws_%N_%j.out
# STDERR file; "N" is node number and "j" job id number
#SBATCH --error=ompi-lws_%N_%j.err
#
# Set partition
#SBATCH --partition=devel
#
#SBATCH --ntasks=1
# Number of CPUs required for the process
#SBATCH --cpus-per-task=32
#
# Memory requirement
#SBATCH --mem 10
#
# Total wall-time
#SBATCH --time=00:05:00
#
# Uncomment to get email alert
### SBATCH --mail-user=<<email id>
### SBATCH --mail-type=ALL

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

date
./openmp_loopwork_share
date
</file>
----
==== Submitting MPI jobs (multi-process) ====
  - How do you want the processes to be distributed?
    - All are on the same node to reduce the network latencies
    - Scatter distribution of jobs to increase overall memory bandwidth
    - Even distribution of processes across nodes
    - Let scheduler choose
== All are on the same node to reduce the network latencies ==
<file bash sample.sub>
#!/bin/bash
# Submission script: "tasks are all grouped on same node"

# Job name
#SBATCH --job-name=mpi_mm
# Output file name
#SBATCH --output=mpi_mm_v2.out
#SBATCH --error=mpi_mm_v2.err
#
# Set the required partition
#SBATCH --partition=short
# Number of processes
#SBATCH --ntasks=32
# Number of nodes
#SBATCH --nodes=1
# Memory per process
#SBATCH --mem-per-cpu=1
#
# Total wall-time
#SBATCH --time=00:05:00
#
# Uncomment the following line if your work is floating point intensive and CPU-bound.
### SBATCH --threads-per-core=1
#
# Uncomment to get email alert
### SBATCH --mail-user=<<email id>
### SBATCH --mail-type=ALL

date
mpirun /home/it/slurm_test/mpi_mm
#srun /home/it/slurm_test/mpi_mm
date
</file>
== Scatter distribution of jobs to increase overall memory bandwidth ==
<file bash sample.sub>
#!/bin/bash
# Submission script: "tasks are scattered across distinct nodes"

# Job name
#SBATCH --job-name=mpi_mm
# Output file name
#SBATCH --output=mpi_mm_v3.out
#SBATCH --error=mpi_mm_v3.err
#
# Set the required partition
#SBATCH --partition=short
# Number of processes
#SBATCH --ntasks=2
#SBATCH --ntasks-per-node=1
# Memory per process
#SBATCH --mem-per-cpu=1
#
# Total wall-time
#SBATCH --time=00:05:00
#
# Uncomment the following line if your work is floating point intensive and CPU-bound.
### SBATCH --threads-per-core=1
#
# Uncomment to get email alert
### SBATCH --mail-user=<<email id>
### SBATCH --mail-type=ALL

date
mpirun /home/it/slurm_test/mpi_mm
#srun /home/it/slurm_test/mpi_mm
date
</file>
== Even distribution of processes across nodes ==
<file bash sample.sub>
#!/bin/bash
# Submission script: "tasks are evenly distributed across nodes"

# Job name
#SBATCH --job-name=mpi_mm
# Output file name
#SBATCH --output=mpi_mm_v1.out
#SBATCH --error=mpi_mm_v1.err
#
# Set the required partition
#SBATCH --partition=short
# Number of processes
#SBATCH --ntasks=32
# Process distribution per node
#SBATCH --ntasks-per-node=8
# Number of nodes
#SBATCH --nodes=4
# Memory per process
#SBATCH --mem-per-cpu=1
#
# Total wall-time
#SBATCH --time=00:05:00
#
# Uncomment the following line if your work is floating point intensive and CPU-bound.
### SBATCH --threads-per-core=1
#
# Uncomment to get email alert
### SBATCH --mail-user=<<email id>
### SBATCH --mail-type=ALL

date
mpirun /home/it/slurm_test/mpi_mm
#srun /home/it/slurm_test/mpi_mm
date
</file>
== Let scheduler choose ==
<file bash sample.sub>
#!/bin/bash
# Submission script: "no plan"

# Job name
#SBATCH --job-name=mpi_mm
# Output file name
#SBATCH --output=mpi_mm_v4.out
#SBATCH --error=mpi_mm_v4.err
#
# Set the required partition
#SBATCH --partition=short
# Number of processes
#SBATCH --ntasks=64
# Memory per process
#SBATCH --mem-per-cpu=1
#
# Total wall-time
#SBATCH --time=00:05:00
#
# Uncomment the following line if your work is floating point intensive and CPU-bound.
### SBATCH --threads-per-core=1
#
# Uncomment to get email alert
### SBATCH --mail-user=<<email id>
### SBATCH --mail-type=ALL

date
mpirun /home/it/slurm_test/mpi_mm
#srun /home/it/slurm_test/mpi_mm
date
</file>
===== Reference =====
  * [[https://www.princeton.edu/researchcomputing/education/online-tutorials/getting-started/running-serial-jobs/]]
  * [[https://www.rc.fas.harvard.edu/resources/running-jobs/]]
  * [[https://uwaterloo.ca/math-faculty-computing-facility/services/service-catalogue-teaching-linux/controlling-and-signaling-jobs|Slurm command for controling anf signaling the jobs]]
  * [[http://doc.aris.grnet.gr/|A proper Slurm user documentation (ARIS user support)]]
