#hostname
echo "hostname:" >> datasource.dat
hostname >> datasource.dat 2>&1
echo "" >> datasource.dat

#FQDN name
echo "FQDN Name: " >> datasource.dat
hostname -f  >> datasource.dat 2>&1
echo "" >> datasource.dat

#zpool health status
echo "zpool health status:" >> datasource.dat
zpool status -x >> datasource.dat 2>&1
echo "" >> datasource.dat

#zpool stauts
echo "zpool status:" >> datasource.dat
zpool status >> datasource.dat 2>&1
echo "" >> datasource.dat

#zfs storage size
echo "zfs storage size:" >> datasource.dat
zfs list >> datasource.dat 2>&1
echo "" >> datasource.dat

##zfs snapshot backup status
echo "zfs snapshot backup status:" >> datasource.dat
znapzendztatz >> datasource.dat 2>&1
echo "" >> datasource.dat

#zfs snapshot list
echo "zfs snapshot list:" >> datasource.dat
zfs list -t snapshot >> datasource.dat 2>&1
echo "" >> datasource.dat

