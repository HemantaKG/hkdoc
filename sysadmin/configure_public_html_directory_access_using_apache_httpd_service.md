==== Configure public_html directory access using apache/httpd service ====
==== Install Apache service ====
Intall Apache service
<code>
#on Redhat/CentOS
yum install httpd

#on Debian/Ubuntu OS
apt-get install apache2
</code>
==== Enable apache2 module and restart apache2 service ====
enable "userdir" apache2 module to access ~/public_html directory
<code>
a2enmod userdir
systemctl restart apache2
</code>
==== Create public_html directory under user home ====
<code>
mkdir ~/public_html
chmod -R 755 ~/public_html
</code>
==== Advance conf ====
To password propect the **public_html** directory: [[password_protect_the_public_html_directory_access_using_apache_httpd_service|Password protect the public_html directory access using apache/httpd service]]