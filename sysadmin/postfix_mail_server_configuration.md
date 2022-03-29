# Mail Server Installation
## Install "postfix" mail server
### Debian and Ubuntu
````
apt-get install postfix
apt-get install mailutils

cp /usr/share/postfix/main.cf.debian /etc/postfix/main.cf
````

### CentOS
````
yum install postfix
````

## Add/modifi relayhost
modify /etc/postfix/main.cf file as
````
nano /etc/postfix/main.cf
relayhost = [smtp.myorg.res.in]
````

## Postfix service restart and status check
````
systemctl restart postfix.service
systemctl status postfix.service
````

## Delete all mails present in postfix mailq
````
postsuper -d ALL
````

## Send a test mail from command line
````
echo "THIS IS A TEST EMAIL" | mail -s "Enter the subject" <<email id>>
````

## Troubleshooting
* Check network insterface "GATEWAY"
* Check "/etc/resolv.conf" file

REF: [[https://www.interserver.net/tips/kb/linux-mail-command-usage-examples/| send test mail example]]
