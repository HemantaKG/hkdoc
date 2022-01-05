# ZFS snapshot plan edit
```bash
/usr/local/bin/znapzendzetup edit SRC '7days=>1day,30days=>1week,2month=>30days' mariodatapool/home DST:a '7days=>1day,30days=>1week,6months=>30days' root@10.10.0.4:datapool/backup_mario

pkill -HUP znapzend
```
