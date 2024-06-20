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
snapshot_backup_status=$(znapzendztatz -H)


# Create datesource and save to file
filename="datasource_v4.html"

#echo "<html><body>" > ${filename}
echo "<table>" > ${filename}

echo "<tr><td>" >> ${filename}
echo "KEY" >> ${filename}
echo "</td><td>" >> ${filename}
echo "VALUE" >> ${filename}
echo "</td></tr>" >> ${filename}

echo "<tr><td>" >> ${filename}
echo "FQHN" >> ${filename}
echo "</td><td>" >> ${filename}
echo ${FQHN} >> ${filename}
echo "</td></tr>" >> ${filename}

echo "<tr><td>" >> ${filename}
echo "ZFS pool health" >> ${filename}
echo "</td><td>" >> ${filename}
echo ${zfs_pool_health_status} >> ${filename}
echo "</td></tr>" >> ${filename}

echo "<tr><td>" >> ${filename}
echo "ZFS checksum health" >> ${filename}
echo "</td><td>" >> ${filename}
echo ${checksum_health_status} >> ${filename}
echo "</td></tr>" >> ${filename}

echo "<tr><td>" >> ${filename}
echo "Zpool size" >> ${filename}
echo "</td><td>" >> ${filename}
echo ${zpool_size} >> ${filename}
echo "</td></tr>" >> ${filename}

echo "<tr><td>" >> ${filename}
echo "Zpool allocated" >> ${filename}
echo "</td><td>" >> ${filename}
echo ${zpool_alloc} >> ${filename}
echo "</td></tr>" >> ${filename}

echo "<tr><td>" >> ${filename}
echo "Zpool free" >> ${filename}
echo "</td><td>" >> ${filename}
echo ${zpool_free} >> ${filename}
echo "</td></tr>" >> ${filename}

echo "<tr><td>" >> ${filename}
echo "Zpool capacity" >> ${filename}
echo "</td><td>" >> ${filename}
echo ${zpool_capacity} >> ${filename}
echo "</td></tr>" >> ${filename}

echo "<tr><td>" >> ${filename}
echo "Zpool fragmentation" >> ${filename}
echo "</td><td>" >> ${filename}
echo ${zpool_fragmentation} >> ${filename}
echo "</td></tr>" >> ${filename}

echo "<tr><td>" >> ${filename}
echo "Zpool snapshot list" >> ${filename}
echo "</td><td>" >> ${filename}
echo ${snapshot_name_list}":"${snapshot_used_space}":"${snapshot_refer_space} >> ${filename}
echo "</td></tr>" >> ${filename}

echo "<tr><td>" >> ${filename}
echo "Zpool snapshot backup status" >> ${filename}
echo "</td><td>" >> ${filename}
echo ${snapshot_backup_status} >> ${filename}
echo "</td></tr>" >> ${filename}

echo "</table>" >> ${filename}
#echo "</body></html>" >> ${filename}

#EOF
