==== Create zfs dataset and mount ====
<code>
mkdir -p /data
zfs create jbod1/data
zfs set mountpoint=/data jbod1/data

OR

mkdir -p /data
zfs create -o mountpoint=/data jbod1/data
</code>
Ref:
  * [[https://docs.oracle.com/cd/E19253-01/819-5461/6n7ht6r2n/index.html|zfs dataset create, rename, destroy]]
  * [[https://docs.oracle.com/cd/E19253-01/819-5461/gaztn/index.html|manage zfs dataset]]
  * [[https://docs.oracle.com/cd/E19253-01/819-5461/gamnr/index.html|zfs dataset mount, unmount]]
==== Userspace Qouta set ====
set userspace quota
<code>
zfs set userquota@guest5=3T mariodatapool/home
</code>
List all zfs userspace quota
<code>
zfs userspace mariodatapool/home
</code>
Ref: [[https://docs.oracle.com/cd/E19253-01/819-5461/gitfx/index.html| zfs userspace quota]]
