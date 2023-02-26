# Configure public_html directory access using apache/httpd service ====
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
