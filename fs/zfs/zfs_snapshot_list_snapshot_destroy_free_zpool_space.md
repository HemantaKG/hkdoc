# List all zfs snapshots
The following command list all zfs snapshot
```bash
zfs list -t snapshot -S used
```

# Destroy zfs snapshot
For example you want to destroy the following zfs snapshot **zfs destroy zsp1/home@2019-03-30-000000**
```bash
zfs destroy mariodatapool/home@2018-03-13-000000
```
