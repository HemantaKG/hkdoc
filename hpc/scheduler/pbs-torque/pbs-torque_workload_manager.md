===== Commands =====
  * How to delete jobs from torque-pbs queue
    * delete single job **''qdel <job_id>''**
    * delete all jobs **''qselect -u <username> | xargs qdel''**