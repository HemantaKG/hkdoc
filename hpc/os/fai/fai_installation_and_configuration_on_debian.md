## Steps for FAI configuration
Ref: https://fai-project.org/fai-guide/
- Install FAI packages
- Create the ''nfsroot''
- Copy the Examples to the config space and set up your requirements by modifying the required files
- Configure network daemons ''DHCP'' and ''TFTP''
- Building local repository/mirror
- Install the system using FAI server
- Troubleshooting and Reference

## Install FAI packages
- Install the key of the FAI project package repository
- Add the URL of the package repository of the FAI project
- Install the package "fai-quickstart" on your install server.

````
wget -O - http://fai-project.org/download/074BCDE4.asc | apt-key add -
echo "deb http://fai-project.org/download jessie koeln" > /etc/apt/sources.list.d/fai.list
apt-get update
aptitude install fai-quickstart
````

## Building a basic FAI platform for OS provisioning
### Create the ''nfsroot''
- Enable the package repository of the FAI project in a different ''sources.list'' file which is used when building the ''nfsroot''. That ''source.list'' located at **/etc/fai/apt/sources.list**. Edit **/etc/fai/apt/sources.list** to keep the required **repo** and **mirror** urls.
- Edit ''/etc/fai/fai.conf'' and enable the ''log'' keeping properties for FAI installation. Log helps track the installtation fail and other error
- Edit ''/etc/fai/nfsroot.conf'' to set required ''Debian version'' to install, ''root passwd'', path to ''nfsroot'' and other things
- Create a empty ''nfs4'' named folder under ''/srv'' and edit ''/etc/exports'' file
- Run ''fai-setup'' to build the NFSROOT with base packages

## Edit "/etc/fai/apt/sources.list"
````
deb http://http.debian.net/debian jessie main contrib non-free
deb http://security.debian.org/debian-security jessie/updates main contrib non-free
# repository that may contain newer fai packages for jessie
#deb http://fai-project.org/download jessie koeln
# Condor repo
deb http://research.cs.wisc.edu/htcondor/debian/stable/ jessie contrib
# LIGO Packages repo and LSC repo
deb http://www.lsc-group.phys.uwm.edu/daswg/download/software/debian/ jessie contrib
deb http://www.lsc-group.phys.uwm.edu/daswg/download/software/debian/ jessie-proposed contrib
deb http://software.ligo.org/lscsoft/debian/ jessie contrib
deb http://software.ligo.org/lscsoft/debian/ jessie-proposed contrib
deb http://software.ligo.org/gridtools/debian/ jessie contrib
deb http://software.ligo.org/gridtools/debian/ jessie-proposed contrib
deb http://software.ligo.org/gridtools/debian/ jessie main
deb http://software.ligo.org/gridtools/debian/ jessie-proposed main
# Other
deb http://ftp.us.debian.org/debian/ jessie contrib
deb http://ftp.us.debian.org/debian/ jessie main
deb http://ftp.us.debian.org/debian/ jessie non-free
deb http://ftp.us.debian.org/debian/ jessie-backports contrib
deb http://ftp.us.debian.org/debian/ jessie-backports main
deb http://ftp.us.debian.org/debian/ jessie-backports non-free
deb http://ftp.us.debian.org/debian/ jessie-updates contrib
deb http://ftp.us.debian.org/debian/ jessie-updates main
deb http://ftp.us.debian.org/debian/ jessie-updates non-free
````

## Edit "/ect/fai/fai.conf"
````
# See fai.conf(5) for detailed information.
# Account for saving log files and calling fai-chboot.
LOGUSER=fai
SERVER=s
# URL to access the fai config space
# If undefined, use default nfs://<install server>/$FAI_CONFIGDIR
# FAI_CONFIG_SRC=nfs://yourservername/path/to/config/space
FAI_CONFIG_SRC=nfs://storage02/srv/fai/config
#FAI_CONFIG_SRC=nfs://$SERVER/srv/fai/config
# Sending FAI install log files from the install client to the
# FAI server
LOGSERVER=$SERVER
FAI_LOGPROTO=ssh
````
NOTE: change the ''yourservername'' to your server name

## Edit "/etc/fai/nfsroot.conf"
````
For a detailed description see nfsroot.conf(5)
# "<suite> <mirror>" for debootstrap
FAI_DEBOOTSTRAP="wheezy http://httpredir.debian.org/debian"
FAI_ROOTPW='$1$kBnWcO.E$djxB128U7dMkrltJHPf6d1'
NFSROOT=/srv/fai/nfsroot
TFTPROOT=/srv/tftp/fai
NFSROOT_HOOKS=/etc/fai/nfsroot-hooks/
FAI_DEBOOTSTRAP_OPTS="--exclude=info"
# Configuration space
FAI_CONFIGDIR=/srv/fai/config
````
NOTE: default root passwd //fai//, change 

## Create an empty "nfs4" directory
create an empty **nfs4** directory under **/srv**. Add the direcory info to **/etc/export** file for //NFS// mount
````
mkdir /srv/nfs4
nano /etc/exports
/srv/nfs4 fsid=0
````

## Build the NFSROOT with base packages
````
fai-setup -v
````
You will get the following block of message, if ''fai-setup'' and ''nfsroot'' build are finish's successfully :-)
>   You have no FAI configuration space yet. Copy the simple examples with:
>   cp -a /usr/share/doc/fai-doc/examples/simple/* /srv/fai/config
>   Then change the configuration files to meet your local needs.
> Please don't forget to fill out the FAI questionnaire after you've finished your project with FAI.
>
>FAI setup finished.

## Building FAI platform with requirements
Processed further if the basic FAI platform build complicated successfully 8-o
### Copy sample configuration
As prompted by ''fai-setup'' run, copy the sample configurations to your fai build directory as follows
````
cp -a /usr/share/doc/fai-doc/examples/simple/* /srv/fai/config
````

### Setup OS provisioning requirements
#### set timezone
set **timezone**, **root-pw** for the new OS installation in file **/srv/fai/config/class/FAIBASE.var**
````
#timezone

UTC=no
TIMEZONE=Asia/Kolkata
````

#### partition HDD
Add the HD disk partition details to ''/srv/fai/config/disk_config/FAIBASE'' file
````
root@storage02:~# nano /srv/fai/config/disk_config/FAIBASE

# example of new config file for setup-storage
#
# <type> <mountpoint> <size>   <fs type> <mount options> <misc options>

disk_config disk1 disklabel:msdos bootable:1 fstabkey:uuid

#primary /      2G-15G   ext4  rw,noatime,errors=remount-ro
#logical swap   200-1G   swap  sw
#logical /tmp   100-1G   ext4  rw,noatime,nosuid,nodev createopts="-L tmp -m 0" tuneopts="-c 0 -i 0"
#logical /home  100-50%  ext4  rw,noatime,nosuid,nodev createopts="-L home -m 1" tuneopts="-c 0 -i 0"

#ADDED BY HEMANTA
# file system partition details for nodes...
#primary        /boot           500     ext4    rw,noatime
#primary        /               200G    ext4    rw,noatime,errors=remount-ro
#logical        swap            64G     swap    sw
#logical        /scratch        666G    ext4    rw,noatime,errors=remount-ro

# file system partition details for master (humpty and dumpty)
primary        /boot           500     ext4    rw,noatime
primary        /               200G    ext4    rw,noatime,errors=remount-ro
logical        swap            64G     swap    sw
logical        /scratch        619G    ext4    rw,noatime,errors=remount-ro

# file system partition details for storage and archive
#primary        /boot           500     ext4    rw,noatime
#primary        /               200G    ext4    rw,noatime,errors=remount-ro
#logical        swap            64G     swap    sw

````

#### Packages needed on new installation
Create a file with the list of all the **package names** under ''/srv/fai/config/package_config/'' directory. The filename must be in **block letters**. //NOTE:// to avoide confusion, it is better to give the filename same as the package name (or) package group type name. The following file we created for our requirement
- /srv/fai/config/package_config/GANGLIA_MASTER
- /srv/fai/config/package_config/GANGLIA_NODE
- /srv/fai/config/package_config/CONDOR_MASTER
- /srv/fai/config/package_config/CONDOR_NODE
- /srv/fai/config/package_config/LIGO_PACK
- /srv/fai/config/package_config/GNOME
- /srv/fai/config/package_config/NIS
- /srv/fai/config/package_config/MISC

````
root@storage02:~# cat /srv/fai/config/package_config/GANGLIA_MASTER
PACKAGES aptitude
ganglia-monitor
rrdtool gmetad
ganglia-webfrontend
````

````
root@storage02:~# cat /srv/fai/config/package_config/GANGLIA_NODE 
PACKAGES aptitude
ganglia-monitor
````

````
root@storage02:~# cat /srv/fai/config/package_config/CONDOR_MASTER 
PACKAGES aptitude
condor
````

````
root@storage02:~# cat /srv/fai/config/package_config/CONDOR_NODE 
PACKAGES aptitude
condor
````

````
root@storage02:~# cat /srv/fai/config/package_config/NIS 
PACKAGES aptitude
nis
````

````
root@storage02:~# cat /srv/fai/config/package_config/LIGO_PACK 
PACKAGES aptitude
lsb-release
ldg-client
globus-proxy-utils
ldg-server
lscsoft-lalsuite-dev
lscsoft-external
lscsoft-all
````

````
root@storage02:~# cat /srv/fai/config/package_config/MISC 
PACKAGES aptitude
#General pack
htop
sudo
ntp
vim
dvipng

#Other python pack
numpy
healpy
scipy
hashmap
matplotlib
corner
six
h5py
healpy
python-tk
astropy

#Exter LaTex Fonts
texlive-latex-extra
texlive-fonts-recommended
````

### Configure all packages for new installation
Put the package configuration files under ''/srv/fai/config/files/etc/<package_name>'' directory.
- create folder **condor** under ''/srv/fai/config/files/etc/'' and keep **condor configuration files** under ''/srv/fai/config/files/etc/condor/''

````
root@storage02:~# ls -l /srv/fai/config/files/etc/condor/
-rw-r--r-- 1 storage02 storage02   1040 Dec 20 00:15 condor_config_local_manager
--rw-r--r-- 1 root      root        1029 Dec 19 23:51 condor_config_local_node
--rw-r--r-- 1 storage02 storage02   1088 Dec 20 00:01 condor_config_local_submit
--rw-r--r-- 1 storage02 storage02 111359 Dec 20 00:19 condor_config_manager
--rw-r--r-- 1 storage02 storage02 111395 Dec 19 23:59 condor_config_node
--rw-r--r-- 1 storage02 storage02 111381 Dec 20 00:13 condor_config_submit
````
- Create a folder **ganglia** under ''/srv/fai/config/files/etc/'' keep **ganglia configuration files** under ''/srv/fai/config/files/etc/ganglia/''
````
root@storage02:~# ls -l /srv/fai/config/files/etc/ganglia/
-rw-r--r-- 1 storage02 storage02 7948 Nov  4  2016 gmetad.conf.master
--rw-r--r-- 1 storage02 storage02 8080 Nov  4  2016 gmond.conf.master
--rw-r--r-- 1 root      root      8066 Dec 20 00:21 gmond.conf.node
````
- Create a floder **apache** under ''/srv/fai/config/files/etc/'' and keep **apache configuration files** under ''/srv/fai/config/files/etc/apache2/''
````
root@storage02:~# ls -l /srv/fai/config/files/etc/apache2/
drwxr-xr-x 2 root root 4096 Nov  4  2016 sites-enabled
````
- keep **hosts file** user ''/srv/fai/config/files/etc/hosts/''
````
root@storage02:~# ls -l /srv/fai/config/files/etc/hosts/
-rw-r--r-- 1 root root 2271 Dec 20 12:14 DEBIAN
````
NOTE: Here **DEBIAN** is a class, this file contains the **/etc/hosts** file details.

### Add shell script files to perform some required default configurations setting at the final stage to FAI and change access mode to "-rwxr-xr-x"
#### Add script file under ''/srv/fai/config/scrip/LAST/''
Filename: 90-ganglia-conf
````
    root@storage02:~# cat /srv/fai/config/scripts/LAST/90-ganglia-conf 
    #! /bin/bash
    
    #Ganglia configuration
    case $HOSTNAME in
            crm|node*|storage*|archive)
                    cp -aurf /var/lib/fai/config/files/etc/ganglia/gmond.conf.node /target/etc/ganglia/gmond.conf; ;;
            humpty|dumpty)
                    cp -aurf /var/lib/fai/config/files/apache2/site-enabled/ganglia.conf.master /target/etc/apache2/sites-enabled/ganglia.conf;
                    cp -aurf /var/lib/fai/config/files/etc/ganglia/gmond.conf.master /target/etc/ganglia/gmond.conf;
                    cp -aurf /var/lib/fai/config/files/etc/ganglia/gmetad.conf.master /target/etc/ganglia/gmetad.conf; ;;
    esac
````
Filename: 91-condor-conf
````
    root@storage02:~# cat /srv/fai/config/scripts/LAST/91-condor-conf 
    #! /bin/bash
    
    #Condor configuration files
    case $HOSTNAME in
            humpty|dumpty)
        	CONFIG_LOCAL_FILE=condor_config_local_submit;
		CONFIG_FILE=condor_config_submit; ;;
            node*)
        	CONFIG_LOCAL_FILE=condor_config_local_node;
		CONFIG_FILE=condor_config_node; ;;
            crm*)
        	CONFIG_LOCAL_FILE=condor_config_local_manager;
		CONFIG_FILE=condor_config_manager; ;;
    esac
    cp -aurf /var/lib/fai/config/files/etc/condor/$CONFIG_LOCAL_FILE /target/etc/condor/condor_config.local
    cp -aurf /var/lib/fai/config/files/etc/condor/$CONFIG_FILE /target/etc/condor/condor_config
````
Filename: 92-nis-conf
````
    root@storage02:~# cat /srv/fai/config/scripts/LAST/92-nis-conf 
    #! /bin/bash
    
    #NIS client configuration file
    case $HOSTNAME in
            node*|crm|storage*|archive)
                    cp -aurf /var/lib/fai/config/files/etc/yp.conf.tmp /target/etc/yp.conf;
                    cp -aurf /var/lib/fai/config/files/etc/nsswitch.conf.tmp /target/etc/nsswitch.conf; ;;
    #                cp -aurf /var/lib/fai/config/files/etc/pam.d/common-session.tmp /target/etc/pam.d/common-session;;
    #
    #       humpty|dumpty)
    #                cp -aurf /var/lib/fai/config/files/etc/default/nis.master /target/etc/default/nis;;
    #                cp -aurf /var/lib/fai/config/files/etc/ypserv.securenets.master /target/etc/ypserv.securenets;;
    #                cp -aurf /var/lib/fai/config/files/var/yp/Makefile.master /target/var/yp/Makefile;;
    esac
````
Filename: 93-nfs-mount-conf
````
    root@storage02:~# cat /srv/fai/config/scripts/LAST/93-nfs-mount-conf 
    #! /bin/bash
    
    # storage zpool mount
    case $HOSTNAME in
            humpty|dumpty|node*)
            echo "10.0.0.10:/home     /home   nfs     defaults        0       0" >> /target/etc/fstab;;
    esac
````
Filename: 94-misc-conf
````
    root@storage02:~# cat /srv/fai/config/scripts/LAST/94-misc-conf 
    #! /bin/bash
    
    # copy resolve.conf file to all nodes
    cp -aurf /var/lib/fai/config/files/etc/resolv.conf.tmp /target/etc/resolv.conf
````

## FAI host wise installation
- add the following lines into ''/srv/fai/config/class/50-host-classes'' to specify the host wise installation differences
````
    ...
    node*)
        # Classes associated to the compute node...
        echo "FAIBASE DEBIAN DHCPC XORG XFCE CONDOR_NODE GANGLIA_NODE LIGO_PACK NIS MISC";;
    master*|humpty|dumpty)
        # Classes associated to the master node NIS removed...
        echo "FAIBASE DEBIAN DHCPC XORG XFCE CONDOR_MASTER GANGLIA_MASTER LIGO_PACK LIGO_DATAFIND MISC";;
    crm)
        # Classes associated to the Cluster Resource Manager
        echo "FAIBASE DEBIAN DHCPC XORG XFCE CONDOR_MASTER GANGLIA_NODE NIS MISC1";;
    storage*|archive)
        # Classes associated to the Storage Node
        echo "FAIBASE DEBIAN DHCPC XORG XFCE STORAGE GANGLIA_NODE NIS MISC1";;
    ...
````

## Configure "dhcp" network daemons
- For booting the install client via ''PXE'', the install server needs a ''DHCP'' server and a ''TFTP'' server daemon running on ''FAI'' server. The package ''fai-quickstart'' has already installed the software packages for those daemons.
- Only additional, the package of the ''NFS'' server for exporting the ''nfsroot'' and the config space was installed.
````
    apt-get install syslinux-common
````
- Configure ''DHCP'' server and add clients by modifi ''/etc/dhpcd/dhcpd.conf'' file as follow
````
    # common set up listed here...
    option domain-name "<<domain name>>";
    filename "fai/pxelinux.0";
    option routers 10.0.0.2;
    next-server storage02;
    server-name storage02;
    option domain-name-servers 8.8.8.8;
    
    # we have defined our range of addresses as 10.0.0.1 to 10.0.0.254
    subnet 10.0.0.0 netmask 255.255.255.0 {
       group{
               host node032{
                    hardware ethernet 00:25:90:FD:74:B2;
                    fixed-address 10.0.0.42;
                    option host-name "node032";
                    }
            }
    }
````
- Add ''FQHN'' to ''/etc/hosts'' file
````
    #fai server
    10.0.0.9	storage02.<<domain>>	storage02
    #nodes
    10.0.0.42	node032.<<domain>>	node032
````

## Building local repository/mirror
Ref:[[http://fai-project.org/fai-guide/#_a_id_debian_mirror_a_how_to_create_a_local_debian_mirror|How to create a local Debian mirror]]
- Create a Debian package mirror with required installation packages to a local directory ex here ''/srv/scratch/dt170918''
````
    fai-mirror -v -c CONDOR_NODE,DEBIAN,FAIBASE,FAISERVER,GANGLIA_NODE,NIS,XFCE,XORG,GNOME,MISC,MISC1,LIGO_PACK /srv/scratch/dt170918
````
- sys-link the above-created directory to ''/var/www/<<mirror-name>>''
````
    ln -s /srv/scratch/dt170918 /var/www/mirror170918
````
- Create a file ''sources.list'' in ''/etc/fai/apt'' directory which gives access to your local Debian mirror.

## Check "/srv/fai/nfsroot/etc/apt/source.list"
```
    # Local Mirror
    deb http://10.0.0.9/alice_mirror cskoeln main contrib non-free
    deb http://http.debian.net/debian jessie main contrib non-free
    deb http://security.debian.org/debian-security jessie/updates main contrib non-free
    # repository that may contain newer fai packages for jessie
    #deb http://fai-project.org/download jessie koeln
    #deb http://10.0.0.9/alice_mirror cskoeln main contrib non-free
````

## Install system using FAI server
````
/etc/init.d/isc-dhcp-server restart
/etc/init.d/tftpd-hpa restart

fai-chboot -IFv -u nfs://storage02/srv/fai/config humpty
````
NOTE: change the node name (i.e here "humpty") to required node that you want to install)

## Troubleshooting and Reference
#### PXE Boot and TFTP issues
- PXE-E32 TFTP timeout
 - Check NIS client service of FAI server running node, if NIS client running than stop NIS service. (NOTE: if NIS client of FAI server sending request to NIS server running on the node to which we are trying to install using FAI)
 - REF: [[https://docs.oracle.com/cd/E19045-01/b200x.blade/817-5625-10/Linux_Troubleshooting.html]]

- To resolve static IP changing to dynamic automatically after some time
- check for ''dhclient'' running ''ps -ef | grep dhclient''
 - if dhclient running kill it ''kill <<dhclient process ID>>''
 - reset network interface (here eth0) ''ifdown eth0 && ifup eth0''
 - check interface ''ifconfig -a''
 - Ref: [[https://unix.stackexchange.com/questions/205857/static-ip-changes-to-dynamic-automatically-after-time]]
- If PXE boot throws an error ''PXE-E11: ARP timeout'', then check ''/etc/dhcp/dhcp.conf'' file and make sure ''next-server, server-name'' the corrent IP/hostname.
  - [[gpg_error|GPG key error]]

### nfsroot build fail (or) fai-setup fail
ERROR:
```
    The following packages have unmet dependencies:
     dracut-config-generic : Depends: dracut-core but it is not going to be installed
    ...
    ERROR when calling fai-make-nfsroot.
````
Ref: [[https://github.com/faiproject/fai/blob/master/conf/NFSROOT|Resolve]]: Add the following ''deb repo'' to ''/etc/fai/apt/source.list''
````
deb http://fai-project.org/download jessie koeln
````
