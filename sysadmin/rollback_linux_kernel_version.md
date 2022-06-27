SDI, RAID, and IB hardware drivers of the BMS are related to the kernel. You are not advised to upgrade the kernel version.
If you have upgraded the kernel, perform the operations in this section to rollback to older working kernel version.

# Legacy BIOS boot or Non "efi" boot
### List all old kernel available on the server
````
awk -F\' '$1=="menuentry " {print $2}' /etc/grub2.cfg
OR 
cat /boot/grub2/grub.cfg |grep menuentry
````
### select the working kernel version and set as default
NOTE: in above list the kernal indez are 0,1,2,...
````
grub2-set-default 2
````
### Build the grud file and reboot the server
````
grub2-mkconfig -o /boot/grub2/grub.cfg
reboot
````
----

# UEFI boot or "efi" boot server
### All old kernel available on the server
````
cat /boot/efi/EFI/centos/grub.cfg |grep menuentry
````
### select the working kernel version and set as default and check and reboot
````
grub2-set-default "CentOS Linux (3.10.0-327.el7.x86_64) 7 (Core)"
grub2-editenv list
reboot
````
