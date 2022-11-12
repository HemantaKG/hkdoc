### Host Details:
- Controller OR Master Node
  - hostname: mgn
  - FQDN: mng.test.cluster
  - ip: 10.0.10.20
- Compute Node(s)
  - hostname n1, n2
  - FQDN: n1.test.cluster, n1.test.cluster
  - ip: 10.0.10.21, 10.0.10.22

# Make xCAT master node ready for xCAT installation and configuration:
The following are pre-installation steps; must check before going for xCAT installation and configuration
- **Update OS** ''yum update''
- Disable **SELinux**
- Add **IP**, **FQDN**, **hostname** into **/etc/hosts** file
- Add **hostname** into **/etc/hostname** file
- **reboot** the system
- After reboot please check **hostname** and **domain name**; with commands ''hostname'' and ''hostname -d'' respectively
- [optional] configure **NFS server** on master node and set **NFS mount** directories /home, /opt, /share ... if your are planning to mount some directories on compute nodes

## Mount iso file and add its repo
### Copy iso file, create directory and mount iso
````
mkdir -p /mnt/iso/centos7
mount -o loop /root/iso/CentOS-7-x86_64-DVD-1708.iso /mnt/iso/centos7
````

## Create a yum repo file:
Create a repo file for above mounted OS disk.
````
nano /etc/yum.repos.d/centos7-dvd.repo

[centos7-dvd]
name=Centos 7 packages
baseurl=file:///mnt/iso/centos7
enabled=1
gpgcheck=1
````

# xCAT package installation:
Install latest stable version
````
wget https://raw.githubusercontent.com/xcat2/xcat-core/master/xCAT-server/share/xcat/tools/go-xcat -O - > /tmp/go-xcat
chmod +x /tmp/go-xcat
/tmp/go-xcat install
````
**NOTE:** for first-time installation source **xcat.sh** file
````
source /etc/profile.d/xcat.sh
````
**optional:** If you want ot install latest development version ''/tmp/go-xcat -x devel install''

# Prepare master for OS provisioning:
## Set some useful environment variables
Set following environment variables. Which make the xCAT configuration easier.
````
export sms_name=master
export sms_ip=10.0.10.20
export domain_name=test.cluster
export sms_eth_internal=enp2s0
export internal_netmask=255.255.255.0
export ntp_server=10.0.10.20
export num_computes=2
export c_ip=( "10.0.10.21" "10.0.10.22" )
export c_mac=( "74:27:EA:D1:BF:C6" "74:27:EA:02:5B:48" )
export c_name=( "n1" "n2" )
export compute_regex="n*"
export compute_prefix="n"
````

## Create an osimage object definition:
XCAT uses ''copycds'' command to create an image which will be available to install nodes
````
copycds /root/os_iso/CentOS-7-x86_64-DVD-1708.iso
````
>[root@master xcat_os_prov]# copycds CentOS-7-x86_64-DVD-1708.iso 
>>Copying media to /install/centos7.4/x86_64
>>Media copy operation successful

- List all osimage definitions that are created by ''copycds'' (REF: command; [[http://xcat-docs.readthedocs.io/en/stable/guides/admin-guides/basic_concepts/node_type.html|for more information]])
- Shows the list of all os images created by above statement
````
lsdef -t osimage
````
>[root@master xcat_os_prov]# lsdef -t osimage
>>centos7.4-x86_64-install-compute  (osimage)
>>centos7.4-x86_64-netboot-compute  (osimage)
>>centos7.4-x86_64-statelite-compute  (osimage)

- Shows the details information of given os image
````
lsdef -t osimage centos7.4-x86_64-install-compute
````
>[root@master xcat_os_prov]# lsdef -t osimage centos7.4-x86_64-install-compute
>>Object name: centos7.4-x86_64-install-compute
>>    imagetype=linux
>>    osarch=x86_64
>>    osdistroname=centos7.4-x86_64
>>    osname=Linux
>>    osvers=centos7.4
>>    otherpkgdir=/install/post/otherpkgs/centos7.4/x86_64
>>    pkgdir=/install/centos7.4/x86_64
>>    pkglist=/opt/xcat/share/xcat/install/centos/compute.centos7.pkglist
>>    profile=compute
>>    provmethod=install
>>    template=/opt/xcat/share/xcat/install/centos/compute.centos7.tmpl
- **NOTE:** For **statefull** OS installation on compute node, use OS image **centos7.4-x86_64-install-compute**

## Modify the default kickstart file:
### Set node root password
Modify the **default kickstart file** as follow
- add timezone
- add root passwd
````
nano /opt/xcat/share/xcat/install/centos/compute.centos7.tmpl

timezone Asia/Kolkata
rootpw --iscrypted Xau2d7MuvWSX6
````
- **NOTE:**
  * Always add encrypted password; its mandatory and secure
  * generate crypt by using any method; using perl inline command as follow
    * password **_r00t_00** is encrypted using following **perl inline command**
````
perl -e 'print crypt("_r00t_00","Xa") . "\n";'p
````

## Add post installation tasks:
Add **post installation** tasks into **post installation block** of default kickstart file
- post installation block starts with **%post** and ends at **%end**
- Here, we are adding following post-installation tasks:
  - NFS directory mount
  - adding GATEWAY into an interface file

````
nano /opt/xcat/share/xcat/install/centos/compute.centos7.tmpl

%post
# NFS mount point; to mount master nodes "/home" and "/share" directories
echo "10.0.10.20:/home    /home    nfs     defults    0    0" >> /etc/fstab
echo "10.0.10.20:/share    /share    nfs     defults    0    0" >> /etc/fstab
# set gateway to get internet access
echo "GATEWAY=10.0.10.20" >> /etc/sysconfig/network-scripts/ifcfg-eno1
...
%end
````

## Define custom disk partition details
- Make a directory namely **custom** under **/install**
- Create a file under **/install/custom** and define custom disk partition details.
- Add/update osimage object's **partitionfile** propertity value  

### Make a custom directory
````
mkdir -p /install/custom/
cd /install/custom
````

### Create file with partition details:
````
cd  /install/custom
nano my-partitions

# Partition clearing information
clearpart --all --initlabel

# Disk partitioning information in MB
part /boot --asprimary --fstype="ext4" --size=1024
part / --asprimary --fstype="ext4" --size=200000
part /scratch --fstype="ext4" --size=666000
part swap --fstype="swap" --size=64000
````

### Add/Update partition file to xact object osimage:
````
chdef -t osimage centos7.4-x86_64-install-compute partitionfile=/install/custom/my-partitions
````
>[root@master custom]# lsdef -t osimage centos7.4-x86_64-install-compute
>>Object name: centos7.4-x86_64-install-compute
>>    imagetype=linux
>>    osarch=x86_64
>>    osdistroname=centos7.4-x86_64
>>    osname=Linux
>>    osvers=centos7.4
>>    otherpkgdir=/install/post/otherpkgs/centos7.4/x86_64
>>    partitionfile=/install/custom/my-partitions
>>    pkgdir=/install/centos7.4/x86_64
>>    pkglist=/opt/xcat/share/xcat/install/centos/compute.centos7.pkglist
>>    profile=compute
>>    provmethod=install
>>    template=/opt/xcat/share/xcat/install/centos/compute.centos7.tmpl

## Set for file synchronization after OS installation:
The **synclist file** contains the configuration entries that specify where the files should be synced to
- Make a derictory namely **install** under **/install/custom**
- Create a synclist file **compute.synclist**
- Add entries to synclist file
````
mkdir -p /install/custom/install
touch /install/custom/install/compute.synclist
````

## Add entries to synclist file:
````
echo "/etc/hosts -> /etc/hosts" > /install/custom/install/compute.synclist
    ...
````
### Add/Update synclist file to xcat osimage object:
````
chdef -t osimage -o centos7.4-x86_64-install-compute synclists=/install/custom/install/compute.synclist
````
>[root@master install]# lsdef -t osimage centos7.4-x86_64-install-compute
>>Object name: centos7.4-x86_64-install-compute
>>    imagetype=linux
>>    osarch=x86_64
>>    osdistroname=centos7.4-x86_64
>>    osname=Linux
>>    osvers=centos7.4
>>    otherpkgdir=/install/post/otherpkgs/centos7.4/x86_64
>>    partitionfile=/install/custom/my-partitions
>>    pkgdir=/install/centos7.4/x86_64
>>    pkglist=/opt/xcat/share/xcat/install/centos/compute.centos7.pkglist
>>    profile=compute
>>    provmethod=install
>>    synclists=/install/custom/install/compute.synclist
>>    template=/opt/xcat/share/xcat/install/centos/compute.centos7.tmpl

## Install additional packages and other packages:
- **NOTE:** There are two kinds of packages as follow
- The packages which either directly avaliable from OS official destro or comes alonge with OS DVD/CD. The xCAT default package list file (i.e. **/opt/xcat/share/xcat/install/centos/compute.centos7.pkglist**) contains the names of those packages
- The packages which neither directly avaliable from OS official destro nor comes alonge with OS DVD/CD.  They are stored in file **compute.otherpkgs.pkglist** under **/install/custom/install/centos/**
## Add common OS distro packages to "compute.centos7.pkglist" file
Add the common distro packages/package-group to the **compute.centos7.pkglist** file. These packages avaliable under the mounted directory. The following required packages and package-group are added for 
````
chdef -t osimage centos7.4-x86_64-install-compute pkglist=/opt/xcat/share/xcat/install/centos/compute.centos7.pkglist

nano /opt/xcat/share/xcat/install/centos/compute.centos7.pkglist

wget
ntp
nfs-utils
net-snmp
rsync
yp-tools
openssh-server
util-linux
net-tools
bash
openssl
@ GNOME
@ X Window System
@ Development Tools
@ Scientific Support
@ System Administration Tools
vim
nano
httpd
````

## Add other packages list
- make a directory **/install/post/otherpkgs/centos7.4/x86_64**
- move into the above directory
- copy all rmp file (of other package) into above directory
- run ''createrepo'' command
- Create a file with name **otherpkgs.list** and all other packages names in it
- Add/Update **otherpkgsdir** directory and **otherpkgs.list** file to osimage object defination
### make a directory, move in, copy rpm files and create repo
````
mkdir -p /install/post/otherpkgs/centos7.4/x86_64
cd /install/post/otherpkgs/centos7.4/x86_64
cp myrpms/* .
createrepo .
````
### Create a file and add list of rmp names
````
mkdir /install/custom/install/centos
nano /install/custom/install/centos/compute.otherpkgs.pkglist
myrmp1
myrpm2
...
````

## Add/Update above created directory and file to osimage defination
````
chdef -t osimage centos7.4-x86_64-install-compute otherpkgdir=/install/post/otherpkgs/centos7.4/x86_64 otherpkglist=/install/custom/install/centos/compute.otherpkgs.pkglist
````
>[root@master ~]# lsdef -t osimage centos7.4-x86_64-install-compute
>>Object name: centos7.4-x86_64-install-compute
>>    imagetype=linux
>>    osarch=x86_64
>>    osdistroname=centos7.4-x86_64
>>    osname=Linux
>>    osvers=centos7.4
>>    otherpkgdir=/install/post/otherpkgs/centos7.4/x86_64
>>    otherpkglist=/install/custom/install/centos/compute.otherpkgs.pkglist
>>    partitionfile=/install/custom/my-partitions
>>    pkgdir=/install/centos7.4/x86_64
>>    pkglist=/opt/xcat/share/xcat/install/centos/compute.centos7.pkglist
>>    profile=compute
>>    provmethod=install
>>    synclists=/install/custom/install/compute.synclist
>>    template=/opt/xcat/share/xcat/install/centos/compute.centos7.tmpl

# OS provisioning
source the env variable file "env_set.txt"
```
source env_set.txt
````
## Limit dhcp allow interface
````
chdef -t site dhcpinterfaces="xcatmn|${sms_eth_internal}"
````
## Genetrate dhcp configuration file
- **NOTE:** check/keep dhcp.service on before running the below command to generate new dhcp.conf file
````
makedhcp -n
````
## Define IP/MAC for all compute nodes and create a group "compute"
- Define all compute nodes and make a group
````
for ((i=0; i<$num_computes; i++)) ; do mkdef -t node ${c_name[i]} groups=compute,all ip=${c_ip[i]} mac=${c_mac[i]} netboot=pxe; done
````
- Set domain name
````
chdef -t site domain=${domain_name}
````
- Set xCAT OS provision method
````
chdef -t group compute provmethod=centos7.4-x86_64-install-compute
````
- Make hosts, network and dns
````
makehosts
makenetworks 
makedns -n
````
- Get the node ready for OS installation
````
nodeset compute osimage=centos7.4-x86_64-install-compute
````
- Restart DHCP service
````
service dhcpd restart
````
> Finally your ready to start PXE boot on all nodes, for OS installation with xCAT :-)
----

# Troubleshooting
- [[how_to_deactivate_virbr0_virtual_interface_devices_centos_gnome|How to deactivate "virbr0"]]
----

# Reference
- [[http://xcat-docs.readthedocs.io/en/stable/guides/install-guides/yum/|xCAT document]]
- [[http://xcat-docs.readthedocs.io/en/stable/guides/admin-guides/references/man1/xdsh.1.html|xdsh - Concurrently runs remote commands on multiple nodes]]
----

### Files used
- text env_set.txt
````txt
##set env for 4 nodes

export sms_ip=10.10.48.2
export domain_name=<<change domain>>
export sms_eth_internal=ens2f0
export internal_netmask=255.255.248.0
export ntp_server=10.10.48.2
export num_computes=4

export c_ip=( "10.10.48.11" "10.10.48.12" "10.10.48.13" "10.10.48.14" )

export c_mac=( 
"d0:67:26:d3:c0:72" "d0:67:26:d2:7a:3a" "d0:67:26:d2:7b:b6" "d0:67:26:d3:c6:ee" )

export c_name=( "cn1" "cn2" "cn3" "cn4" )

export compute_regex="cn*"
export compute_prefix="cn"
````

- compute.centos7.tmpl
````bash
#
#cmdline

lang en_US
#KICKSTARTNET#

#
# Where's the source?
# nfs --server hostname.of.server or IP --dir /path/to/RH/CD/image
#
#nfs --server #XCATVAR:INSTALL_NFS# --dir #XCATVAR:INSTALL_SRC_DIR#

%include /tmp/repos

#device ethernet e100
keyboard "us"

#
# Clear the MBR
#
zerombr

#
# Wipe out the disk
#
clearpart --all --initlabel
#clearpart --linux

#
# Customize to fit your needs
#

#XCAT_PARTITION_START#
# xCAT based partitioning
%include /tmp/partitionfile
#No RAID
#/boot really significant for this sort of setup nowadays?
#part /boot --size 50 --fstype ext3
#part swap --size 1024
#part / --size 1 --grow --fstype ext4

#RAID 0 /scr for performance
#part / --size 1024 --ondisk sda
#part swap --size 512 --ondisk sda
#part /var --size 1024 --ondisk sdb
#part swap --size 512 --ondisk sdb
#part raid.01 --size 1 --grow --ondisk sda
#part raid.02 --size 1 --grow --ondisk sdb
#raid /scr --level 0 --device md0 raid.01 raid.02

#Full RAID 1 Sample
#part raid.01 --size 50 --ondisk sda
#part raid.02 --size 50 --ondisk sdb
#raid /boot --level 1 --device md0 raid.01 raid.02
#
#part raid.11 --size 1024 --ondisk sda
#part raid.12 --size 1024 --ondisk sdb
#raid / --level 1 --device md1 raid.11 raid.12
#
#part raid.21 --size 1024 --ondisk sda
#part raid.22 --size 1024 --ondisk sdb
#raid /var --level 1 --device md2 raid.21 raid.22
#
#part raid.31 --size 1024 --ondisk sda
#part raid.32 --size 1024 --ondisk sdb
#raid swap --level 1 --device md3 raid.31 raid.32
#
#part raid.41 --size 1 --grow --ondisk sda
#part raid.42 --size 1 --grow --ondisk sdb
#raid /scr --level 1 --device md4 raid.41 raid.42
#XCAT_PARTITION_END#

#
# bootloader config
# --append <args>
# --useLilo
# --md5pass <crypted MD5 password for GRUB>
#
#The bootloader config here is commented out
#For user customized partition file or partition script,
#the bootloader configuration should be specified in the user customized partition file/script
#For the xCAT default partition scheme, the bootloader configuration is in /tmp/partitionfile
#which is generated in %pre section
##KICKSTARTBOOTLOADER#

#
# install or upgrade
#
install

#
# text mode install (default is graphical)
#
text

#
# firewall
#
firewall --disabled

#
# Select a zone
# Add the --utc switch if your hardware clock is set to GMT
#
#timezone US/Hawaii
#timezone US/Pacific
#timezone US/Mountain
#timezone US/Central
#timezone US/Eastern
timezone --utc "#TABLE:site:key=timezone:value#"

#
# Don't do X
#
skipx


#
# To generate an encrypted root password use:
#
# perl -e 'print crypt("blah","Xa") . "\n";'p
# openssl passwd -apr1 -salt xxxxxxxx password
#
# where "blah" is your root password.
#
#rootpw --iscrypted XaLGAVe1C41x2
#rootpw XaLGAVe1C41x2 --iscrypted
#rootpw --iscrypted #CRYPT:passwd:key=system,username=root:password#
#password _r00t_00
rootpw --iscrypted Xau2d7MuvWSX6

#
# NIS setup: auth --enablenis --nisdomain sensenet
# --nisserver neptune --useshadow --enablemd5
#
# OR
auth --useshadow --enablemd5


#
# SE Linux
#
selinux --disabled

#
# Reboot after installation
#
reboot

#
#end of section
#
%packages
#INCLUDE_DEFAULT_PKGLIST#
%end
%pre
{
echo "Running Kickstart Pre-Installation script..."
#INCLUDE:#ENV:XCATROOT#/share/xcat/install/scripts/pre.rh.rhels7#
} &>>/tmp/pre-install.log
%end
%post
# NFS mount over compute nodes
echo "10.10.0.2:/home        /home  nfs     defaults        0	0" >> /etc/fstab
echo "10.10.0.2:/share        /share   nfs     defaults        0	0" >> /etc/fstab

# set gateway to get internet access
echo "GATEWAY=10.10.0.2" >> /etc/sysconfig/network-scripts/ifcfg-em1

mkdir -p /var/log/xcat/
{
cat >> /var/log/xcat/xcat.log << "EOF"
%include /tmp/pre-install.log
EOF
echo "Running Kickstart Post-Installation script..."
#INCLUDE:#ENV:XCATROOT#/share/xcat/install/scripts/post.xcat#
#INCLUDE:#ENV:XCATROOT#/share/xcat/install/scripts/post.rhels7#
} &>>/var/log/xcat/xcat.log
%end
</code>

<code bash my-partitions>
# Partition clearing information
clearpart --all --initlabel

# Disk partitioning information in MB
part /boot --asprimary --fstype="ext4" --size=1024
part / --asprimary --fstype="ext4" --size=200000
part /scratch --fstype="ext4" --size=666000
part swap --fstype="swap" --size=64000
````
- compute.synclist
````bash
###########################################
## Before installation                   ##
## uncomment at OS installation phase    ##
###########################################

# uncomment to copy "hosts" file
#/etc/hosts -> /etc/hosts

# uncomment to copy NFS configuration file
#/etc/idmapd.conf -> /etc/idmapd.conf

############################################
## After installation                     ##
## After post_boot_installation phase     ##
############################################

## Ganglia configuration file copy
## uncomment and run "updatenode" for ganglia "gmond.conf" file copy
#/etc/ganglia/gmond.conf -> /etc/ganglia/gmond.conf

## Slurm configuration file copy
## uncomment and run "updatenode" for slurm configuration
#/etc/munge/munge.key -> /etc/munge/munge.key
/etc/slurm/slurm.conf -> /etc/slurm/slurm.conf
#/home/it/xcat_os_prov/slurm_node/cgroup_allowed_devices_file.conf -> /etc/slurm/cgroup_allowed_devices_file.conf
#/home/it/xcat_os_prov/slurm_node/cgroup.conf -> /etc/slurm/cgroup.conf
````

- compute.centos7.pkglist
````bash
#Please make sure there is a space between @ and group name
wget
ntp
nfs-utils
net-snmp
rsync
yp-tools
openssh-server
util-linux
net-tools
bash
openssl
@ GNOME
@ X Window System
@ Development Tools
@ Scientific Support
@ System Administration Tools
vim
nano
httpd
````

- compute.otherpkgs.pkglist
````bash
epel-release
ganglia-gmond
libconfuse
ganglia
````
