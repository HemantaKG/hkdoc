==== Prerequisites tool(s) and packages(s) ====
install following prerequisites tool(s) and packages(s). NOTE: install "mbuffer" package on both server(S)
<code>
yum group install "Development Tools"
yum install perl-core
yum install mbuffer
</code>
password less login to backup serve is required, share the ssh key with backup server.[[[[ssh|SSH key share]]
==== znapzend installation setps ====
follow these simple instructions below to install **znapzend**. You need a compiler and install as follow. 
Download latest **[[https://github.com/oetiker/znapzend/releases|znapzend tar file]]**. Configure, make and install
<code>
wget https://github.com/oetiker/znapzend/releases/download/v0.17.0/znapzend-0.17.0.tar.gz
tar zxvf znapzend-0.17.0.tar.gz
cd znapzend-0.17.0
./configure --prefix=/opt/znapzend-0.17.0
make
make install

for x in /opt/znapzend-0.17.0/bin/*; do ln -s $x /usr/local/bin; done
</code>
==== Backup Plan ====
**NOTE:** ssh-key share required to run backup data to remote backup server. Use 'ssh-copy-id username@remote_host' to copy ssh-key.
== Design your backup plan: ==
<code>
/usr/local/bin/znapzendzetup create --recursive --mbuffer=/bin/mbuffer --mbuffersize=1G --tsformat='%Y-%m-%d-%H%M%S' --pre-snap-command=off --post-snap-command=off SRC '7d=>1d,30d=>1w,1y=>1m' mariodatapool/home DST:a '7d=>1d,30d=>1w,90d=>30d,1y=>3m,5y=>1y' root@10.10.0.4:datapool/backup_mario
</code>
>OUTPUT:
>>    *** backup plan: mariodatapool/home ***
>>    *dst_a           = root@10.10.0.4:datapool/backup_mario
>>    *dst_a_plan      = 7days=>1day,30days=>1week,90days=>30days,1year=>3months,5years=>1year
>>    *enabled         = on
>>    *mbuffer         = /bin/mbuffer
>>    *mbuffer_size    = 1G
>>    *post_znap_cmd   = off
>>    *pre_znap_cmd    = off
>>    *recursive       = on
>>    *src             = mariodatapool/home
>>    *src_plan        = 7days=>1day,30days=>1week,1year=>1month
>>    *tsformat        = %Y-%m-%d-%H%M%S
>>    *zend_delay      = 0
>>    
>>    Do you want to save this backup set [y/N]? y
>>    NOTE: if you have modified your configuration, send a HUP signal
>>    (pkill -HUP znapzend) to your znapzend daemon for it to notice the change.
==== Running ====
The **znapzend** daemon is responsible for doing the actual backups.
To see if your configuration is any good, run **znapzend** in **noaction mode** first
<code>
/usr/local/bin/znapzend --noaction --debug
</code>
(<color #ed1c24>OR</color>) If you don't want to wait for the scheduler to actually schedule work, you can also force immediate action by calling
<code>
/usr/local/bin/znapzend --noaction --debug --runonce=mariodatapool/home
</code>
>>    OUTPUT:
>>    [Fri Mar  2 13:46:43 2018] [info] znapzend (PID=105590) starting up ...
>>    [Fri Mar  2 13:46:43 2018] [info] refreshing backup plans...
>>    [Fri Mar  2 13:46:44 2018] [info] found a valid backup plan for mariodatapool/home...
>>    [Fri Mar  2 13:46:44 2018] [info] znapzend (PID=105590) initialized -- resuming normal operations.
>>    [Fri Mar  2 13:46:44 2018] [debug] snapshot worker for mariodatapool/home spawned (105606)
>>    [Fri Mar  2 13:46:44 2018] [info] creating recursive snapshot on mariodatapool/home
>>    # zfs snapshot -r mariodatapool/home@2018-03-02-134644
>>    [Fri Mar  2 13:46:44 2018] [debug] snapshot worker for mariodatapool/home done (105606)
>>    [Fri Mar  2 13:46:44 2018] [debug] send/receive worker for mariodatapool/home spawned (105607)
>>    [Fri Mar  2 13:46:44 2018] [info] starting work on backupSet mariodatapool/home
>>    # zfs list -H -r -o name -t filesystem,volume mariodatapool/home
>>    [Fri Mar  2 13:46:44 2018] [debug] sending snapshots from mariodatapool/home to root@10.10.0.4:datapool/backup_mario
>>    # zfs list -H -o name -t snapshot -s creation -d 1 mariodatapool/home
>>    # ssh -o batchMode=yes -o ConnectTimeout=30 root@10.10.0.4 zfs list -H -o name -t snapshot -s creation -d 1 datapool/backup_mario
>>    # ssh -o batchMode=yes -o ConnectTimeout=30 root@10.10.0.4 zfs list -H -o name -t snapshot -s creation -d 1 datapool/backup_mario
>>    [Fri Mar  2 13:46:44 2018] [debug] cleaning up snapshots on root@10.10.0.4:datapool/backup_mario
>>    # zfs list -H -o name -t snapshot -s creation -d 1 mariodatapool/home
>>    [Fri Mar  2 13:46:44 2018] [debug] cleaning up snapshots on mariodatapool/home
>>    [Fri Mar  2 13:46:44 2018] [info] done with backupset mariodatapool/home in 0 seconds
>>    [Fri Mar  2 13:46:44 2018] [debug] send/receive worker for mariodatapool/home done (105607)
then when you are happy with what you got, start it in daemon mode
<code>
/usr/local/bin/znapzend --daemonize
</code>
>>    OUTPUT:
>>    znapzend (7622) is running in the background now.
==== View and Modification of Backup plane ====
[[https://github.com/oetiker/znapzend/blob/master/doc/znapzendzetup.pod|REF:]] to the current running znapzend zfs backup plan
<code>
znapzendzetup list
</code>
to modify the source side backup plan
<code>
/usr/local/bin/znapzendzetup edit SRC '7days=>1day,30days=>1week,1year=>1month' mariodatapool/home

#the following command to apply the modified backup plane
pkill -HUP /usr/local/bin/znapzend
</code>
==== Backup statistics ====
It show the backup details of both source and destination servers
<code>
znapzendztatz 
</code>
==== Edit Backup plane ====
To change the backup plane:
<code>
znapzendzetup edit SRC '7days=>1day,30days=>1week,6month=>30days' tetrisdatapool/home_data DST:a '7days=>1day,30days=>1week,1year=>30days' root@10.10.48.5:tetrisarchivedatapool/backup_tetris
</code>

==== Referance ====
  * [[https://github.com/oetiker/znapzend/]]