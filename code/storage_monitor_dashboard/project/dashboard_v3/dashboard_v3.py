# Sample datasource (.csv) file
#
# FQHN,storage.tetris.icts.res.in
# ZFS pool health,HEALTHY
# ZFS checksum health,HEALTHY
# Zpool size,261T
# Zpool allocated,139T
# Zpool free,122T
# Zpool capacity,53%
# Zpool fragmentation,38%
# Zpool snapshot list,tetrisdatapool/home_data@2020-10-08-000000 tetrisdatapool/home_data@2020-10-15-000000 tetrisdatapool/home_data@2020-10-22-000000 tetrisdatapool/home_data@2020-10-29-000000 tetrisdatapool/home_data@2020-11-05-000000 tetrisdatapool/home_data@2020-11-06-000000 tetrisdatapool/home_data@2020-11-07-000000 tetrisdatapool/home_data@2020-11-08-000000 tetrisdatapool/home_data@2020-11-09-000000 tetrisdatapool/home_data@2020-11-10-000000 tetrisdatapool/home_data@2020-11-11-000000 tetrisdatapool/home_data@2020-11-12-000000 tetrisdatapool/home_data@2020-11-13-000000:1.77T 833G 511G 362G 25.5G 9.50G 11.6G 13.5G 13.4G 45.1G 19.6G 16.4G 11.0G:105T 105T 105T 105T 109T 109T 109T 109T 110T 110T 112T 112T 113T
# Zpool snapshot backup status,4.23T 2020-11-13-000000 tetrisdatapool/home_data 12.3T 2020-11-13-000000 root@10.10.48.5:tetrisarchivedatapool/backup_tetris
#
# Hint:
# https://codepen.io/raubaca/pen/PZzpVe
#
#
# Code: Storage Monitor DashBoard
#
# Hemanta Kumar G
# ICTS-TIFR
# DT20201123
#


import pandas as pd
import glob


final_str_write= """
<!DOCTYPE html>
<html lang="en">

<head>
  <title>storage monitor</title>
  <meta charset="UTF-8">

  <link rel="stylesheet" href="css/styles1.css">
  <link rel="stylesheet" href="css/styles2.css">
</head>

<body translate="no">
  <h1>Storage Monitor</h1>
    <div class="tabs">
"""

str_write= ""
tc= 0
for fname in glob.glob("/home/hemanta/data/action_items/storage_monitor/project/dashboard_v3/dataset/*.csv"):
	df= pd.read_csv(fname)
	#print(df)
	mylist= list(df.columns)
	k= df['KEY']
	v= df['VALUE']
	#print(k[8])
	#print(v[8])

	fqhn= v[0]
	if fqhn== "localhost" or fqhn== "":
	   fqhn= fname.split('/')[-1].split('.')[0]
	   
	zpool_status= v[1]
	zpool_checksum_status= v[2]
	zpool_size= v[3]
	zpool_allocated= v[4]
	zpool_free_space= v[5]
	zpool_use_capacity= v[6]
	zpool_fragmentation= v[7]
	
	space_use= int(zpool_use_capacity.replace('%', ''))
	fragmentation= int(zpool_fragmentation.replace('%', ''))
	
	tc= tc+1
	str_write= str_write+ """<div class="tab">
	<input type="radio" id=rd"""+ str(tc)+ """ name=rd>
    <label class="tab-label" for=rd"""+ str(tc)+ """>"""+fqhn+"""</label>
    <div class="tab-content">"""
    
	str_write= str_write+ "<div class=a><table class=a><tr><th>FQHA</th><td><font class=c>"+ fqhn+ "</font></td></tr>"

	if zpool_status !="HEALTHY":
		str_write= str_write+ "<tr><th class=a> zpool status</th><td class=a><font class=r>"+ zpool_status+ "</font></td></tr>"
	else:
		str_write= str_write+ "<tr><th class=a> zpool status</th><td class=a><font class=g>"+ zpool_status+ "</td></tr>"
	
	if zpool_checksum_status !="HEALTHY":
		str_write= str_write+ "<tr><th class=a> zpool checksum status</th><td class=a><font class=r>"+ zpool_checksum_status+ "</font></td></tr>"
	else:
		str_write= str_write+ "<tr><th class=a> zpool checksum status</th><td class=a><font class=g>"+ zpool_checksum_status+ "</td></tr>"
	
	str_write= str_write+ "<tr><th class=a> zpool size</th><td class=a><font class=c>"+ zpool_size+ "</font></td></tr><tr><th class=a> data allocation</th><td class=a><font class=c>"+ zpool_allocated+ "</font></td></tr>"

	if space_use< 80:
		str_write= str_write+ "<tr><th class=a> zpool used</th><td class=a><font class=c>"+ zpool_use_capacity+ "</font><br><progress class=progress-g min=0 max=100 value="+ str(space_use)+ "></progress></td></tr>"
	else:
		str_write= str_write+ "<tr><th class=a> zpool used</th><td class=a><font class=c>"+ zpool_use_capacity+ "<br><progress class=progress-r min=0 max=100 value="+ str(space_use)+ "></progress></font></td></tr>"
	
	if fragmentation< 80:
		str_write= str_write+ "<tr><th class=a> zpool fragmentation</th><td class=a><font class=c>"+ zpool_fragmentation+ "<br><progress class=progress-g min=0 max=100 value="+ str(fragmentation)+ "></progress></font></td></tr>"
	else:
		str_write= str_write+ "<tr><th class=a> zpool fragmentation</th><td class=a><font class=c>"+ zpool_fragmentation+ "<br><progress class=progress-r min=0 max=100 value="+ str(fragmentation)+ "></progress></font></td></tr>"
		
	str_write= str_write+ "<tr><th class=a>snapshot list</th><td class=a><font class=c>"
	if v[8]!= '::':
		snap_list, used_list, ref_list= v[8].split(':')
		snap= snap_list.split(' ')
		used= used_list.split(' ')
		ref= ref_list.split(' ')
		i= 0
		tmp_list=""
		for snap_name in snap:
			#print(snap_name+ " --- "+ used[i]+ " --- "+ ref[i])
			tmp_list= tmp_list+ snap_name+ " --- "+ used[i]+ " --- "+ ref[i]+ "<br>"
			i= i+1
		i= 0
	else:
		#print("No snapshot")
		tmp_list= "NONE"
	
	snap= used= ref= ''
	str_write= str_write+ tmp_list+ "</font></td></tr>"
	
	tmp_list= ""
	if isinstance(v[9], str):
		snap_status_list= v[9].split(' ')
		#print(snap_status_list[0]+ " --- "+ snap_status_list[1]+ " --- "+ snap_status_list[2])
		#print(snap_status_list[3]+ " --- "+ snap_status_list[4]+ " --- "+ snap_status_list[5])
		tmp_list= "<tr><th class=a>backup status</th><td class=a><font class=c>"+ snap_status_list[0]+ " --- "+ snap_status_list[1]+ " --- "+ snap_status_list[2]+ "<br>"+ snap_status_list[3]+ " --- "+ snap_status_list[4]+ " --- "+ snap_status_list[5]+ "</font></td></tr>" 
	else:
		#print("No snapshot")
		tmp_list= "<tr><th class=a>backup status</th><td class=a><font class=c>NONE</font></td></tr>"
	
	str_write= str_write+ tmp_list
	str_write= str_write+ "</table></div></div></div>"

str_write= str_write+ """
      <div class="tab">
        <input type="radio" id=rd"""+str(tc+1) +""" name="rd">
        <label for=rd"""+str(tc+1)+ """ class="tab-close">Close &times;</label>
      </div>"""
      
final_str_write= final_str_write+ str_write+ "</div></body></html>"
file_writer= open("dashboard_v3.html", 'w')
file_writer.write(final_str_write)
file_writer.close()

## EOF

