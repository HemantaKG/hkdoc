==== ZFS snapshot Troubleshooting ====
If the zfs **znapzend** stoped sending backups and zfs snapshots to backup server.
  - check error log(s) **/var/log/message|grep zfs** OR **/var/log/syslog|grep zfs**
  - check last snapshot details on both source and remove backup server usign **znapzendztatz** command
<code>
[root@master hemanta.kumar]# znapzendztatz
USED    LAST SNAPSHOT       DATASET
32.8T   2019-06-15-000000   mariodatapool/home
27.5T   2019-03-15-170000   root@10.10.0.4:datapool/backup_mario
</code>
=== sending all zfs snapshots to backup server ===
>last snapshot on backup server: 2019-03-15-170000
>recent snapshot on storage server: 2019-06-15-000000
send last to recent to backup server:
<code>
zfs send -I mariodatapool/home@2019-03-15-170000 mariodatapool/home@2019-06-15-000000|ssh -o batchMode=yes -o ConnectTimeout=30 'root@10.10.0.4' '/bin/mbuffer -q -s 128k -W 60 -m 1G|zfs recv -F datapool/backup_mario'
</code>
NOTE: its part of **zanpzend** snapshot backup step.
>if above command statement fails with an error
>>...
>>**cannot receive incremental stream: destination has been modified**
>>**internal error: Invalid argument**
>>**cannot receive: failed to read from stream**
>>...
try to send the last and its next snapshot to backup server using zfs snapshot send ans receive command line as follow: [[https://docs.oracle.com/cd/E19253-01/819-5461/gbimy/index.html|Send and Receiving a ZFS Snapshot]]
<code>
zfs send -i mariodatapool/home@2019-03-15-170000 mariodatapool/home@2019-03-15-180000 | ssh root@10.10.0.4 zfs recv -F datapool/backup_mario
</code>
After successfully sending the last fail snapshot try to send next snapshot(s) using **zanpzend** snapshot send command line as follow:
<code>
zfs send -I mariodatapool/home@2019-03-15-180000 mariodatapool/home@2019-06-15-000000|ssh -o batchMode=yes -o ConnectTimeout=30 'root@10.10.0.4' '/bin/mbuffer -q -s 128k -W 60 -m 1G|zfs recv -F datapool/backup_mario'
</code>
>If you get following error, don't worry you can ignore it and run the same above command line again:
>>**mbuffer: error: watchdog timeout: input stalled; sending SIGINT**
>>**mbuffer: error: watchdog timeout: output stalled; sending SIGINT**
>>**mbuffer: warning: error during output to <stdout>: canceled**
>>**cannot receive: failed to read from stream**
NOTE: If a many snapshots are pending to backup than; send a few snapshots at a time, and repeated this process till you reach the recent snapshot. (some times the znapzend starts taking snapshot backup after manual send using zfs snapshot send command line.)