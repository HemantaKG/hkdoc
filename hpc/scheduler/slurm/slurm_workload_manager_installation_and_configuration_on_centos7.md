===== System details =====
  * controller/server/master node
    * hostname: mgn
    * ip: 10.0.10.10
  * compute nodes
    * hostname n1, n2
    * ip: 10.0.10.1, 10.0.10.2
===== Prerequisite installations and configuration need to do over all nodes of the cluster =====
==== Add user for Slurm and Munge ====
Slurm and Munge require same UID and GID across every node in the cluster. So do following on all the nodes including master nodes, before you install Slurm or Munge
<code>
groupadd -g 981 munge
useradd  -m -c "MUNGE Uid 'N' Gid Emporium" -d /var/lib/munge -u 981 -g munge  -s /sbin/nologin munge
groupadd -g 982 slurm
useradd  -m -c "SLURM workload manager" -d /var/lib/slurm -u 982 -g slurm  -s /bin/bash slurm
</code>
==== Install and configuration Munge ====
=== Install Munge ===
Do following on all the nodes including master nodes
<code>
yum install epel-release
yum install munge munge-libs munge-devel -y
</code>
NOTE: **EPEL repository** required if it is not available
=== Create Munge secret key on control/server node ===
After installing Munge, you need to **generate/create a secret key on the server node (i.e here mgn)** and copy to all other nodes
<code>
yum install rng-tools -y
rngd -r /dev/urandom

/usr/sbin/create-munge-key -r

dd if=/dev/urandom bs=1 count=1024 > /etc/munge/munge.key
</code>
NOTE:
  * Install **rng-tools** to properly create the key
  * You only have to do the creation of the secret key on the server (i.e here mgn)

=== Copy Munge secret key to all compute nodes ===
After the secret key is created, you need to copy the key to all of the compute nodes (i.e here n1, n2)
<code>
scp /etc/munge/munge.key root@n1:/etc/munge
scp /etc/munge/munge.key root@n2:/etc/munge
</code>
=== Set proper permissions ===
Do the following on all nodes to set correct the permissions for Munge
<code>
chown munge: /etc/munge/munge.key
chmod 400 /etc/munge/munge.key
chown -R munge: /etc/munge/ /var/log/munge/
chmod 0700 /etc/munge/ /var/log/munge/
</code>
**NOTE:** munge.conf file must be owned by **munge user**, **munge group** and access permissions must be **''chmod 400''**
=== Start the Munge service ===
Do the following on all nodes to start Munge service on all nodes
<code>
systemctl enable munge
systemctl start munge
</code>
=== Test Munge ===
**NOTE:** successful execution of all the below test is required to processed further
<code>
munge -n
munge -n | unmunge
munge -n | ssh n1.test.cluster unmunge
munge -n | ssh n2 unmunge
remunge
</code>
==== Sync clocks on the cluster ====
NOTE: **clock sync** is most important for Slurm configuration
<code>
yum install ntp -y
chkconfig ntpd on
ntpdate pool.ntp.org
systemctl start ntpd
</code>
==== Install Slurm dependencies ====
Slurm has a few dependencies that we need to install upon all nodes
<code>
yum install openssl openssl-devel pam-devel numactl numactl-devel hwloc hwloc-devel lua lua-devel readline-devel rrdtool-devel ncurses-devel man2html libibmad libibumad perl-devel -y
</code>
===== Download and build Slurm rpms =====
  * Install **mariadb-server** and **mariadb-devel** on **master server** (or where ever your building rmps); before running **''rpmbuild''** to generate slurm rmp packages
<code>
yum install mariadb-server mariadb-devel -y
</code>
  * Download the [[https://www.schedmd.com/downloads.php|latest version of Slurm]] preferably in our shared folder
  * Build the **rmps** from above downloaded **slurm-xx.xx.xx.dz2** file using ''**rpmbuild**'' command. **NOTE:** If rpmbuild not available install rpm-build package ''yum install rpm-build''. Sometimes the rpmbuild fails if required development tools are not available (such as; gcc compiler) then, install development tools packages ''yum group install "Development Tools"''
  * All rpms file will be available under **/root/rpmbuild/RPMS/x86_64/** if your building as a root user
  * Move into the **/root/rpmbuild/RPMS/x86_64/** and Copy all the Slurm rpms to some other folder. **NOTE:** copy into some shared directory (NFS mounted directory) it is easy for installation on all compute nodes
<code>
#Install Development Tools
yum group install "Development Tools"

#Run rpmbuild to create rmps NOTE: install rpm-build if not available
yum install rpm-build
rpmbuild -ta slurm-17.02.8.tar.bz2

#move into the rpm created directory
cd /root/rpmbuild/RPMS/x86_64

#copy all Slurm rpms to shared directory
cp * /home/it/slurm_rpm/
cd /home/it/slurm_rpm
</code>
==== Install Slurm on all nodes ====
<code>
yum --nogpgcheck localinstall slurm-*
</code>
===== Genarate and configure Slurm configuration file =====
Slurm workload manager resource allocation methods: for more details please check [[ Consumable Resources in Slurm ]]
  * node allocation plug-in ''linear''. its default
  * consumable resource plug-in ''cons_res''
==== Generate Slurm configuration file ====
  * Visit [[http://slurm.schedmd.com/configurator.easy.html|page]] to generate/make a configuration file for Slurm
  * Change and modifications the properties as per your requirements 
    * I made only the following changes and left everything default
  * Press submit button to generate full **Slurm configuration file**
  * Copy Slurm configuration file that was created from the website and paste it into **slurm.conf**
  * Keep the **slurm.conf** file under **/etc/slurm/** folder [[Slurm Configuration file|Mario]], [[Slurm Configuration file test_cluster|test_cluster]]
<code>
ControlMachine: mgn
ControlAddr: 10.0.10.10
NodeName: n[1-2]
CPUs: 2
StateSaveLocation: /var/spool/slurmctld
SlurmctldLogFile: /var/log/slurmctld.log
SlurmdLogFile: /var/log/slurmd.log
ClusterName: testcluster

#save slurm.conf file under /etc/slurm directory
cd /etc/slurm
nano slurm.conf
</code>
==== Add all compute nodes in slurm.conf file ====
  * By default Slurm tries to determine the IP addresses automatically with the one line i.e **''NodeName=buhpc[1-6] CPUs = 4 State = UNKNOWN''**
  * If your node doesn't have IP addresses in order, then you need to manually delete/comment the above one line and add following lines in **# COMPUTE NODES** block of **slurm.conf** file
<code>
#NodeName=n[1-2] CPUs=2 State=UNKNOWN
NodeName=n1 NodeAddr=10.0.10.1 CPUs=2 State=UNKNOWN
NodeName=n2 NodeAddr=10.0.10.2 CPUs=2 State=UNKNOWN
</code>
==== Copy the slurm.conf file from master node to all compute nodes ====
<code>
scp slurm.conf root@n1:/etc/slurm/slurm.conf
scp slurm.conf root@n2:/etc/slurm/slurm.conf
</code>
===== configure controller/master node =====
Do the following change and modification on server node
<code>
mkdir /var/spool/slurmctld
chown slurm: /var/spool/slurmctld
chmod 755 /var/spool/slurmctld
mkdir -p /var/log/slurm
chown -R slurm: /var/log/slurm
touch /var/log/slurm/slurmctld.log
chown slurm: /var/log/slurm/slurmctld.log
touch /var/log/slurm/slurm_jobacct.log /var/log/slurm/slurm_jobcomp.log
chown slurm: /var/log/slurm/slurm_jobacct.log /var/log/slurm/slurm_jobcomp.log
</code>
===== configure all compute nodes =====
Do the following changes and modifications on all compute nodes
<code>
mkdir /var/spool/slurmd
chown slurm: /var/spool/slurmd
chmod 755 /var/spool/slurmd
mkdir -p /var/log/slurm
chown -R slurm: /var/log/slurm/
touch /var/log/slurm/slurmd.log
chown slurm: /var/log/slurm/slurmd.log
</code>
===== *Firewall setting =====
  * firewall will block connections between nodes, so I normally disable the firewall on the compute nodes except controller/server node (i.e mgn)
<code>
systemctl stop firewalld
systemctl disable firewalld
</code>
  * controller/master node (i.e mgn) open the default ports that Slurm uses, **NOTE:** not required if **firewalld.service stoped**
<code>
firewall-cmd --permanent --zone=public --add-port=6817/udp
firewall-cmd --permanent --zone=public --add-port=6817/tcp
firewall-cmd --permanent --zone=public --add-port=6818/tcp
firewall-cmd --permanent --zone=public --add-port=6818/tcp
firewall-cmd --permanent --zone=public --add-port=7321/tcp
firewall-cmd --permanent --zone=public --add-port=7321/tcp
firewall-cmd --reload
</code>
===== Check Slurm configuration =====
<code>
slurmd -C
</code>
generates output like:
> ClusterName=(null) NodeName=buhpc3 CPUs=4 Boards=1 SocketsPerBoard=2 CoresPerSocket=2 ThreadsPerCore=1 RealMemory=7822 TmpDisk=45753 UpTime=13-14:27:52
===== Start Slurm service =====
=== Slurm service on compute nodes === 
Start **''slurmd''** service only on all **compute nodes**
<code>
systemctl enable slurmd.service
systemctl start slurmd.service
systemctl status slurmd.service
</code>
=== Slurm service on controler/master node ===
Start **''slurmctld''** service only on **control/master node**
<code>
systemctl enable slurmctld.service
systemctl start slurmctld.service
systemctl status slurmctld.service
</code>
===== Some usefull Slurm commands =====
The following some useful Slurm commands to get details information about node, jod and Slurm envirolment variables 
  * Display all nodes ''**scontrol show nodes**''
  * Display the job queue ''**scontrol show jobs**''
  * List all Slurm evn variables ''**scontrol show config**''

===== Slurm Accounting =====
[[ Slurm configured to collect accounting information ]]
===== Troubelshooting =====
==== Check the logs ====
    * for controller node check **/var/log/slurmctld.log**
    * for compute node check **/var/log/slurmd.log**
==== Fail to start slurmd service on compute node ====
**ERROR: ** recorded at **slurmd.log** file on compute node
<code>
less /var/log/slurmd.log
[2017-10-26T20:07:14.990] Node configuration differs from hardware: CPUs=2:4(hw) Boards=1:1(hw) SocketsPerBoard=2:1(hw) CoresPerSocket=1:2(hw) ThreadsPerCore=1:2(hw)
[2017-10-26T20:07:14.990] Message aggregation disabled
[2017-10-26T20:07:14.990] Resource spec: Reserved system memory limit not configured for this node
[2017-10-26T20:07:14.996] error: cgroup namespace 'freezer' not mounted. aborting
[2017-10-26T20:07:14.996] error: unable to create freezer cgroup namespace
[2017-10-26T20:07:14.996] error: Couldn't load specified plugin name for proctrack/cgroup: Plugin init() callback failed
[2017-10-26T20:07:14.996] error: cannot create proctrack context for proctrack/cgroup
[2017-10-26T20:07:14.996] error: slurmd initialization failed
</code>
**[[https://bugs.schedmd.com/show_bug.cgi?id=3701|RESOLVE]]:**
It is mentatory to modify these two files **cgroup.conf** and **cgroup_allowed_devices_file.conf** over all compute nodes to start **slurmd** service successfully 
  * Modify the **/etc/slurm/cgroup.conf** file
  * Modify the **/etc/slurm/cgroup_allowed_devices_file.conf** file
<code>
cd /etc/slurm
cp cgroup.conf.example cgroup.conf

nano cgroup.conf
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
</code>
<code>
cp cgroup_allowed_devices_file.conf.example cgroup_allowed_devices_file.conf

nano cgroup_allowed_devices_file.conf
/dev/null
/dev/urandom
/dev/zero
/dev/sda*
/dev/cpu/*/*
/dev/pts/*
</code>
==== source install Opem-mpi with Slurm OMPI with PMI support ====
[[https://www.open-mpi.org/faq/?category=slurm|Ref01]], [[https://www.mail-archive.com/devel@lists.open-mpi.org/msg20373.html|Ref02]], [[https://bugs.schedmd.com/show_bug.cgi?id=1978|Ref03]]
<code>./configure --with-devel-headers --prefix=/extra/openmpi3_slurm --with-pmi=/usr --with-pmi-libdir=/usr --with-slurm --with-sge
make -j 4 all
make install
</code>
==== Update node state ====
Ref: [[https://stackoverflow.com/questions/29535118/how-to-undrain-slurm-nodes-in-drain-state|How to “undrain” slurm nodes in drain state]]
<code>
scontrol
</code>
>scontrol: update NodeName=n2 State=DOWN Reason="undraining"
>scontrol: update NodeName=n2 State=RESUME
>scontrol: show node n2
==== Down "virbr0" interface ====
need to make down **virbr0** interface to run Slurm jobs, (OR) stop **virbr0** interface service [[how_to_deactivate_virbr0_virtual_interface_devices_centos_gnome|Ref]]
<code>
ifconfig virbr0 down
</code>
===== Reference =====
  * [[https://www.slothparadise.com/how-to-install-slurm-on-centos-7-cluster/|Installation and configuration]]
  * [[https://slurm.schedmd.com/configurator.easy.html|Create Slurm configuration file]]
  * [[https://bugs.schedmd.com/show_bug.cgi?id=3701|Fail to start slurmd service on compute node]]
  * [[https://slurm.schedmd.com/priority_multifactor.html|job priority]]
  * [[https://support.ceci-hpc.be/doc/_contents/QuickStart/SubmittingJobs/SlurmTutorial.html|Slurm Quick Start Tutorial]]
  * [[https://slurm.schedmd.com/cpu_management.html#Example|CPU Management User and Administrator Guide]]
  * [[https://help.rc.ufl.edu/doc/SLURM_Job_Arrays|Slurm job arrays]]
  * [[http://doc.aris.grnet.gr/|A proper Slurm user documentation (ARIS user support)]]
===== User Guide =====
[[ Slurm workload manager user guide ]]