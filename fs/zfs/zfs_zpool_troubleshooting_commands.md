# ZFS pool management, zpool issue resolve commands
## Managing ZFS Storage Pool Properties
- set 'autoreplace= on' 
[References Link](http://docs.oracle.com/cd/E19253-01/819-5461/6n7ht6r00/index.html)

```bash
zpool get all jbod1
zpool set autoreplace=on jbod1
```

## ZFS Installation Related Issues on CentOS7
if above url FAILS with error '''zfs-release-1-4.el7_3.centos.n FAILED''' use try below url]
```bash
sudo yum install http://destek.serbestinternet.com/rhel7/rhel7/rhel7/zfs/zfs-release-1-4.el7_3.centos.noarch.rpm
yum install kernel-devel zfs
```

## Load "zfs modprobe" Issue on CentOS7
```bash
[root@storage ~]# zpool status
The ZFS modules are not loaded.

[root@storage ~]# zfs list
The ZFS modules are not loaded.
Try running '/sbin/modprobe zfs' as root to load them.

[root@storage ~]# /sbin/modprobe zfs
modprobe: FATAL: Module zfs not found.
Try running '/sbin/modprobe zfs' as root to load them.	-------[issue]
```

Do as follow to resolve the above issue

```bash
yum update
reboot
/sbin/modprobe zfs
```

Or, Try the following, if the above step not works

```bash
[root@storage ~]# ls /lib/modules	-----------------------[check kernel module version]
3.10.0-514.21.1.el7.x86_64  3.10.0-514.el7.x86_64

[root@storage ~]# dkms install spl/0.6.5.9	---------------[build 'spl' for required version]
Module spl/0.6.5.9 already installed on kernel 3.10.0-514.21.1.el7.x86_64/x86_64

[root@storage ~]# dkms install zfs/0.6.5.9	---------------[build 'zfs' for required version]
Module zfs/0.6.5.9 already installed on kernel 3.10.0-514.21.1.el7.x86_64/x86_64

[root@storage ~]# /sbin/modprobe zfs

[root@storage ~]# zfs list
no datasets available
```

## zpool not importing automatically after OS reboot
zfs service modules status check and enable:[Issue zpool auto import not working on centos 7.3 zfs version 0.6.9.1]

```bash 
[root@storage ~]# systemctl list-unit-files |grep zfs
    zfs-import-cache.service                      disabled
    zfs-import-scan.service                       disabled
    zfs-mount.service                             disabled
    zfs-share.service                             disabled
    zfs-zed.service                               disabled
    zfs.target                                    disabled
enable required services
```

```bash
[root@storage ~]# systemctl enable zfs.target
[root@storage ~]# systemctl enable zfs-zed.service
[root@storage ~]# systemctl enable zfs-share.service
[root@storage ~]# systemctl enable zfs-mount.service
[root@storage ~]# systemctl enable zfs-import-cache.service
[root@storage ~]# systemctl list-unit-files |grep zfs
    zfs-import-cache.service                      enabled 
    zfs-import-scan.service                       disabled
    zfs-mount.service                             enabled 
    zfs-share.service                             enabled 
    zfs-zed.service                               enabled 
    zfs.target                                    enabled
```

## Some Useful zfs commands
- [more detail on the space consumed by the snapshots](https://blogs.oracle.com/solaris/understanding-the-space-used-by-zfs-v2):
```bash
zfs list -t all -o space -r datapool
```
- [Checking ZFS File System Integrity](https://docs.oracle.com/cd/E18752_01/html/819-5461/gbbwa.html)
```bash
zpool scrub tank
```
- [Creating and Destroying ZFS Snapshots](https://docs.oracle.com/cd/E19253-01/819-5461/gbcya/index.html)
- [ZFS Features and Terminology](http://www.allanjude.com/bsd/zfs-term.html#zfs-term-compression)
- [zfs Administration](http://www.allanjude.com/bsd/zfs-zfs.html)
- [Understanding and Resolving ZFS Disk Failure](https://docs.joyent.com/private-cloud/troubleshooting/disk-replacement)
- [Improve zfs performance](https://icesquare.com/wordpress/how-to-improve-zfs-performance)
