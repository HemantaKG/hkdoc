echo "<html><body>" > datasource_v2.html
# hostname
echo "<table>" >> datasource_v2.html
echo "<tr><th>" >> datasource_v2.html
echo "hostname" >> datasource_v2.html
echo "</th><th>" >> datasource_v2.html
hostname >> datasource_v2.html 2>&1
echo "</th></tr>" >> datasource_v2.html

# FQDN name
echo "<tr><th>" >> datasource_v2.html
echo "FQDN Name: " >> datasource_v2.html
echo "</th><th>" >> datasource_v2.html
hostname -f  >> datasource_v2.html 2>&1
echo "</th></tr>" >> datasource_v2.html

# zpool health status
echo "<tr><th>" >> datasource_v2.html
echo "zpool health status:" >> datasource_v2.html
echo "</th><th>" >> datasource_v2.html
zpool status -x >> datasource_v2.html 2>&1
echo "</th></tr>" >> datasource_v2.html

# zpool stauts
#echo "<tr><th>" >> datasource_v2.html
#echo "zpool status:" >> datasource_v2.html
#echo "</th><th>" >> datasource_v2.html
#zpool status >> datasource_v2.html 2>&1
#echo "</th></tr>" >> datasource_v2.html

# zfs storage size
echo "<tr><th>" >> datasource_v2.html
echo "zfs storage size:" >> datasource_v2.html
echo "</th><th>" >> datasource_v2.html
zfs list >> datasource_v2.html 2>&1
echo "</th></tr>" >> datasource_v2.html

# zfs snapshot backup status
echo "<tr><th>" >> datasource_v2.html
echo "zfs snapshot backup status:" >> datasource_v2.html
echo "</th><th>" >> datasource_v2.html
znapzendztatz >> datasource_v2.html 2>&1
echo "</th></tr>" >> datasource_v2.html

# zfs snapshot list
echo "<tr><th>" >> datasource_v2.html
echo "zfs snapshot list:" >> datasource_v2.html
echo "</th><th>" >> datasource_v2.html
zfs list -t snapshot >> datasource_v2.html 2>&1
echo "</th></tr>" >> datasource_v2.html

echo "</table>" >> datasource_v2.html
echo "</body></html>" >> datasource_v2.html

