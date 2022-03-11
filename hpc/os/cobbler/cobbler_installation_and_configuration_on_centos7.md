==== Cobbler installation and configuration ====
System details:
- controller/server/master node
   - hostname: mgn/mgn.test.cluster
   - ip: 10.0.10.10
- compute nodes
   - hostname n1, n2
   - ip: 10.0.10.1, 10.0.10.2
- Install a VM and setup a static IP
- Add hosts to **/etc/hosts** file
- Disable **selinux**

## Install Cobbler
````
yum install cobbler
````

## Configure Cobbler setting as per your requirments
Edit **/etc/cobbler/setting** file to set **cobbler root passwd**, **server IP**, **next_server IP**, **manage_dhcp**
- change default passwd with new crypted password, **NOTE:** get crypted password by running ''**openssl passwd -1 -salt 'random-phrase-here' 'your-password-here'**''
- change **server** and **next_server** IP same as your system static IP
- change ''**mange_dhpc: 1**'' to manage dhcp by cobbler
````
nano /etc/cobbler/setting
default_password_crupted: <<crypted passwd>>
server: 10.0.2.2
next_server: 10.0.2.2
manage_dhcp: 1
````

## Configure Cobbler dhcp template file
- Edit **/etc/cobbler/dhcp.template** file to set required dhcp configuration.
- The above file generates a **/etc/dhcp/dhcpd.conf** file to run dhcp server on server
- **NOTE:** change only below properties as per your required IP ranges
````
nano /etc/cobbler/dhcp.template

subnet 10.0.10.0 netmask 255.255.255.0 {
    option routers                10.0.10.10;
    option domain-name-servers    8.8.8.8;
    option subnet-mask            255.255.255.0;
    range dynamic-booyp           10.0.10.2 10.0.10.5;
    default-lease-time            21600;
    max-lease-time                43200;
    next-server                   $next_server;
````

## Cobbler service start
start ''**httpd**'' and ''**cobbler**'' services
````
systemctl start cobblerd.service
systemctl enable cobblerd.service
systemctl status cobblerd.service

systemctl start httpd
systemctl enable httpd
systemctl status httpd
````

## Check Cobbler configuration and generate dhcp.conf file
first run ''cobbler check'', it checks all cobbler configurations setting and point outs issues if there. Then run ''cobbler sync'', it generates the ''/etc/dhcp/dhcpd.conf'' file.
````
cobbler check
cobbler sync
````

## Mount OS iso file
mount the iso file to somewhere; here ''/mnt''
````
mount -t iso9660 -o loop,ro /root/iso_files/CentOS-7-x86_64-Minimal-1611.iso /mnt/
````

## Import the distribution
Import the distribution into cobbler object list, the ''name'' and ''path'' arguments are the only required options for import. Here, distribution imported as name **c7**
````
cobbler import --name=c7 --path=/mnt
````

## Cobbler OS object
NOTE: run **cobbler sync** after every changes/update of any Cobbler objects (such as profile/system add or remove operations)
- List all cobbler objects
````
cobbler distro list
````
List all cobbler profiles
````
cobbler profile list
````
Remove profile **p4** form Cobbler profile list
````
cobbler profile remove --name=p4
````
Get report of **c7-x86_64** distro 
````
cobbler distro report --name=c7-x86_64
````

## Add kickstart file to Cobbler OS profile
- Keep **kickstart file** under **/var/lib/cobbler/kickstarts/**
- Update Cobbler OS profile
````
# NOTE: profile create with kickstart file
cobbler profile add --name=centos7-x86_64 --kickstart=/var/lib/cobbler/kickstarts/sample.ks

# NOTE: profile create with name, specific distro, repos, kickstart file
cobbler profile add --name=p4 --distro=c7-x86_64 --repos=centos7 --kickstart=/var/lib/cobbler/kickstarts/c7_p4_s1_1.ks
   
**NOTE:** here, "p4"* is the profile name "c7-x86_64" is distro name "centos7" is user created repo name
````
Check that the above kickstart file was added properly or not to the profile
````
cobbler profile getks --name=p4|less
````

## Create/Edit system to install and list systems
- Profiles can be used to PXE boot, but most of the features in cobbler revolve around system objects
- The more information you give about a system, the more cobbler will do automatically for you
- Create a system object based on the profile that was created during the import, When creating a system, the name and profile are the only two required fields
create cobbler system object: system name **c7_sys** using profile **c7-x86_64** 

````
cobbler system add --name=c7_sys --profile=c7-x86_64
````
List all cobbler systems objects
````
cobbler system list
````
Show the cobbler system **c7_sys** report
````
cobbler system report --name=c7_sys
````
Edit cobbler system **c7_sys** to add interface, MAC ID, IP address, netmask and etc
````
cobbler system edit --name=c7_sys --interface=eth0 --mac=D4:3D:7E:23:70:FB --ip-address=10.0.10.2 --netmask=255.255.255.0 --static=1
cobbler system edit --name=centos_sys --gateway=10.0.10.10 --hostname=n1.sys
````
NOTE: run ''cobbler sync'' after creating a system to commit the changes    
````
cobbler sync
````

## Start/Restart tftp service
````
systemctl restart tftp.service
````

## Add tcp/udp ports to iptable
Add port **80** and **69** to iptables (OR) try with firewall service off
````
iptables -I INPUT -p tcp -s 10.0.10.0/24 -d 10.0.10.10. --dport 80 -j ACCEPT
iptables -I INPUT -p udp -s 10.0.10.0/24 -d 10.0.10.10. --dport 69 -j ACCEPT
````
NOTE: restart ''cobbler.service'' and ''httpd.service''

## Cobbler web-interface configuration
Install following additional packages
````
yum install cobbler cobbler-web dnsmasq syslinux pykickstart xinetd
````
Create Cobbler user account to access web-interface username ''cobbler''
````
htdigest /etc/cobbler/users.digest "Cobbler" cobbler
````
NOTE: access cobbler web: ''https://localhost/cobbler_web''

## Cobbler Repo add and Reposync
Ref:[[http://cobbler.github.io/manuals/2.4.0/4/1/5_-_Repos.html|Repos]], [[http://cobbler.github.io/manuals/2.4.0/4/2/5_-_Reposync.html|Reposync]],[[https://github.com/cobbler/cobbler/wiki/Manage-yum-repos|Manage yum repos]]
<code>
cobbler repo add --mirror=http://mirror.centos.org/centos/7/os/x86_64/ --name=centos7
cobbler reposync
</code>
==== Adding Additional repos urls ====
  * We can add additional ''repos'' in kickstart file for installation of extra packages which are not available in ''iso''. We can add many ''repos'' as
<code>
repo --name=source-2 --baseurl=http://10.0.10.10/cobbler/repo_mirror/centos7
repo --name=source-3 --baseurl=http://ftp.riken.jp/Linux/fedora/epel/7/x86_64/
repo --name=source-4 --baseurl=http://ftp.iitm.ac.in/centos/
</code>
==== Reference ====
  * [[https://cobbler.github.io/quickstart/|Cobbler quickstart]]
  * [[https://cobbler.readthedocs.io/en/latest/|Cobbler Documentation]]
  * [[http://cobbler.github.io/manuals/2.6.0/5_-_Web_Interface.html|Cobbler web-interface]]
==== Some Handy Commands ====
  * Get ''kickstart'' file linked with ''system''
<code>
cobbler system getks --name=foo | less
</code>
  * List repo
<code>
yum repolist
</code>
  * List all yum ''groups'' of repo
<code>
yum group list
</code>
==== Troubleshooting ====
  * If ''PIX Boot'' not staring, then check following:
    * ''Add tcp/udp ports to iptable''
    * restart ''tftp.service''
  * [[https://www.centos.org/forums/viewtopic.php?t=57419|''dracut'' cant locate ''/dev/root'']]
**ERROR:**
<code>
...
[  205.095282] dracut-initqueue[669]: Warning: /dev/root does not exist
 Starting Dracut Emergency Shell...
Warning: /dev/root does not exist

Generating "/run/initramfs/rdsosreport.txt"
...
</code>
**RESOLVE:**
<code> 
cobbler distro edit --name=centos7-x86_64 --kopts="inst.repo=http://10.0.10.10/cobbler/ks_mirror/centos7"
</code>
