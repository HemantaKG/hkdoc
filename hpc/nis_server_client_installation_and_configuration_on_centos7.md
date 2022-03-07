# NIS Server Configuration
System details
* server/master node
  * hostname: mgn, mgn.test.cluster
  * ip: 10.0.10.10
* child node
  * hostname: n1, n1.test.cluster
  * ip: 10.0.10.2

## Installation
````
yum -y install ypserv rpcbind
````

## Configuration
modify "/etc/hosts" file
````
nano /etc/hosts
    # add IP addresses for NIS server and clients
    10.0.10.10    mgn.test.cluster    mgn
    10.0.10.2     n1.test.cluster     n1
````

## set domain name for NIS
set NIS domain name
````
ypdomainname test.cluster
   
echo "NISDOMAIN=test.cluster" >> /etc/sysconfig/network
````

modify "/var/yp/securenets"
````
nano /var/yp/securenets
    # add IP addresses you allow to access to NIS server
    255.0.0.0       127.0.0.0
    255.255.255.0   10.0.10.0
````

## start services
````
systemctl start rpcbind ypserv ypxfrd yppasswdd
systemctl enable rpcbind ypserv ypxfrd yppasswdd
````

## Create/update NIS DB
````
# update NIS database
    /usr/lib64/yp/ypinit -m 
````

Update NIS DB
If you added users in local NIS server, apply them to NIS database, too.
````
cd /var/yp
make
````

## Allow ports: Firewall
NOTE: by default all ports are in block stat in CentOS, We need set those to allow
````
nano /etc/sysconfig/network
    # add to the end
    YPSERV_ARGS="-p 944"
    YPXFRD_ARGS="-p 945"
````
````
nano /etc/sysconfig/yppasswdd
    # add like follows
    YPPASSWDD_ARGS="--port 946"
````

## Service and firewall add/restart
Allow NIS services or ports
````
systemctl restart rpcbind ypserv ypxfrd yppasswdd
firewall-cmd --add-service=rpc-bind --permanent

firewall-cmd --add-port=944/tcp --permanent
firewall-cmd --add-port=944/udp --permanent
firewall-cmd --add-port=945/tcp --permanent
firewall-cmd --add-port=945/udp --permanent
firewall-cmd --add-port=946/udp --permanent
firewall-cmd --reload
````

# NIS Client Configuration
## Installation
````
yum install ypbind rpcbind
````

## Configuration
modify "/etc/hosts"
````
nano /etc/hosts
    # add IP addresses for NIS server and clients
    10.0.10.10    mgn.test.cluster    mgn
    10.0.10.2     n1.test.cluster     n1
````

## domain name set, autoconfig NIS client and restart services
````
ypdomainname test.cluster

echo "NISDOMAIN=test.cluster" >> /etc/sysconfig/network 

authconfig --enablenis --nisdomain=test.cluster --nisserver=mgn.test.cluster --enablemkhomedir --update

systemctl start rpcbind ypbind
systemctl enable rpcbind ypbind
````
