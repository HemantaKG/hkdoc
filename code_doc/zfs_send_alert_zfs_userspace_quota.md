## The python script helps to check zfs user's quota used by the user and sends alert mesaage to users if the user consumed >=80% of allocated zfs user quota

```python

### filename: python zfs_userspace_alert.py
"""
The python script helps to check zfs user's quota used by the user and sends alert mesaage to users;
if the user consumed >=80% of allocated zfs user quota

#crontad add, run script at every 12 hours
0 */12 * * * python /opt/zfs_userspace_check/zfs_userspace_alert.py

Hemanta Kumar G.
ICTS-TIFR
DT20180321 
"""

from email.mime.text import MIMEText
from subprocess import Popen, PIPE
import subprocess

"""
# user list .txt file; present at same directory
user_list_file = "user_list.txt"
"""
#set mail related details
from_addr= "<<change email id>>"
bcc_addr= "<<change email id>>"
mail_sub= "Mario: Your home quota full!!"

# get userspace use details
zfs_command = subprocess.Popen(['zfs', 'userspace', 'mariodatapool/home'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
out, err = zfs_command.communicate()
linelist= out.splitlines()

#global list and dictionary to store user information
#spacelist=[]
userinfo={}

for line in linelist[1:-1]:
  wordlist= line.split()
  user= wordlist[2]
  spaceuse= wordlist[3]
  spacealloc= wordlist[4]
  #if user quota not allocated and user reached data size TB scale than add user to list spacelist
  spacelist=[]
  if spacealloc!= 'none' and spaceuse[-1]== 'T':
      spacelist.append(spaceuse[:-1])
      spacelist.append(spacealloc[:-1])
      #add list to userinfo dict iff user consumed 80% of allocated space quota
      if float(spacelist[0])>= 0.8* float(spacelist[1]):
        userinfo[user]= spacelist

"""
#read user details file and add user email id to userinfo list
if bool(userinfo):
  fs= open(user_list_file, 'r')
  for uline in fs.read().splitlines():
    username,uemail= uline.split(',')
    if username in userinfo:
      userinfo[username].append(uemail)
"""

#send alert mail to user for clear space
if bool(userinfo):
	for user in userinfo:
		msg_body= """
		Your "/home" space quota almost filled.
		You are consumed around """+ userinfo[user][0] + """TB disk space, of the allocated disk space of 3TB.
		Please clear some data.
		
		Note:
		don't reply, it is a system generated mail.
		for any HPC relateed queries, write to "<<change email id>>"
		
		Thank you.
		
		Regards,
		HPC support
		ICTS-TIFR
		"""
		msg = MIMEText("Dear "+ user +",\n"+ msg_body)
		msg["From"] = from_addr
		msg["To"] = user+"@<<change email domain>>"
		msg["Bcc"] = bcc_addr
		msg["Subject"] = mail_sub
		p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
		out= p.communicate(msg.as_string())
### EOF ###

```
