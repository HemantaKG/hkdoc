## Copy beegfs repo file
```
wget -O /etc/yum.repos.d/beegfs_rhel7.repo https://www.beegfs.io/release/beegfs_7.2.7/dists/beegfs-rhel7.repo
OR
wget -O /etc/yum.repos.d/beegfs_rhel7.repo https://www.beegfs.io/release/beegfs_7.4.0/dists/beegfs-rhel9.repo
```

## Install beegfs client packages
```
yum install beegfs-client beegfs-helperd beegfs-utils libbeegfs-ib -y
```

## Update beegfs client conf file under "/etc/beegfs/beegfs-client.conf"
check and set "sysMgmtdHost = sonic-master" in "/etc/beegfs/beegfs-client.conf" file
```
vim /etc/beegfs/beegfs-client.conf
sysMgmtdHost = sonic-master

/opt/beegfs/sbin/beegfs-setup-client -m sonic-master
```

## Update "/etc/beegfs/beegfs-client-autobuild.conf" file and Build beegfs client
```
REF01 for Non GPU server configuration
REF02 for NVIDIA GPU server configuration

/etc/init.d/beegfs-client rebuild
```

## Start beegfs-client service
Check and set the "connDisableAuthentication = true" in "/etc/beegfs/beegfs-client.conf" and "/etc/beegfs/beegfs-helperd.conf" files
```
vim /etc/beegfs/beegfs-client.conf
connDisableAuthentication = true

vim /etc/beegfs/beegfs-helperd.conf
connDisableAuthentication = true

systemctl start beegfs-helperd
systemctl status beegfs-helperd
systemctl enable beegfs-helperd

systemctl start beegfs-client
systemctl status beegfs-client
systemctl enable beegfs-client

beegfs-df
```

## REF01: For non GPU server
## Update the as following in "/etc/beegfs/beegfs-client-autobuild.conf"
```
buildArgs=-j8 BEEGFS_OPENTK_IBVERBS=1 OFED_INCLUDE_PATH=/usr/src/ofa_kernel/default/include
```


## REF02: For NVIDIA GPU server
## Update the as following in "/etc/beegfs/beegfs-client-autobuild.conf
```
buildArgs=-j8 BEEGFS_OPENTK_IBVERBS=1 OFED_INCLUDE_PATH=/usr/src/ofa_kernel/default/include NVFS_INCLUDE_PATH=/usr/src/nvidia-fs-2.17.5 NVIDIA_INCLUDE_PATH=/usr/src/nvidia-535.104.05/nvidia
```

## Run the following If config-host.h is not present in NVFS_INCLUDE_PATH, execute the configure
```
cd /usr/src/nvidia-fs-2.17.5
./configure
```


