# zfs backup using znapzend

## Prerequisites tool(s) and packages(s)
Install following prerequisites tool(s) and packages(s).
NOTE: install "mbuffer" package on both server(S)

```bash
yum group install "Development Tools"
yum install perl-core
yum install mbuffer
```

NOTE: password less login is required to take backup using for znapzend service. [share the ssh key]()

## znapzend package installation:
follow these instructions below to install **znapzend**.
step1: Download the latest package: [znapzend tar file](https://github.com/oetiker/znapzend/releases)
```bash
wget https://github.com/oetiker/znapzend/releases/download/v0.17.0/znapzend-0.17.0.tar.gz
```
step2: Configure, make and install
```bash
tar zxvf znapzend-0.17.0.tar.gz
cd znapzend-0.17.0
./configure --prefix=/opt/znapzend-0.17.0
make
make install
```
step3: Add executable to **/usr/local/bin**
```bash
for x in /opt/znapzend-0.17.0/bin/*; do ln -s $x /usr/local/bin; done
```

## Plan the data backup
NOTE: password less login is required to take backup using for znapzend service. Use **ssh-copy-id username@archive_server_hostname** to copy ssh-key.
### Design your backup plan:
```bash
/usr/local/bin/znapzendzetup create --recursive --mbuffer=/bin/mbuffer --mbuffersize=1G --tsformat='%Y-%m-%d-%H%M%S' --pre-snap-command=off --post-snap-command=off SRC '7d=>1d,30d=>1w,1y=>1m' mariodatapool/home DST:a '7d=>1d,30d=>1w,90d=>30d,1y=>3m,5y=>1y' root@10.10.0.4:datapool/backup_mario
```
> *** backup plan: mariodatapool/home ***
> *dst_a           = root@10.10.0.4:datapool/backup_mario
> *dst_a_plan      = 7days=>1day,30days=>1week,90days=>30days,1year=>3months,5years=>1year
> *enabled         = on
> *mbuffer         = /bin/mbuffer
> *mbuffer_size    = 1G
> *post_znap_cmd   = off
> *pre_znap_cmd    = off
> *recursive       = on
> *src             = mariodatapool/home
> *src_plan        = 7days=>1day,30days=>1week,1year=>1month
> *tsformat        = %Y-%m-%d-%H%M%S
> *zend_delay      = 0
> 
> Do you want to save this backup set [y/N]? y
> NOTE: if you have modified your configuration, send a HUP signal
> (pkill -HUP znapzend) to your znapzend daemon for it to notice the change.

### Dry running to check the backup service working:
The **znapzend** daemon is responsible for doing the actual backups.
To see if your configuration is any good, run **znapzend** in **noaction mode** first
```bash
/usr/local/bin/znapzend --noaction --debug
```

you can also quick check by force immediate action by calling
```bash
/usr/local/bin/znapzend --noaction --debug --runonce=mariodatapool/home
```
> [Fri Mar  2 13:46:43 2018] [info] znapzend (PID=105590) starting up ...
> [Fri Mar  2 13:46:43 2018] [info] refreshing backup plans...
> [Fri Mar  2 13:46:44 2018] [info] found a valid backup plan for mariodatapool/home...
> [Fri Mar  2 13:46:44 2018] [info] znapzend (PID=105590) initialized -- resuming normal operations.
> [Fri Mar  2 13:46:44 2018] [debug] snapshot worker for mariodatapool/home spawned (105606)
> [Fri Mar  2 13:46:44 2018] [info] creating recursive snapshot on mariodatapool/home
> # zfs snapshot -r mariodatapool/home@2018-03-02-134644
> [Fri Mar  2 13:46:44 2018] [debug] snapshot worker for mariodatapool/home done (105606)
> [Fri Mar  2 13:46:44 2018] [debug] send/receive worker for mariodatapool/home spawned (105607)
> [Fri Mar  2 13:46:44 2018] [info] starting work on backupSet mariodatapool/home
> # zfs list -H -r -o name -t filesystem,volume mariodatapool/home
> [Fri Mar  2 13:46:44 2018] [debug] sending snapshots from mariodatapool/home to root@10.10.0.4:datapool/backup_mario
> # zfs list -H -o name -t snapshot -s creation -d 1 mariodatapool/home
> # ssh -o batchMode=yes -o ConnectTimeout=30 root@10.10.0.4 zfs list -H -o name -t snapshot -s creation -d 1 datapool/backup_mario
> # ssh -o batchMode=yes -o ConnectTimeout=30 root@10.10.0.4 zfs list -H -o name -t snapshot -s creation -d 1 datapool/backup_mario
> [Fri Mar  2 13:46:44 2018] [debug] cleaning up snapshots on root@10.10.0.4:datapool/backup_mario
> # zfs list -H -o name -t snapshot -s creation -d 1 mariodatapool/home
> [Fri Mar  2 13:46:44 2018] [debug] cleaning up snapshots on mariodatapool/home
> [Fri Mar  2 13:46:44 2018] [info] done with backupset mariodatapool/home in 0 seconds
> [Fri Mar  2 13:46:44 2018] [debug] send/receive worker for mariodatapool/home done (105607)
then when you are happy with what you got, start it in daemon mode

### start znapzend service
```bash 
/usr/local/bin/znapzend --daemonize
```
> znapzend (7622) is running in the background now.

## View and Modification of Backup plane
[Ref:](https://github.com/oetiker/znapzend/blob/master/doc/znapzendzetup.pod)

### To view the current running znapzend zfs backup plan
```bash
znapzendzetup list
```

### To modify the source side backup plan
```bash
/usr/local/bin/znapzendzetup edit SRC '7days=>1day,30days=>1week,1year=>1month' mariodatapool/home
```

## Edit Backup plane
To the backup plane:
```bash
znapzendzetup edit SRC '7days=>1day,30days=>1week,6month=>30days' tetrisdatapool/home_data DST:a '7days=>1day,30days=>1week,1year=>30days' root@10.10.48.5:tetrisarchivedatapool/backup_tetris
```

### Following command to apply the modified backup plane
```bash
pkill -HUP /usr/local/bin/znapzend
```

## Backup statistics
To show the backup details of both source and destination servers
```bash
znapzendztatz 
```

[Referance](https://github.com/oetiker/znapzend)
