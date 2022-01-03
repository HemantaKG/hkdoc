## Python script to reads a csv file and generates a Nagios cfg file
### filename: read_csv_generate_nagios_cfg.py

```python

#!/usr/bin/python

"""
this script reads csv file and generates a Nagios cfg file
the input csv file record contains following information
	[[host_name,alias,address]]

Run the script as follow:
	$> python generate_host_block_nagios_cfg.py --ifn <<input csv filename>> --floc <<input file location>> --gn <<host group name>> --ofn <<output filename>>
	Example:
	$> python generate_host_block_nagios_cfg.py --ifn ipphone.txt --floc /home/hemanta/Desktop/ --gn ipphone --ofn ipphone

DT: 170711
Name: Hemanta
File Name: generate_host_block_nagios_cfg.py
"""

import sys, getopt, subprocess, crypt

def main(comm_argv):
	# group name
	hostgroupname= ''
	# csv file location
	location= ''
	# csv input file name
	infilename= ''
	# cgf output file name
	outfilename= ''
	
	# command line input parsing
	# check for number of arguments must be greater than 1
	if len(sys.argv) >1 and (sys.argv[1]== '--ifn') and (sys.argv[3]== '--floc') and (sys.argv[5]== '--gn') and (sys.argv[7]== '--ofn'):
		try:
			# store command line inputs into (option, argument) list
			option_list, argumrnt_list= getopt.getopt(comm_argv, '',["ifn=", "floc=", "gn=", "ofn="]) 
		except getopt.GetoptError:
			# print the input format
			print 'generatenagioscfg.py --ifn ipphone.txt --floc /home/hemanta/Desktop/ --gn ipphone --ofn ipphone' 
			sys.exit(2)
		# featch argument values from list option_list
		for option, arg in option_list:
			if option== '--ifn':
				infilename= arg
			elif option== '--floc':
				location= arg
			elif option== '--gn':
				hostgroupname= arg
			elif option== '--ofn':
				outfilename= arg
	else:
		# print the script run format
		print 'generatenagioscfg.py --ifn ipphone.txt --floc /home/hemanta/Desktop/ --gn ipphone --ofn ipphone' 
		# exit on running wrong format
		sys.exit(2)

	# read records from csv input file
	print infilename, location, hostgroupname, outfilename
	csvfile= location+ infilename
	foi= open(csvfile, 'r')
	lines= foi.readlines()
	foi.close()
	
	# write blocks into output cfg file
	def createcfgfile(block):
		cfgfile= location+ outfilename+ ".cfg"
		fow= open(cfgfile, 'a')
		fow.write(block+"\n")
		fow.close()

	# required format block generate
	def createblock(wrds):
		block= "define host{"
		block= block+"\n\tuse\tgeneric-switch"
		block= block+"\n\thost_name\t"+wrds[0]
		block= block+"\n\talias\t"+wrds[1]
		block= block+"\n\taddress\t"+wrds[2]
		block= block+"\thostgroups\t"+hostgroupname
		block= block+"\n\tcontact_groups\tadmins"
		block= block+"\n\tnotification_interval\t0"
		block= block+"\n}"
		createcfgfile(block)		

	# split inout csv file
	for line in lines:
		wrds= line.split(',')
		createblock(wrds)

if __name__ == "__main__":
	main(sys.argv[1:])

### EOS ###

#sample block
#define host{
#        use             generic-switch
#        host_name       Sutlej-x460 
#        alias           SUTLEJ X460 Switch
#        address         10.0.*.*
#        hostgroups      X460
#        contact_groups  admins
#        notification_interval   0
#        }
#
### EOF ###

```
