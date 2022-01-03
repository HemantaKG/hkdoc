==== Install DokuWiki ====
Ref:[[https://www.dokuwiki.org/install:debian|''dokuWiki installation on Debian]]
    apt-get install php5 libapache2-mod-php5 php5-mcrypt dokuwiki
==== Configur apache access dokuWiki remotely ====
Check and modify ''/etc/apache2/mods-enabled/dir.conf'' file contant as below
    nano /etc/apache2/mods-enabled/dir.conf
    
    <IfModule mod_dir.c>
        DirectoryIndex index.php index.html index.cgi index.pl index.php index.xhtml index.htm
    </IfModule>
Check, add and modify ''/etc/apache2/conf-enabled/dokuwiki.conf'' file content as below
    node /etc/apache2/conf-enabled/dokuwiki.conf
    
    NOTE: Add the following line at top of the file
    <VirtualHost *:80>
    ServerName humpty.alice.icts.res.in
    DocumentRoot /usr/share/dokuwiki/
    
    NOTE: Add the following line at bottom of the file
    </VirtualHost>
    
    NOTE: modify the line "Allow from localhost 127.0.0.1 ::1" as
    Allow from all 
==== Backup and Restore DokuWiki data ====
  * To take back up copy the entire folder ''/var/lib/dokuwiki''
  * To restore from backup just copy above copied ''dokuwiki'' folder to ''/var/lib/dokuwiki'', than change the owner of ''/var/lib/dokuwiki/acl'' and ''/var/lib/dokuwiki/data'' to ''www-data:root''. 
===== REF =====
  * [[https://timothy-quinn.com/building-dokuwiki-on-centos-7/| Ref1]]