# Create zfs dataset and mount
```bash
mkdir -p /data
zfs create jbod1/data
zfs set mountpoint=/data jbod1/data
```
OR
```bash
mkdir -p /data
zfs create -o mountpoint=/data jbod1/data
```

Ref:
* [zfs dataset create, rename, destroy](https://docs.oracle.com/cd/E19253-01/819-5461/6n7ht6r2n/index.html)
* [manage zfs dataset](https://docs.oracle.com/cd/E19253-01/819-5461/gaztn/index.html)
* [zfs dataset mount, unmount](https://docs.oracle.com/cd/E19253-01/819-5461/gamnr/index.html)

# Userspace Qouta set
set userspace quota
```bash
zfs set userquota@guest5=3T mariodatapool/home
```

# List all zfs userspace quota
```bash
zfs userspace mariodatapool/home
```

# Referance:
[zfs userspace quota](https://docs.oracle.com/cd/E19253-01/819-5461/gitfx/index.html)
