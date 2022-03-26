# Disable IPv6 module on CentOS
* Just put this into "/etc/sysctl.conf" file.
  * net.ipv6.conf.all.disable_ipv6 = 1
  * net.ipv6.conf.default.disable_ipv6 = 1
