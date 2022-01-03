=== System details ===
  * Operating system: CentOS 7 64 bit
  * Hostname: sambaserver.myorg.in
  * IP Address: 192.x.x.x/24
  * NOTE: **Disable SELinux service**

==== Install Samba server ====
Install Samba server by running following command
<code>yum install samba* -y</code>
Check for samba package those you installed by using the above command, as
<code>
rpm -qa | grep samba
yum list installed | grep samba
</code>
==== start Samba service ====
Start samba services, and enable them to start automatically on every reboot
<code>
systemctl start smb
systemctl start nmb

systemctl enable smb
systemctl enable nmb
</code>

==== Firewall configuration ====
Allow Samba server default ports through firewall, NOTE: iff firewall enable
<code>
firewall-cmd --permanent --add-port=137/tcp
firewall-cmd --permanent --add-port=138/tcp
firewall-cmd --permanent --add-port=139/tcp
firewall-cmd --permanent --add-port=445/tcp
firewall-cmd --permanent --add-port=901/tcp

#Restart firewall to apply the changes
firewall-cmd --reload
</code>
----
==== Configure a read-only access to a directory by Anonymous user (OR) Anonymous user share ====
Now, let us create a directory for **anonymous share** with users.
NOTE: Anyone can only read this share, the password isn't required to access this directory
  * Create a directory called **/software/share** and set **read-only** permission.
NOTE: You can name this share as per your liking
<code>mkdir -p /software/share
chmod -R 0755 /software/share
</code>
=== Edit Samba configuration file ===
Add the following code block at the end of **/etc/samba/smb.conf** file to allow read-only access to **/software/share** directory to any user without username and password
<code>
nano /etc/samba/smb.conf

[IT-Share]
  path = /software/share
  browsable = Yes
  read only = Yes
  guest ok = Yes
  create mode = 0444
</code>
----
==== Configure a read-only accessed to Security Enabled directory share ====
Creating a read-only accessed samba share.
Now, let us create a password protected samba share so that the users should enter the valid username and password to access the shared directory
  * Create a user called **it_sw** and a group called **smbgroup**
  * Assign the user **it_ws** to **smbgroup** group, and set **samba password** to that **it-sw** user.
<code>
# create user account without login permissions
useradd -s /sbin/nologin it_sw
# add smbgroup
groupadd smbgroup
# add user to "smbgroup"
usermod -a -G smbgroup it_sw

# set samba password for the user "it_sw"
smbpasswd -a it_sw
</code>
Create a new directory for share **/software/sw**
<code>
mkdir /software/sw
chown -R it_sw:smbgroup /software/sw
</code>
Add the following code block to **/etc/samba/smb.conf** file to allow read-only access to **/software/sw** directory with valib username and password
<code>
nano /etc/samba/smb.conf
[sw]
path = /software/sw
writable = No
browsable = Yes
guest ok = No
valid users = @smbgroup
</code>
----
==== Test/check Samba directory share configuration ====
Run the following command to test Samba configuration 
<code>
testparm
</code>
>>NOTE: OUTPUT something like below
>>Load smb config files from /etc/samba/smb.conf
>>rlimit_max: increasing rlimit_max (1024) to minimum Windows limit (16384)
>>Processing section "[homes]"
>>Processing section "[IT-Share]"
>>Loaded services file OK.
>>Server role: ROLE_STANDALONE
>>
>>Press enter to see a dump of your service definitions
>>
>>Global parameters
>>[global]
>>    workgroup = SAMBA
>>    printcap name = cups
>>    security = USER
>>    idmap config * : backend = tdb
>>    cups options = raw
>>
>>[homes]
>>    comment = Home Directories
>>    browseable = No
>>    inherit acls = Yes
>>    read only = No
>>    valid users = %S %D%w%S
>>
>>[IT-Share]
>>    path = /software/share
>>    create mask = 0444
>>    guest ok = Yes
If every thing fine, than restart samba services to effect the chages:
<code>
systemctl restart smb
systemctl restart nmb
</code>
==== Reference ====
[[https://www.unixmen.com/install-configure-samba-server-centos-7/|Install And Configure Samba Server In CentOS7]]
