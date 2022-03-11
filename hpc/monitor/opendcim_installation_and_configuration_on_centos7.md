# OpenDCIM Installation and Configuration
## Install "httpd"
````
yum -y install httpd
systemctl enable httpd.service
systemctl start httpd.service
````

## Install "php, php-mysql, php-mbstring, php-snmp"
````
yum -y install php
yum -y install php-mysql
yum -y install php-mbstring
yum -y install php-snmp
````

## Install "mariadb server"
````
yum -y install mariadb-server
systemctl enable mariadb.service
systemctl start mariadb.service

mysql_secure_installation
[just enter y y y y y for all]
````

## Create database
- database name ''dcim'', passwd ''dcimpasswd'' and grant all privileges
````
mysql -u root -p
create database dcim;
grant all privileges on dcim.* to 'dcim' identified by 'dcimpasswd';
exit
````

## Install ssl module for httpd and create self certificate for secure access
- install ssl module
````
yum -y install mod_ssl
````

- Generate self certificate
````
    cd /root
    openssl genrsa -out ca.key 1024
    openssl req -new -key ca.key -out ca.csr
        Country Name (2 letter code) [XX]:IN
        State or Province Name (full name) []:KARNATAKA
        Locality Name (eg, city) [Default City]:BANGALURU
        Organization Name (eg, company) [Default Company Ltd]:<<enter name>>
        Organizational Unit Name (eg, section) []:IT
        Common Name (eg, your name or your server's hostname) []:<<enter name>>
        Email Address []:<<enter email id>>
    
    Please enter the following 'extra' attributes
    to be sent with your certificate request
        A challenge password []:<<enter password>>
        An optional company name []:<<enter name>>
    
    openssl x509 -req -days 365 -in ca.csr -signkey ca.key -out ca.crt
    Signature ok
    subject=/C=IN/ST=KARNATAKA/L=BANGALURU/O=****/OU=IT/CN=****/emailAddress=****
    Getting Private key
````

## Move/Copy to "/etc/pki/tls/*" folder
````
cp ca.crt /etc/pki/tls/certs
cp ca.key /etc/pki/tls/private/ca.key
cp ca.csr /etc/pki/tls/private/ca.csr
````

## Set OpenDCIM server url and create .conf file
````
vim +/ServerName /etc/httpd/conf/httpd.conf
ServerName opendcim.<<change hostname>>:443

systemctl restart httpd.service
````

- Create .conf file as follow
````
vim /etc/httpd/conf.d/opendcim.<<hostname>>.conf
        <VirtualHost *:443>
            SSLEngine On
            SSLCertificateFile /etc/pki/tls/certs/ca.crt
            SSLCertificateKeyFile /etc/pki/tls/private/ca.key
            ServerAdmin ****
            DocumentRoot /opt/openDCIM/opendcim
            ServerName ****
            
            <Directory /opt/openDCIM/opendcim>
                AllowOverride All
                AuthType Basic
                AuthName "openDCIM"
                AuthUserFile /opt/openDCIM/opendcim/.htpasswd
                Require valid-user
            </Directory>
        </VirtualHost>
````

## Add port to firewall
````
firewall-cmd --zone=public --add-port=443/tcp --permanent
firewall-cmd --reload
````

## Untar and configure OpenDCIM
### Make a directory under "/opt" and untar openDCIM tar file
````
mkdir /opt/openDCIM
cd /opt/openDCIM

cp ~/Downloads/openDCIM-4.4.tar.gz .
tar -xzvf openDCIM-4.4.tar.gz

mv openDCIM-4.4 opendcim
cd /opt/openDCIM/opendcim
````

## Remane "db.inc.php-dist" file to "db.inc.php" and edit as follow ===
````
cp db.inc.php-dist db.inc.php
nano db.inc.php

$dbhost = 'localhost';
$dbname = 'dcim';
$dbuser = 'dcim';
$dbpass = 'dcimpassword';
````

## Create OpenDCIM user account as "ADMIN" using htpasswd and restart httpd service
````
touch /opt/openDCIM/opendcim/.htpasswd
htpasswd /opt/openDCIM/opendcim/.htpasswd ADMIN
New password:admindcim
Re-type new password:admindcim

systemctl restart httpd.service
````

## Troubleshooting and Reference
- disable Selinux and reboot system.
- remove "install.php" file from "/opt/openDCIM/opendcim" folder and reloging to opendcim server
- issue01: Upload directory 'drawings' is not writable
- Upload directory 'drawings' is not writable: http://discussion.opendcim.narkive.com/1xgNfPYG/upload-directory-is-not-writable-why

````
chown -R root:apache opendcim
chcon -R -h -t httpd_sys_content_rw_t drawings
chcon -R -h -t httpd_sys_content_rw_t pictures

systemctl restart httpd.service
````
