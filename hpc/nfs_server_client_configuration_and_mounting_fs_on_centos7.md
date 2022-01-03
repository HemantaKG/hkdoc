==== System details =====
  * server/master node
    * hostname: mgn, mgn.test.cluster
    * ip: 10.0.10.10
  * child node
    * hostname: n1, n1.test.cluster
    * ip: 10.0.10.2
==== NFS server configuration =====
=== NFS server installation ====
<code>
yum -y install nfs-utils
</code>
=== edit "/etc/idmapd.conf" file ===
uncomment and change ''Domain'' to your domain name ''test.cluster'' at line 5
<code>
nano /etc/idmapd.conf

Domain = test.cluster
</code>
=== edit "/etc/exports" file ===
write the NFS export fs details
<code>
nano /etc/exports

# NFS exports
/home   10.0.10.0/24(rw,sync,no_root_squash,no_subtree_check)
</code>
=== restart services ===
<code>
systemctl start rpcbind nfs-server
systemctl enable rpcbind nfs-server
</code>
=== allow NFS service at firewall ===
**<color #ff7f27>NOTE</color>**: Do in case firewalld service is running
<code>
firewall-cmd --add-service=nfs --permanent 
firewall-cmd --reload
</code>
==== NFS client configuration ====
=== install NFS ===
<code>
yum -y install nfs-utils
</code>
=== edit "/etc/idmapd.conf" file ===
uncomment and change ''Domain'' to your domain name ''test.cluster''
<code>
nano /etc/idmapd.conf

Domain test.cluster
</code>
=== start "rpcbind' service ===
<code>
systemctl start rpcbind
systemctl enable rpcbind
</code>
=== NFS mounting ===
<code>
mount -t nfs mgn@test.cluster:/home /home
</code>
NOTE: **Configure NFS mounting on ''/etc/fstab'' file to mount it when the system boots**
<code>
nano /etc/fstab

mgn.test.cluster:/home    /home    nfs     defults    0    0
</code>