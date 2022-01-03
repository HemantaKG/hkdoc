[[https://www.centos.org/forums/viewtopic.php?t=56198|Ref:]]

The **libvirt** has **Default network** configured and auto-started by default.
The **libvirtd.service** is enabled by default.

Thus, if you have **libvirt** installed, then the service is running and on start it has
created those (virtual) interface devices.

The virbr0 (bridge) is like a switch into which you can connect your virtual guests
and your host. The host can act as a router between outside physical subnet and
internal virtual subnet. The router can do NAT (aka masquerade).

You can, on the configuration of **libvirt**, disable the autostart of the Default network.
You can disable **libvirtd.service**, if you don't use it.

Do the following after installation of CentOS on new server:
<code>
ifconfig virbr0 down
systemctl stop libvirtd.service
systemctl disable libvirtd.service
systemctl restart network.service
</code>
Deactivate using xCAT server (on OS provisioned nodes)
<code>
xdsh compute "ifconfig virbr0 down"
xdsh compute "systemctl stop libvirtd.service"
xdsh compute "systemctl disable libvirtd.service"
</code>