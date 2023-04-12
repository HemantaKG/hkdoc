# Consumable Resources in Slurm
Slurm, using the default node allocation plug-in (i.e select/liner), which allocates nodes to jobs in exclusive mode. This means that even when all the resources within a node are not utilized by a given job, another job will not have access to these resources. Nodes possess resources such as processors, memory, swap, local disk, etc. and jobs consume these resources. The exclusive use default policy in Slurm can result in inefficient utilization of the cluster and of its nodes resources. Slurm's cons_res or consumable resource plugin (i.e select/cons_res) is available to manage resources on a much more fine-grained basis as described below.
# Using the Consumable Resource Allocation Plugin:
- select/cons_res
Modify the **SelectType** from **select/linear** to **select/cons_res** and add **SelectTypeParameters**  to **slurm.conf** file as follow
````
SelectType=select/cons_res
#SelectType=select/linear
SelectTypeParameters=CR_CPU_Memory
````
# Reference
- https://slurm.schedmd.com/cons_res.html| Consumable Resource Allocation
