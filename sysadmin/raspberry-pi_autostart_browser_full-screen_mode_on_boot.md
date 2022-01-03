==== Configure Raspberry Pi device for autostart web browser in full-screen mode ====
=== Install lightweight web browser tool ===
Raspberry Pi required a lightweight web browser, here we are using **firefox ESR** for Debian
<code>
# Install firefox esr
sudo add-apt-repository ppa:mozillateam/ppa
sudo apt-get update
sudo apt-get install firefox-esr
</code>
<note tip>If ''add-apt-repository'' command not found then install following packages [[http://learn.linksprite.com/pcduino/linux-applications/how-to-fix-error-sudo-add-apt-repository-command-not-found/|Ref]]
<code>
apt-get update
apt-get install software-properties-common
apt-get install apt-file && apt-file update
</code>
</note>
=== Install xdotool tool ===
**xdotool** helps to run keyboard input through a shell script. With **xdotool** input from the mouse and keyboard very easily
<code>
# Install xdotool
sudo apt-get install xdotool
</code>
=== Develop a shell script to web browser in full screen mode ===
Below shell script developed to run firefox page in fullscreen mode for Nagios monitor web page
<code>
nano /home/pi/nagio_monitor.sh
</code>
<file bash nagio_monitor.sh>
#!/bin/bash
firefox -url "http://nagios.myorg.res.in/nagios/cgi-bin/status.cgi?hostgroup=all&style=summary" & xdotool search --sync --onlyvisible --class "firefox" windowactivate key F11
while true; do
  xdotool key F5
  sleep 30
done
</file>
<note tip>To use Chromium web browser instands of Mozila Firefox; replace **firefox** in above script by **chromium-browser** </note>
Change the above shell script to execute mode
<code>
chmod +x nagios_monitor.sh
</code>
=== Configure Raspberry Pi to run above script on reboot ===
Add above created shell script (here, **nagio_monitor.sh**) with following command, into **./config/lxsession/LXDE-pi/autostart** OR **/etc/xdg/lxsession/LXDE-pi/autostart**file as follow
<code>
nano .config/lxsession/LXDE-pi/autostart
OR
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

@xset s off
@xset -dpms
@xset s noblank
@sh /home/pi/nagio_monitor.sh
</code>
=== Resolve Dell TV resolution issue ===
<color #ed1c24>ISSUE:</color> Not getting full screen (resolution) <color #22b14c>RESOLVE:</color> [[https://stackoverflow.com/questions/22891235/how-to-change-screen-resolution-of-raspberry-pi|ref]], Add the follwing line(s) into **/boot/config.txt** file and restart the Raspberry Pi device as follow
<code>
nano /boot/config.txt

# full screen (resolution) By hemanta
resolution 82   1920x1080   60Hz    1080p
hdmi_ignore_edid=0xa5000080
hdmi_force_hotplug=1
hdmi_boost=7
hdmi_group=2
hdmi_mode=82
hdmi_drive=1
</code>
