==== RPMdb checksum Error or Warning ====
If you're getting the following error are warning while installing packages using yum
<code>
 Error: Rpmdb checksum is invalid: pkg checksums ...
OR
 Warning: RPMDB altered outside of yum ...
</code>
Resolve by:
<code>
yum history sync
</code>
==== KIckStart Installation Guide ====
Ref: [[http://pykickstart.readthedocs.io/en/latest/kickstart-docs.html|Kickstart Documentation]]
==== Change and Setting Time-Zone of your System ====
  * Please do following for CentOS
<code>
# show the list of timezones
timedatectl list-timezones

# set timezone
timedatectl set-timezone Asia/Kolkata

# show status
timedatectl
</code>
==== locate install and locate db update ====
  * ''yum install mlocate'' for centos
  * ''updatedb''  creates  or updates a database used by ''locate'' command 
  * ''updatedb'' is usually run daily by cron to update the default database
==== Show disk and disk partion detail information ====
<code>
sudo parted -s /dev/sda unit mb print free

#OUTPUT
hemanta@hemanta:~$ sudo parted -s /dev/sda unit mb print free
Model: ATA TOSHIBA MQ01ACF0 (scsi)
Disk /dev/sda: 500108MB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start     End       Size      File system     Name  Flags
       0.02MB    1.05MB    1.03MB    Free Space
1      1.05MB    1000MB    999MB     fat32                 boot, esp
2      1000MB    121000MB  120000MB  ext4
3      121000MB  361001MB  240000MB  ext4
4      361001MB  491001MB  130000MB  ext4
5      491001MB  500107MB  9106MB    linux-swap(v1)
       500107MB  500108MB  1.06MB    Free Space
</code>
==== MAC OS x11 terminal forwarding issue ====
Ref: [[https://discussions.apple.com/thread/1058045?start=0&tstart=0]],[[https://dyhr.com/2009/09/05/how-to-enable-x11-forwarding-with-ssh-on-mac-os-x-leopard/]],[[https://www.xquartz.org/]]

  * set ''x11forwarding yes'' in file ''/etc/ssh/sshd_config''
  * Install ''XQuartz'' and restart the system
  * Now try ''ssh -X" to login remote server
==== How to Find and Kill All Zombie Processes ====
[[https://www.servernoobs.com/how-to-find-and-kill-all-zombie-processes/|Ref:]]
On Unix operating systems, a **zombie process or defunct process** is a process that has completed execution but still has an entry in the process table, allowing the process that started it to read its exit status. It almost always means that the parent is still around. If the parent exited, the child would be orphaned and re-parented to init, which would immediately perform the wait(). In other words, they should go away once the parent process is done.

A zombie process doesn’t react to signals.
== Find out Zombie process ==
<code>ps aux |grep "defunct"</code>
OR
<code>ps aux |grep Z</code>
== List the PID of Zombie ==
<code>ps aux | awk '{ print $8 " " $2 }' | grep -w Z</code>
In order to kill these processes, you need to find the parent process first
<code>pstree -paul
kill -9 <<parent process ID>></code>
==== Kill all processes which matching the string pattern ====
kill al process running by **hemanta**
string pattern: **hemanta**
<code>
ps -ef | grep 'hemanta' | grep -v grep | awk '{print $2}' | xargs -r kill -9
</code>
==== MAC OS fortran compliler installation ====
[[https://www.webmo.net/support/fortran_osx.html|Ref]]
