# Slurm accounting configuration
NOTE: Install MariaDB server before building Slurm rpms or installing Slurm for source
## Verify the slurm-sql package is installed
```
rpm -q mariadb-server mariadb-devel
rpm -ql slurm-sql | grep accounting_storage_mysql.so
````
**NOTE:** If **accounting_storage_mysql.so** not found than; locate the file and copy to "/usr/lib64/slurm" as;
````
locate accounting_storage_mysql.so

cp /root/rpmbuild/BUILD/slurm-17.02.8/src/plugins/accounting_storage/mysql/.libs/accounting_storage_mysql.so /usr/lib64/slurm/
cp /root/rpmbuild/BUILD/slurm-17.02.8/src/plugins/jobcomp/mysql/.libs/jobcomp_mysql.so /usr/lib64/slurm/
````

## Start database server
````
systemctl start mariadb
systemctl enable mariadb
systemctl status mariadb
````

### Configure and set root password for new database server
NOTE:
- Its needs to **set root password for root user**; for first time run of MariaDB database server
- remove all previous settings and example databases
````
/usr/bin/mysql_secure_installation
````
>Enter current password for root (enter for none):
>NOTE: just press enter
>
>Set root password? [Y/n] y
>New password: 
>Re-enter new password: 
>
>Remove anonymous users? [Y/n] y
>Disallow root login remotely? [Y/n] y
>Remove test database and access to it? [Y/n] y
>Reload privilege tables now? [Y/n] y

### Create database for Slurm workload manager
Open mysql database as a root user using above root password. Create database for Slurm workload manager and grand all to slurm user 
````
mysql -p

grant all on slurm_acct_db.* TO 'slurm'@'localhost' identified by '<<password>>' with grant option;
show VARIABLES LIKE 'have_innodb';
create database slurm_acct_db;
quit;
````
NOTE: Change "db name" slurm_acct_db and "db password" password to your db name and password
### Modify Slurm configuration files for slurm accounting group configuration
- Copy **/etc/slurm/slurmdbd.conf.example** to **/etc/slurm/slurmdbd.conf**
- Modify **slurm.conf** and **slurmdbb.conf** files [[ Slurm configuration file| Mario ]]

### Start slurmdbd service
````
systemctl start slurmdbd.service
systemctl enable slurmdbd.service
systemctl status slurmdbd.service
````

## Create Slurm accounting group and Add user under accounting group
NOTE: below cluster name must be same name as cluster name that given in slurm.conf file. Where **testcluster** is the slurm cluster name
````
# create cluster group account
sacctmgr add cluster testcluster
````
### Create accounts under above created cluster group
````
# add a none test to group "testcluster" group (**not required)
sacctmgr add account none,test Cluster=testcluster Description="none" Organization="none"

# add cluster "hpc" as accounting group to "testcluster" group
sacctmgr add account hpc Cluster=testcluster Description="prototype hpc cluster" Organization="<<name>>"

# add cluster "guestusers" as accounting group to "testcluster" group
sacctmgr add account guestusers Cluster=tetriscluster Description="Tetris HPC Cluster" Organization="<<name>>"
````
### Add users under account and set resource users limit
````
# add user "it" to the accounting group "test"
sacctmgr add user it Account=test

# add user "hemanta" to the accounting group "hpc"
sacctmgr add user hemanta Account=hpc

# add user "guest1" to the accounting group "guestusers"
sacctmgr add user guest1 DefaultAccount=guestusers

# set resource max limit(s) for above added user "guest1"
sacctmgr modify user guest1 account=guestusers set MaxSubmit=1000 MaxJobs=240
````

### Show all slurm accounting users
````
sacctmgr show user -s
````

### Some more examples of accounting group and user
File: add_user_slurm_accounting_group.txt
```` txt
//Add to slurm.conf
# user job limit(s)
AccountingStorageEnforce=associations,limits
#AccountingStorageEnforce=limits

//Guest user CPU limit set
sacctmgr add account guestusers Cluster=tetriscluster Description="Tetris HPC Cluster" Organization="<<name>>"
sacctmgr add user guest1 Account=guestusers
sacctmgr modify user guest1 set GrpTRES=cpu=96
sacctmgr modify user where name=guest1 cluster=tetriscluster account=guestusers set maxjobs=96

//working
sacctmgr modify user guest1 cluster=tetriscluster account=guestusers set MaxJobs=320 MaxSubmit=1000

//show all user accounting/QOS policy
sacctmgr show user -s

//restart services 
slurmd on nodes
slurmcrld on master

//Delete account
sacctmgr delete user guest1 account=guestusers
sacctmgr delete user guest2 account=guestusers

//Add user(s) and set limit(s):
# guest user(s):
sacctmgr add user guest1 DefaultAccount=guestusers
sacctmgr modify user guest1 account=guestusers set MaxSubmit=1000 MaxJobs=240

sacctmgr add user guest2 DefaultAccount=guestusers
sacctmgr modify user guest2 account=guestusers set MaxSubmit=1000 MaxJobs=240

# Add and modify user(s):
sacctmgr add user hemanta.kumar DefaultAccount=icts
sacctmgr modify user hemanta.kumar account=icts set MaxSubmit=640 MaxJobs=2000

#set resource limit (JOB limit)
sacctmgr modify user hemanta.kumar account=icts set MaxSubmit=2000 MaxJobs=640

//delete user [check for no job(s) in queue]:
sacctmgr delete user guest1 account=guestusers

// cluster utilization report (Slurm report)
sreport cluster UserUtilizationByAccount format=Accounts,Cluster,TresCount,Login,Proper,Used
````

## Some usefull commands
````
sacct -S2018-01-31-11:40 -E2018-02-12-17:00 -X -o jobid,start,end,state,user,partition,jobname
````

## Reference
- https://wiki.fysik.dtu.dk/niflheim/Slurm_database
- http://biocluster.ucr.edu/~jhayes/slurm/accounting.shtml
- https://slurm.schedmd.com/accounting.html
