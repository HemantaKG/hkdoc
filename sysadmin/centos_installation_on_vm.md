# List of services to install ans check afeter CentOS minimal installation on VM
## Check network interface:
````
ip addr show
````
## Change interface file to get internet access:
````
vi /etc/sysconfig/network-scripts/ifcfg-enp0s3

change "ONBOOT= yes"
````
## Restart netwok service:
````
service network restart
````
## Install extra epel repo list:
````
yum -y install epel-release
````
## Install some useful network tools:
(it installes ifconfig command)
````
yum -y install net-tools
````
## Install GUI Desktop "GNOME":
````
yum -y groups install "GNOME Desktop"
````
## Start GUI Desktop:
````
startx
````
