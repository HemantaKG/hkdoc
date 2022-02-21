# Ganglia instalation on master node
(Ref|https://linuxcluster.wordpress.com/2010/01/01/installing-and-configuring-ganglia-on-centos-5-4/)
NOTE: 
Mater node IP: 10.10.0.2

'''
yum install ganglia rrdtool ganglia-gmetad ganglia-gmond ganglia-web
'''

# Configuration on master node
Edit "gmetad.conf"
Add datasource name and gridname
'''
nano /etc/ganglia/gmetad.conf

>data_source "mario_cluster" 10.10.0.2:8649
>gridname "mario_cluster"
'''

# Edit "gmond.conf"
Modify as follow;
'''
nano /etc/ganglia/gmond.conf

cluster {
  name = "mario_cluster"
  owner = "unspecified"
  latlong = "unspecified"
  url = "unspecified"
}

host {
  location = "<<change FQHN>>"
}

udp_send_channel {
  host = 10.10.0.2
  port = 8649
  ttl = 1
}

/* You can specify as many udp_recv_channels as you like as well. */
udp_recv_channel {
  port = 8649
  retry_bind = true
}
'''

# Edit "ganglia.conf" file
Modify **ganglia.conf** file under **/etc/httpd/conf.d** to access Ganglia web-page as follow;
add following lines of statement in <Location /ganglia> tab

'''
nano /etc/httpd/conf.d/ganglia.conf

AllowOverride None
Require all granted
'''

# Start ganglia services on master node
'''
systemctl start httpd gmetad gmond
systemctl enable httpd gmetad gmond
systemctl status httpd gmetad gmond
'''

# Ganglia instalation on compute nodes
## installation on node
'''
yum install ganglia-gmond
'''

# Configuration on node
- Copy **/etc/ganglia/gmond.conf** configuration file from master to all compute nodes and keep under **/etc/ganglia/** directory. Than start Ganglia service on compute nodes

'''
# start ganglia service
systemctl start gmond
systemctl enable gmond
systemctl status gmond
'''

# Troubleshooting
- ISSUE: RRD data illegal attempt to update found **/var/log/messages** file. RESOLVE
Note: Time syncronization accross all nodes of the cluster

    Feb 21 16:34:14 master gmetad: RRD_update (/var/lib/ganglia/rrds/mario_cluster/__SummaryInfo__/proc_run.rrd): /var/lib/ganglia/rrds/mario_cluster/__SummaryInfo__/proc_run.rrd: illegal attempt to update using time 1519211054 when last update time is 1519211054 (minimum one second step)

- ISSUE: There was an error collecting ganglia data (127.0.0.1:8652): fsockopen error: Connection refused; RESOLVE disable **selinux**
