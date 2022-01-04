# zfs and zpool Filesystem Health Check Script
## Create a shell script "Ex: filename "zpool_health_check.sh" location "/opt/"
### Filename: zpool_health_check.sh

```bash
#! /bin/sh
#
# Calomel.org
#     https://calomel.org/zfs_health_check_script.html
#     FreeBSD ZFS Health Check script
#     zfs_health.sh @ Version 0.17

# Check health of ZFS volumes and drives. On any faults send email.

# server name change it
server_name="server_name"

# 99 problems but ZFS aint one
problems=0


# Health - Check if all zfs volumes are in good condition. We are looking for
# any keyword signifying a degraded or broken array.

condition=$(/sbin/zpool status | egrep -i '(DEGRADED|FAULTED|OFFLINE|UNAVAIL|REMOVED|FAIL|DESTROYED|corrupt|cannot|unrecover)')
if [ "${condition}" ]; then
        emailSubject="`hostname`@{server_name} - ZFS pool - HEALTH fault"
        problems=1
fi


# Capacity - Make sure the pool capacity is below 80% for best performance. The
# percentage really depends on how large your volume is. If you have a 128GB
# SSD then 80% is reasonable. If you have a 60TB raid-z2 array then you can
# probably set the warning closer to 95%.
#
# ZFS uses a copy-on-write scheme. The file system writes new data to
# sequential free blocks first and when the uberblock has been updated the new
# inode pointers become valid. This method is true only when the pool has
# enough free sequential blocks. If the pool is at capacity and space limited,
# ZFS will be have to randomly write blocks. This means ZFS can not create an
# optimal set of sequential writes and write performance is severely impacted.

maxCapacity=80

if [ ${problems} -eq 0 ]; then
   capacity=$(/sbin/zpool list -H -o capacity | cut -d'%' -f1)
   for line in ${capacity}
     do
       if [ $line -ge $maxCapacity ]; then
         filled_upto=$(df -Th|grep zfs|awk -F " " '{print $6}')
         emailSubject="`hostname`@{server_name} - ZFS pool - Capacity Exceeded - Filled upto ${filled_upto}"
         problems=1
       fi
     done
fi

# Errors - Check the columns for READ, WRITE and CKSUM (checksum) drive errors
# on all volumes and all drives using "zpool status". If any non-zero errors
# are reported an email will be sent out. You should then look to replace the
# faulty drive and run "zpool scrub" on the affected volume after resilvering.
if [ ${problems} -eq 0 ]; then
   errors=$(/sbin/zpool status | grep ONLINE | grep -v state | awk '{print $3 $4 $5}' | grep -v 000)
   if [ "${errors}" ]; then
        emailSubject="`hostname`@{server_name} - ZFS pool - Drive Errors"
        problems=1
   fi
fi

# Email - On any problems send email with drive status information and
# capacities including a helpful subject line. Also use logger to write the
# email subject to the local logs. This is also the place you may want to put
# any other notifications like playing a sound file, beeping the internal 
# speaker, paging someone or updating Nagios or even BigBrother.

if [ "$problems" -ne 0 ]; then
  printf '%s\n' "$emailSubject" "" "'/sbin/zpool list'" "" "'/sbin/zpool status'" | /usr/bin/mail -s "$emailSubject" <<change email id>> <<change email id>>
  logger $emailSubject
else
  emailSubject="`hostname`@{server_name} ZFS pool - Normal, No Errors"
  printf '%s\n' "$emailSubject" "" "`/sbin/zpool list`" "" "`/sbin/zpool status`" | /usr/bin/mail -s "`hostname`@{server_name}: ZFS health check report" <<change email id>> <<change email id>>
  logger $emailSubject
fi

### EOF ###
```
