### System Details 
Controller/Server/Master node
  - hostname: mgn
  - ip: 10.0.10.10
Compute nodes
  - hostname n1, n2
  - ip: 10.0.10.1, 10.0.10.2

## Prerequisite installations and configuration need to be done over all nodes of the cluster
### Add user for Slurm and Munge
Slurm and Munge require the same UID and GID across every node in the cluster. So do follow all the nodes including master nodes, before you install Slurm or Munge
````
groupadd -g 971 munge
useradd  -m -c "MUNGE Uid 'N' Gid Emporium" -d /var/lib/munge -u 971 -g munge  -s /sbin/nologin munge
groupadd -g 972 slurm
useradd  -m -c "SLURM workload manager" -d /var/lib/slurm -u 972 -g slurm  -s /bin/bash slurm
````

### Install and configure Munge
#### Install Munge
Do following on all the nodes including master nodes
````
dnf --enablerepo=crb install munge munge-libs munge-devel
````
NOTE: **EPEL repository** required if it is not available

#### Create Munge secret key on control/server node
After installing Munge, you need to "generate/create a secret key on the server node (i.e. here mgn)" and copy it to all other nodes
````
yum install rng-tools -y
rngd -r /dev/urandom

/usr/sbin/create-munge-key -r

dd if=/dev/urandom bs=1 count=1024 > /etc/munge/munge.key
````
NOTE:
- Install **rng-tools** to properly create the key
- You only have to do the creation of the secret key on the server (i.e. here mgn)

#### Copy Munge secret key to all compute nodes
After the secret key is created, you need to copy the key to all of the compute nodes (i.e. here n1, n2)
````
scp /etc/munge/munge.key root@n1:/etc/munge
scp /etc/munge/munge.key root@n2:/etc/munge
````

#### Set proper permissions
Do the following on all nodes to set correct the permissions for Munge
````
chown munge: /etc/munge/munge.key
chmod 400 /etc/munge/munge.key
chown -R munge: /etc/munge/ /var/log/munge/
chmod 0700 /etc/munge/ /var/log/munge/
````
NOTE: munge.conf file must be owned by "munge user", "munge group" and access permissions must be "chmod 400"

### Start the Munge service
Do the following on all nodes to start Munge service all nodes
````
systemctl enable munge
systemctl start munge
````

#### Test Munge
NOTE: successful execution of all the below tests is required to be processed further
````
munge -n
munge -n | unmunge
munge -n | ssh n1.test.cluster unmunge
munge -n | ssh n2 unmunge
remunge
````


## Install dependency packages on all nodes
````

dnf --enablerepo=crb install pmix-pmi-devel rrdtool-devel lua-devel
````
