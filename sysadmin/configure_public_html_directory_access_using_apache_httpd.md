# "public_html" directory access using apache/httpd
## Install Apache server
Intall Apache web server
````
#on Redhat/CentOS
yum install httpd

#on Debian/Ubuntu OS
apt-get install apache2
````

## Enable apache2 module and restart apache2 service
enable "userdir" apache2 module to access ~/public_html directory
````
a2enmod userdir
systemctl restart apache2
````

## Create "public_html" directory under user "home"
````
mkdir ~/public_html
chmod -R 755 ~/public_html
````
# Advance configurations
To password propect the **public_html** directory
# Password protect the public_html directory access using apache/httpd
## Create a password file with htpasswd command
Create a **username** and **passwd** to protect the **public_html** directory; by using apache ''htpasswd'' command
````
htpasswd -c /etc/security/.htpasswd totouser
````
NOTE: here the username is "totouser"

## Configure Apache to allow .htaccess access
Add following line into "Directory" tag under "userdir.conf" file.
- For Redhat/CentOS system **/etc/httpd/conf.d/userdir.conf** file
- For Debian/Ubuntu system **/etc/apache2/mods-enabled/userdir.conf** file

````
<Directory "/home/*/Public">
...
...
AuthType Basic
AuthGroupFile /dev/null
AuthName "Restricted Content"
AuthUserFile /etc/security/.htpasswd
Require valid-user
</Directory>
````
# Configure Apache password authentication
- you need to create a ''.htaccess'' file in the web directory you wish to restrict
- Add the following content
````
AuthType Basic
AuthGroupFile /dev/null
AuthName "Restricted Content"
AuthUserFile /etc/security/.htpasswd
Require valid-user
````
## Enable apache modules
You need to enable "authz_groupfile" apache module. Otherwise apache restart will fail with an error message <color #ed1c24>**Invalid command 'AuthGroupFile', perhaps misspelled or defined by a module not included in the server configuration**</color>
````
a2enmod authz_groupfile
````
## Restart Apache service and test
````
#on Redhat/CentOS
apachectl restart

#on Ubuntu/Debian OS
systemctl restart apache2
````
## Referance
- https://devops.profitbricks.com/tutorials/set-up-basic-authentication-in-apache-using-htaccess-on-centos-7
- https://www.cyberciti.biz/faq/howto-setup-apache-password-protect-directory-with-htaccess-file
