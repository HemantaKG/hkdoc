==== Install Mail Server ====
=== Install "postfix" mail server ===
== Debian and Ubuntu: ==
<code>
apt-get install postfix
apt-get install mailutils
</code>
<code>
cp /usr/share/postfix/main.cf.debian /etc/postfix/main.cf
</code>
== CentOS: ==
<code>
yum install postfix
</code>
==== Add/modifi relayhost ====
Add/modify /etc/postfix/main.cf file as
<code>
nano /etc/postfix/main.cf
relayhost = [smtp.myorg.res.in]
</code>

==== Postfix service restart and status check ====
<code>
systemctl restart postfix.service
systemctl status postfix.service
</code>
==== Delete all mails present in postfix mailq ====
<code>
postsuper -d ALL
</code>
==== Send a test mail from command line ====
<code>
echo "THIS IS A TEST EMAIL" | mail -s "Enter the subject" <<email id>>
</code>
REF: [[https://www.interserver.net/tips/kb/linux-mail-command-usage-examples/| send test mail example]]
