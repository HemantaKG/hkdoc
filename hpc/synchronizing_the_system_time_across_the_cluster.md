# Install NTP service on compute cluster
[Ref:](|https://knowm.org/how-to-synchronize-time-across-a-linux-cluster/)

## Intall NTP service on all nodes
````
yum install ntp
````

## Restart service
````
systemctl restart ntpd.service
````

# NTP clients service on all compute nodes
On all the remaining nodes in your cluster, set them up to sync clocks with the node which was designated as the main time server in the cluster
````
nano /etc/ntp.conf

# add ntp server ip
server 10.10.0.2
````

## Restart service
````
systemctl restart ntpd.service
````

## Check Connectivity to main time server
````
ntpq -c lpeer
````
