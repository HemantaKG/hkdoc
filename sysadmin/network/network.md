# Packate forwarding
### First flash all ''iptable'' settings before ''netting''
````
iptables -F
````
### Now run the below commands for ''netting''
NOTE: Public interface ''enp0s29u1u6'' and Local interface ''enp3s0''
````
iptables -t nat -A POSTROUTING -o enp0s29u1u6 -j MASQUERADE
iptables -A FORWARD -i enp3s0 -j ACCEPT
````
NOTE:
* ''/etc/resolve.conf'' and ''GATEWAY'' was definded but still node not getting internet and ''ping 8.8.8.8'' not pinging, than do ''iptable'' flash and rerun the ''netting''

### Enable forwarding on CentOS\Rocky:
Add the following to bottom of the file ''/etc/sysctl.conf''
````
net.ipv4.ip_forward=1
````
### Run the following to make the changes
````
sysctl -p
````
### List iptable settings
````
iptables -L
````
Ref: https://linuxconfig.org/how-to-turn-on-off-ip-forwarding-in-linux
----

# Configuring static IP
## CentOS:
* Modify the ''/etc/sysconfig/network-scripts/ifcfg-enp*'' file as
  * change ''BOOTPROTO'' to ''none''
  * add following two properties at the end of the file
    * IPADDR=10.10.0.10
    * PREFIX=24
NOTE: change IP address and prefix as per your system, keep other properties unchanged

EX: modifing properties in "ifcfg-enp2s0" interface file to set static IP on CentOS
````
nano /etc/sysconfig/network-scripts/ifconf-enp2s0

TYPE=Ethernet
BOOTPROTO=none
DEFROUTE=yes
PEERDNS=yes
PEERROUTES=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_PEERDNS=yes
IPV6_PEERROUTES=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=enp2s0
UUID=2d108ca5-e8c1-466b-b72a-a55b9731a9a0 
DEVICE=enp2s0
ONBOOT=yes
IPADDR=10.0.10.20
PREFIX=24
ZONE=public
GATEWAY=10.0.10.10
````
NOTE: change **UUID**, **DEVICE**, **NAME**, **IPADDR**, **PREFIX**, **GATEWAY** accourding to your requirements

## Debian:
On Debian and Ubuntu OS, the static IP for all interfaces are configured in "/etc/network/interfaces" file. To set static IP do as follow:
NOTE: Whereas in CentOS each interface has its own interface file.
````
nano /etc/network/interfaces

# The loopback network interface
auto lo
iface lo inet loopback

# Public IP setup
auto eth0
iface eth0 inet static
address x.x.x.x
netmask 255.255.254.0
gateway x.x.x.x
dns-nameservers 8.8.8.8 4.2.2.2

## Local IP setup
auto eth2
iface eth2 inet static
address 10.0.0.x
netmask 255.255.255.0
````

# How to set a virtual IP for one of the interface in Debian
````
...
# Modified on DT20180803, Humpty node upgrade, virtual port created for ganglia
# Local IP 10G interface
auto eth2 eth2:0
iface eth2 inet static
address 10.0.0.2
netmask 255.255.255.0

# Virtual host eth2:0
iface eth2:0 inet static
address 10.0.0.5
netmask 255.255.255.0
````
----

# Set network interface to get DHCP IP (newly installed system)
CentOS:
* modify ''ONBOOT'' parameter of ''/etc/sysconfig/network-scripts/ifcfg-enp*'' to ''yes''
* check for IP address ''ip addr show''
----

# 8.8.8.8 unreachable
ISSUE:
* In case if your facing ''connect network is unreachable'' issue or
* ''ping 8.8.8.8'' fail or unreachable issue
RESOLVE:
* add/check ''GATEWAY'' in network interface file
* OPTIONAL: check **/etc/resolve,conf** file, to add ''nameserver 8.8.8.8''
* check/add for ip_forward enable: https://devops.profitbricks.com/tutorials/deploy-outbound-nat-gateway-on-centos-7/

RESOLVE:
````
''echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.d/ip_forward.conf''
````
----

# Could not retrieve mirrorlist
ISSUE:
````
Could not retrieve mirrorlist...
    [root@archive ~]# yum update
    Loaded plugins: fastestmirror, langpacks
    Could not retrieve mirrorlist http://mirrorlist.centos.org/?release=7&arch=x86_64&repo=os&infra=stock error was 
    14: curl#6 - "Could not resolve host: mirrorlist.centos.org; Unknown error"
     One of the configured repositories failed (Unknown),
     and yum doesn't have enough cached data to continue. At this point the only
     safe thing yum can do is fail. There are a few ways to work "fix" this:
          1. Contact the upstream for the repository and get them to fix the problem.
          
          2. Reconfigure the baseurl/etc. for the repository, to point to a working
     ...
````

RESOLVE:
* check "/etc/resolve,conf" file and add ''nameserver 8.8.8.8''
----

# Fail to update (or) install any rpm package using yum =====
ISSUE(s) if any of teh following:
* [Errno 14] curl#6 - "Could not resolve host: centos.mirror.snu.edu.in; Unknown error"
* ''yum update'' or ''yum install ...'' fails with following type os error 
````
Could not retrieve mirrorlist http://... error was
14: curl#6 - "Could not resolve host: mirrorlist.centos.org; Unknown error"
````
RESOLVE:
* check ''/etc/resolve,conf'' file and **add appropriate nameserver** ''nameserver 8.8.8.8''
----

# Add Gateway
* Temporary: from the command line
````
route add default gw 10.0.10.10 eth0
````
* Permanent: add gateway IP at the end of the "/etc/sysconfig/network-script/ifcon-en"
````
GATEWAY=10.0.10.10
````
----
