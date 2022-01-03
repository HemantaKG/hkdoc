## This script helps to auto do the following tasks:
### 1. dump MySQL database using "mysqldump"; file saved at ${mysqldump_loc} directory with name ${MYSQLDUMP_FILE} on source host
###	2. backup above generated Mysql dump file to backup storage; at location ${mysqldump_destination_loc}
###	3. backup specified source data directories ${source_data_dir} to location ${data_destination_loc on backup storage
###	4. recods "log" and "error" to ${logfile_loc} location on source host with name "_idackup***.log" and "_ibackup_***.err" respectivily
###	5. sends backup status notification email to list of users ${send_email_to}) 
### 6. removes all last 7 days old files log, err and mysql-dump files 

### filename: ibackup.sh


```bash

#!/bin/bash
###########################################################################################################################################
#
### This script helps to auto do the following tasks:
#	1. dump MySQL database using "mysqldump"; file saved at ${mysqldump_loc} directory with name ${MYSQLDUMP_FILE} on source host
#	2. backup above generated Mysql dump file to backup storage; at location ${mysqldump_destination_loc}
#	3. backup specified source data directories ${source_data_dir} to location ${data_destination_loc on backup storage
#	4. recods "log" and "error" to ${logfile_loc} location on source host with name "_idackup***.log" and "_ibackup_***.err" respectivily
#	5. sends backup status notification email to list of users ${send_email_to}) 
#   6. removes all last 7 days old files log, err and mysql-dump files 
#
### The things to do before running this script:
##	1. chage the following variables of this script as per your requirment;
#		a. set ${is_mysql_db}="yes" if your want to take mysql bump backup, otherwise set ${is_mysql_db}="no"
#		b. set mysql dump file name ${MYSQLDUMP_FILE}, mysql dump file location on source host ${mysqldump_loc} and mysql dump file destination location ${mysqldump_destination_loc} , if ${is_mysql_db}="yes"
#		c. set source data location ${source_data_dir}
#		d. set destination host ${destination_host}
#		e. set destination location ${data_destination_loc}
##	2. create "mysqlbackup" directory under ${mysqldump_loc} on source host
##	3. create the following directories at destination host under ${mysqldump_destination_loc}
#		a. make directory with name of source hostname 
#		b. make "mysqlbackup" directory under above created directory
#
## Run script (or) add as crontad job:
#	bash ./ibackup_v3.sh
#
# Hemanta Kumar G
# DT20180403
###########################################################################################################################################


#get source machine hostname; don't this variable
HN=`hostname`

#if mysql database running than set "yes" else set "no"
is_mysql_db="no"

#set file name for mysql-dump with hostname and date as a part of file name
MYSQLDUMP_FILE="mysql_dump_${HN}_"`date +"%Y_%m_%d"`".sql"

#set the destination directory for mysql-dump; change to your path 
mysqldump_loc="/home/ibackup/mysqlbackup"

#set the backup source directory; change to your source path
source_data_dir="/home/hemanta/action_items"
#source directory path is command line input example: "/home/hemanta/hm_etc/convert_csv_cfg_nagios /home/hemanta/action_items"
#source_data_dir=$1

#set destination machine FQHN; NOTE: change to your destination host
destination_host="ibackup@<<change hostname>>"

#set the backup destination directory on destination machine; NOTE: change to your destination path
mysqldump_destination_loc="/ibackup/${HN}/mysqlbackup/"
data_destination_loc="/ibackup/${HN}/"

#set email address to send alert mails; NOTE: change email address
send_email_to="<<change email id>> <<change email id>> <<change email id>>"

#set the number of days you want to keep the backup files (example set KEEP_BACKUP_UPTO_DAYS= 8, to keep upto backu file of last 7 day)
KEEP_UPTO_DAYS=8

#status variable default value "0"
PROBLEM=0

#log file details
logfile_loc=$(pwd)
log_file=${logfile_loc}"/_ibackup_"`date +"%Y_%m_%d"`".log"
#error file details
errfile_loc=$(pwd)
err_file=${errfile_loc}"/_ibackup_"`date +"%Y_%m_%d"`".err"

#recode date into log and error files
printf '%s\n' "`date`">>${log_file}
printf '%s\n' "`date`">>${err_file}

#function to remove last 7 days old files
remove_files()
{
	file_loc=$1
	filetype=$2
	oldfile_list=("$(ls -t ${file_loc}/${filetype})")
	#echo ${oldfile_list}
	count=0
	for filename in ${oldfile_list[@]}; do
		count=$((count+1))
		if [ ${count} -eq ${KEEP_UPTO_DAYS} ]; then
			#echo ${filename}
			remove="$(rm ${filename})"
		fi
	done
}

#take mysql-dump, rsync mysql-dump and rsync data (if mysql db present execute if part,; else execute else part)
if [ "${is_mysql_db}" == "yes" ]; then
	printf '%s\n' "MySQL dump start:">>${log_file}
	#dump all MySQL databases
	mysqldump --all-databases >> ${mysqldump_loc}/${MYSQLDUMP_FILE} 2> ${err_file}
	mysqldump_exit_state=$?
	printf '%s\n' "MySQL dump end:">>${log_file}
	#in case mysql-dump fails
	if [ ${mysqldump_exit_state} -ne 0 ]; then
		email_body="MySQL dump fail."
		PROBLEM=1
	else
	  #remove all last 7 days old mysql-dump files from the directory
	  #remove_file() funtion call by passing two funtion parameters
	  remove_files ${mysqldump_loc} "*.sql"
		
		printf '%s\n' "backup start: ${MYSQLDUMP_FILE}">>${log_file}
		#backup mysqldump generated file
		rsync -avblph ${mysqldump_loc}/${MYSQLDUMP_FILE} ${destination_host}:${mysqldump_destination_loc} >> ${log_file} 2>> ${err_file}
		rsync_exit_state=$?
		printf '%s\n' "backup end: ${MYSQLDUMP_FILE}">>${log_file}
		#check for rsync error
		if [ ${rsync_exit_state} -ne 0 ]; then
			email_body=${MYSQLDUMP_FILE}" rsync fail."
			PROBLEM=1
		else
			printf '%s\n' "backup start: ${source_data_dir}">>${log_file}
			#backup data directory
			rsync -avblph ${source_data_dir} ${destination_host}:${data_destination_loc} >> ${log_file} 2>> ${err_file}
			rsync_exit_state=$?
			printf '%s\n' "backup end: ${source_data_dir}">>${log_file}
			#check for rsync error
			if [ ${rsync_exit_state} -ne 0 ]; then
				email_body=${source_data_dir}" rsync fail."
				PROBLEM=1
			fi
		fi
	fi
else
	printf '%s\n' "backup start: ${source_data_dir}">>${log_file}
	#backup data directory
	rsync -avblph ${source_data_dir} ${destination_host}:${data_destination_loc} >> ${log_file} 2>> ${err_file}
	rsync_exit_state=$?
	printf '%s\n' "backup end: ${source_data_dir}">>${log_file}
	#check for rsync error
	if [ ${rsync_exit_state} -ne 0 ]; then
		email_body=${source_data_dir}" rsync fail."
		PROBLEM=1
	fi
fi

#remove all last 7 days old log and err files from the directory
#remove all last 7 days old log files from the directory
remove_files ${logfile_loc} "*.log"
#remove all last 7 days old err files from the directory
remove_files ${errfile_loc} "*.err"

#error file
ibackup_error_file=`cat ${err_file}`

#send mail
if [ ${PROBLEM} -ne 0 ]; then
	#printf '%s\n' "${HN} Backup failed: " ${email_body}
	printf '%s\n' "`date` - ${email_body} - Please check error file - ${err_file} - ${ibackup_error_file}"| /usr/bin/mail -s "${HN} - Backup Failed!!" ${send_email_to}
else
	#printf '%s\n' "${HN} Backup success."
	printf '%s\n' "`date` - Backup Success"| /usr/bin/mail -s "${HN} - Backup Success" <<change email id>>
fi

### EOF ###

```
