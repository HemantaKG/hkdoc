  * [[network#Packate forwarding (Netting)|Packate forwarding (Netting)]]
  * [[network#Configuring static IP|Configuring static IP]]
  * [[network#Set network interface to get DHCP IP (newly installed system)|Set network interface to get DHCP IP (newly installed system)]]
  * [[network#Could not retrieve mirrorlist|Could not retrieve mirrorlist]]
  * [[network#Fail to update (or) install any rpm package using yum|Fail to update (or) install any rpm package using yum]]
  * [[network#Adding Gateway|Adding Gateway]]
===== Packate forwarding (Netting) =====
  * First flash all ''iptable'' settings before ''netting''
<code>
iptables -F
</code>
  * Now run below commands for ''netting''
NOTE: Public interface ''enp0s29u1u6'' and Local interface ''enp3s0''
<code>
iptables -t nat -A POSTROUTING -o enp0s29u1u6 -j MASQUERADE
iptables -A FORWARD -i enp3s0 -j ACCEPT
</code>
NOTE:
  * //**''/etc/resolve.conf'' and ''GATEWAY'' was definded but still node not getting internet and ''ping 8.8.8.8'' not pinging, than do ''iptable'' flash and rerun the ''netting''**//
  * on **CentOS** system please check **''/etc/sysctl.conf''** file:
<code>
nano /etc/sysctl.conf
net.ipv4.ip_forward=1
</code>
  * List iptable settings
<code>
iptables -L
</code>
----
===== Configuring static IP =====
==== On CentOS: ====
  * Modify the ''/etc/sysconfig/network-scripts/ifcfg-enp*'' file as
    * change ''BOOTPROTO'' to ''none''
    * add following two properties at the end of the file
      * ''IPADDR=10.10.0.10''
      * ''PREFIX=24''
NOTE: change IP address and prefix as per your system, keep other properties unchanged

**EX:** modifing properties in **ifcfg-enp2s0** interface file to set static IP on CentOS
<code>
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
</code>
NOTE: change **UUID**, **DEVICE**, **NAME**, **IPADDR**, **PREFIX**, **GATEWAY** accourding to your requirements
==== On Debian: ====
On Debian and Ubuntu OS, the static IP for all interfaces are configured in "//**/etc/network/interfaces**//" file. To set static IP do as follow:

NOTE: Whereas in CentOS each interface has its own interface file. 
<code>
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
</code>
To set virtual IP on one of the interface:
<code>
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
</code>
----
===== Set network interface to get DHCP IP (newly installed system) =====
==== On CentOS: ====
  * modify ''ONBOOT'' parameter of ''/etc/sysconfig/network-scripts/ifcfg-enp*'' to ''yes''
  * check for IP address ''ip addr show''

----
===== 8.8.8.8 unreachable =====
<color #ed1c24>ISSUE</color>:
  * In case if your facing ''connect network is unreachable'' issue or
  * ''ping 8.8.8.8'' fail or unreachable issue
<color #22b14c>RESOLVE</color>:
  * **add/check ''GATEWAY'' in network interface file**
  * [OPTIONAL] check **/etc/resolve,conf** file, to add ''nameserver 8.8.8.8''
  * [[https://devops.profitbricks.com/tutorials/deploy-outbound-nat-gateway-on-centos-7/|check/add for ip_forward enable]] ''echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.d/ip_forward.conf''

----
===== Could not retrieve mirrorlist =====
<color #ed1c24>ISSUE</color>:
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
<color #22b14c>RESOLVE</color>:
check **/etc/resolve,conf** file and add ''nameserver 8.8.8.8''
===== Fail to update (or) install any rpm package using yum =====
<color #ed1c24>ISSUE(s)</color> any one:
  * [Errno 14] curl#6 - "Could not resolve host: centos.mirror.snu.edu.in; Unknown error"
  * ''yum update'' or ''yum install ...'' fails with following type os error <code>Could not retrieve mirrorlist http://... error was
14: curl#6 - "Could not resolve host: mirrorlist.centos.org; Unknown error"</code>
<color #22b14c>RESOLVE</color>: check ''/etc/resolve,conf'' file and **add appropriate nameserver** ''nameserver 8.8.8.8''

----
===== Adding Gateway =====
  * Temporary: from the command line
<code>route add default gw 10.0.10.10 eth0</code>
  * Permanent: add gateway IP at the end of the **/etc/sysconfig/network-script/ifcon-en* ** file.
    * //GATEWAY=10.0.10.10''//

----