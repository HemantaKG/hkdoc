==== Password protect the public_html directory access using apache/httpd service ====
Ref: [[https://devops.profitbricks.com/tutorials/set-up-basic-authentication-in-apache-using-htaccess-on-centos-7/|Ref1]], [[https://www.cyberciti.biz/faq/howto-setup-apache-password-protect-directory-with-htaccess-file/|Ref2]]
==== Create a password file with htpasswd command ====
Create a **username** and **passwd** to protect the **public_html** directory; by using apache ''htpasswd'' command
<code>
htpasswd -c /etc/security/.htpasswd totouser
</code>
NOTE: here the username is "totouser"
==== Configure Apache to allow .htaccess access ====
Add following line(s) of statementes under the **<Directory>** tag block of **userdir.conf** file; (NOTE: file location variy on OS)
  * For Redhat/CentOS system **/etc/httpd/conf.d/userdir.conf** file
  * For Debian/Ubuntu system **/etc/apache2/mods-enabled/userdir.conf** file
<code>
<Directory "/home/*/Public">
...
...
AuthType Basic
AuthGroupFile /dev/null
AuthName "Restricted Content"
AuthUserFile /etc/security/.htpasswd
Require valid-user
</Directory>
</code>
==== Configure Apache password authentication ====
  * you need to create a ''.htaccess'' file in the web directory you wish to restrict
  * Add the following content
<code>
AuthType Basic
AuthGroupFile /dev/null
AuthName "Restricted Content"
AuthUserFile /etc/security/.htpasswd
Require valid-user
</code>
==== Enable apache modules ====
You need to enable "authz_groupfile" apache module. Otherwise apache restart will fail with an error message <color #ed1c24>**Invalid command 'AuthGroupFile', perhaps misspelled or defined by a module not included in the server configuration**</color>
<code>
a2enmod authz_groupfile
</code>
==== Restart Apache service and test ====
<code>
#on Redhat/CentOS
apachectl restart

#on Ubuntu/Debian OS
systemctl restart apache2
</code>