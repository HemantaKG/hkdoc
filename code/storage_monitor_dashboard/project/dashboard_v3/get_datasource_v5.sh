#!/bin/bash

# Get server hostname
FQHN=$(hostname -f)

# Health - Check if all zfs volumes are in good condition. We are looking for any keyword signifying a degraded or broken array.
health_condition=$(zpool status | egrep -i '(DEGRADED|FAULTED|OFFLINE|UNAVAIL|REMOVED|FAIL|DESTROYED|corrupt|cannot|unrecover)')
if [ "${health_condition}" ]; then
  zfs_pool_health_status="FAULTY"
else
  zfs_pool_health_status="HEALTHY"
fi


# Capacity - Check zpool Total space and the Total space in use
zpool_size=$(zpool list -H -o size)
zpool_alloc=$(zpool list -H -o alloc)
zpool_free=$(zpool list -H -o free)
zpool_capacity=$(zpool list -H -o capacity)
zpool_fragmentation=$(zpool list -H -o fragmentation)


# Errors - Check the columns for READ, WRITE and CKSUM (checksum) drive errors on all volumes and all drives using "zpool status"
checksum_errors=$(/sbin/zpool status | grep ONLINE | grep -v state | awk '{print $3 $4 $5}' | grep -v 000)
if [ "${checksum_errors}" ]; then
  checksum_health_status="CHECKSUM Error"
else
  checksum_health_status="HEALTHY"
fi


# ZPOOL snapshot backup(s) and latest snapshot status
snapshot_name_list=$(zfs list -t snapshot -H -o name)
snapshot_used_space=$(zfs list -t snapshot -H -o used)
snapshot_refer_space=$(zfs list -t snapshot -H -o refer)
snapshot_backup_status=$(znapzendztatz -H 2> /dev/null)


# Create datesource and save to file
filename="datasource_v55.csv"

echo "KEY,VALUE" > ${filename}
echo "FQHN,"${FQHN} >> ${filename}
echo "ZFS pool health,"${zfs_pool_health_status} >> ${filename}
echo "ZFS checksum health,"${checksum_health_status} >> ${filename}
echo "Zpool size,"${zpool_size} >> ${filename}
echo "Zpool allocated,"${zpool_alloc} >> ${filename}
echo "Zpool free,"${zpool_free} >> ${filename}
echo "Zpool capacity,"${zpool_capacity} >> ${filename}
echo "Zpool fragmentation,"${zpool_fragmentation} >> ${filename}
echo "Zpool snapshot list,"${snapshot_name_list}":"${snapshot_used_space}":"${snapshot_refer_space} >> ${filename}
echo "Zpool snapshot backup status,"${snapshot_backup_status} >> ${filename}

#EOF
