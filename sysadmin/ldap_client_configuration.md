===== LDAP client configuration on CentOS =====
==Install the following packages on client system==
<code>
yum install openldap-clients.x86_64
yum install nss-pam-ldapd
</code>
After successful installation of above packages run the below statement to enable LDAP authentication and auto create user home directory
<code>
authconfig --enableldap --enableldapauth --ldapserver=ldap.myorg.res.in --ldapbasedn="dc=myorg,dc=res,dc=in" --enablemkhomedir --update
</code>
restart nslcd service
<code>
systemctl restart nslcd
</code>
==Check LDAP configuration==
<code>
getent passwd
</code>
==Disable LDAP Authentication in Linux==
<code>
authconfig --disableldapauth --disableldap --enableshadow --updateall
</code>
===== LDAP Client configuration on Ubuntu 16.04 =====
Install LDAP client packages on client system. 
During the installation, the package installer will ask you a variety of questions. Enter the values according to your environment.
<code>
apt-get -y install libnss-ldap libpam-ldap ldap-utils nscd

#give your LDAP server’s IP address or hostname
give your LDAP server hostname (or) server ip [ldap://ldap.myorg.res.in]

#enter the DN (Domain Name) of the LDAP search base
give your DN of LDAP search [dc=myorg,dc=res,dc=in]

#choose the LDAP version to use
choose version [3]

#decide whether the LDAP administrative account can act as a local root
choose [NO]

LDAP db login
choose [NO]
</code>
==== Configure "nsswitch.conf" to work with LDAP ====
open **nsswitch.conf** file and modify as follow
<code>
vim /etc/nsswitch.conf
  passwd:         compat ldap
  group:          compat ldap
  shadow:         compat ldap
</code>
if you want the home directory of the user to be created automatically, then add the following line at the end of **/etc/pam.d/common-session** file 
<code>
vim /etc/pam.d/common-session
  session required        pam_mkhomedir.so skel=/etc/skel umask=077
</code>
restart nscd service to apply all changes to ldap client
<code>
service nscd restart
</code>
==Test LDAP client==
<code>
getent passwd it
getent passwd hemanta.kumar
</code>
[[https://www.itzgeek.com/how-tos/linux/ubuntu-how-tos/configure-ldap-client-on-ubuntu-16-04-debian-8.html|Ref]]
