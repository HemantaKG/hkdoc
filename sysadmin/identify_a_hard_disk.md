==== How to identify HDD disk? ====
The following set of commands help you to identify hard disk by blinking LED indicator of the hard disk. (hardware dependent command, may not support some hardware)
<code>
#to blink LED of disk "sdl"
ledctl locate=/dev/sdl

#to stop LED blink of disk "sdl"
ledctl locate_off=/dev/sdl
ledctl  off=/dev/sdl
</code>
==== HDD Property Details ====
REF: [[https://pthree.org/2012/12/11/zfs-administration-part-vi-scrub-and-resilver/]]
<code>
# to get details of HDD "sda"
hdparm -I /dev/sda
</code>