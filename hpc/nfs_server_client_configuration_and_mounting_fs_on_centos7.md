# NFS server configuration
System details
* server/master node
  * hostname: mgn, mgn.test.cluster
  * ip: 10.0.10.10
* child node
  * hostname: n1, n1.test.cluster
  * ip: 10.0.10.2

## NFS server installation
````
yum -y install nfs-utils
````

modify "/etc/idmapd.conf" file
uncomment and change ''Domain'' to your domain name ''test.cluster'' at line 5
````
nano /etc/idmapd.conf
    Domain = test.cluster
````

modify "/etc/exports" file
write the NFS export fs details
````
nano /etc/exports

# NFS exports
/home   10.0.10.0/24(rw,sync,no_root_squash,no_subtree_check)
````

## Restart services
````
systemctl start rpcbind nfs-server
systemctl enable rpcbind nfs-server
````

## allow NFS service at firewall
NOTE: Do in case firewalld service is running
````
firewall-cmd --add-service=nfs --permanent 
firewall-cmd --reload
````

## NFS client configuration
Install NFS
````
yum -y install nfs-utils
````

modify "/etc/idmapd.conf" file
uncomment and change ''Domain'' to your domain name ''test.cluster''
````
nano /etc/idmapd.conf
    Domain test.cluster
````

## Start "rpcbind' service
````
systemctl start rpcbind
systemctl enable rpcbind
````

## NFS mounting
````
mount -t nfs mgn@test.cluster:/home /home
````
NOTE: **Configure NFS mounting on ''/etc/fstab'' file to mount it when the system boots**

````
nano /etc/fstab

mgn.test.cluster:/home    /home    nfs     defults    0    0
````
