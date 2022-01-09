## Login and Register
Login to [[http://registrationcenter.intel.com|intel registration center]] and register your serial key [key looks like xxxx-xxxxxxxx]
Download the required Intel Parallel Studio package. NOTE: offline installation tar file size is around 5TB

## Untar and install
Following below step to install Parallel Studio; NOTE: by default installation directory is **/opt/intel** 
>
>untar the above downloaded package
>
>cd to directory
>
>run **./install_GUI.sh** OR **./install.sh**
>
>press enter
>
>type **accept**
>
>press enter 
>
>press enter [if you have the key]
>
>enter **unique serial key** [key looks like xxxx-xxxxxxxx]
>
>press enter
>
>press enter [enter 1]
>
>press enter
>
>press enter [you may skip 32-bit version, if you using only 64-bit]
>  

## Source PATH
Add the following line into **/etc/bashrc** for Centos (OR) **/etc/bash.bashrc** file for Ubuntu
```bash
source /opt/intel/parallel_studio_xe_2017.4.056/psxevars.sh
```
