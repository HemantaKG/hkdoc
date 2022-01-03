===== ZFS pool management, resolved issues and useful zfs commands =====
==== Managing ZFS Storage Pool Properties ====
  * set 'autoreplace= on' [[http://docs.oracle.com/cd/E19253-01/819-5461/6n7ht6r00/index.html|References Link]]
<code>
zpool get all jbod1
zpool set autoreplace=on jbod1
</code>
==== ZFS Installation Related Issues on CentOS7 ====
[if above url FAILS with error '''zfs-release-1-4.el7_3.centos.n FAILED''' use try below url]
    sudo yum install http://destek.serbestinternet.com/rhel7/rhel7/rhel7/zfs/zfs-release-1-4.el7_3.centos.noarch.rpm
    yum install kernel-devel zfs
==== Load "zfs modprobe" Issue on CentOS7 ====
    [root@jbodstorage ~]# zpool status
    The ZFS modules are not loaded.
    [root@jbodstorage ~]# zfs list
    The ZFS modules are not loaded.
    Try running '/sbin/modprobe zfs' as root to load them.
    [root@jbodstorage ~]# /sbin/modprobe zfs
    modprobe: FATAL: Module zfs not found.
    Try running '/sbin/modprobe zfs' as root to load them.	-------[issue]
Do as follow to resolve the above issue
    yum update
    reboot
    /sbin/modprobe zfs
OR, try if above not works
    [root@jbodstorage ~]# ls /lib/modules	-----------------------[check kernel module version]
    3.10.0-514.21.1.el7.x86_64  3.10.0-514.el7.x86_64
    [root@jbodstorage ~]# dkms install spl/0.6.5.9	---------------[build 'spl' for required version]
    Module spl/0.6.5.9 already installed on kernel 3.10.0-514.21.1.el7.x86_64/x86_64
    [root@jbodstorage ~]# dkms install zfs/0.6.5.9	---------------[build 'zfs' for required version]
    Module zfs/0.6.5.9 already installed on kernel 3.10.0-514.21.1.el7.x86_64/x86_64
    [root@jbodstorage ~]# /sbin/modprobe zfs
    [root@jbodstorage ~]# zfs list
    no datasets available
==== zpool not importing automatically after OS reboot ==== 
zfs service modules status check and enable:[Issue zpool auto import not working on centos 7.3 zfs version 0.6.9.1]
    [root@jbodstorage ~]# systemctl list-unit-files |grep zfs
    zfs-import-cache.service                      disabled
    zfs-import-scan.service                       disabled
    zfs-mount.service                             disabled
    zfs-share.service                             disabled
    zfs-zed.service                               disabled
    zfs.target                                    disabled
enable required services
    [root@jbodstorage ~]# systemctl enable zfs.target
    [root@jbodstorage ~]# systemctl enable zfs-zed.service
    [root@jbodstorage ~]# systemctl enable zfs-share.service
    [root@jbodstorage ~]# systemctl enable zfs-mount.service
    [root@jbodstorage ~]# systemctl enable zfs-import-cache.service
    [root@jbodstorage ~]# systemctl list-unit-files |grep zfs
    zfs-import-cache.service                      enabled 
    zfs-import-scan.service                       disabled
    zfs-mount.service                             enabled 
    zfs-share.service                             enabled 
    zfs-zed.service                               enabled 
    zfs.target                                    enabled
==== Some Useful zfs commands ====
  * [[https://blogs.oracle.com/solaris/understanding-the-space-used-by-zfs-v2|more detail on the space consumed by the snapshots]]: ''zfs list -t all -o space -r datapool''
  * [[https://docs.oracle.com/cd/E18752_01/html/819-5461/gbbwa.html|Checking ZFS File System Integrity]]: ''zpool scrub tank''
  * [[https://docs.oracle.com/cd/E19253-01/819-5461/gbcya/index.html|Creating and Destroying ZFS Snapshots]]
  * [[http://www.allanjude.com/bsd/zfs-term.html#zfs-term-compression|ZFS Features and Terminology]]
  * [[http://www.allanjude.com/bsd/zfs-zfs.html|zfs Administration]]
  * [[https://docs.joyent.com/private-cloud/troubleshooting/disk-replacement|Understanding and Resolving ZFS Disk Failure]]
  * [[https://icesquare.com/wordpress/how-to-improve-zfs-performance/| Improve zfs performance]]