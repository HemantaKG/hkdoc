# Installtion of 'zfs' filesystem on CentOS

Install epel-release, Update OS
```bash
yum install epel-release
yum update
```
disable 'SeLinux' and reboot the server
- disable selinux
- reboot system
 
# Installation a zfs-release package
NOTE: Support CentOS version and Architecture
- EL Releases: 6.x, 7.x
- Architectures: x86_64

To simplify installation a **zfs-release package** is provided which includes a **zfs.repo configuration file** and the ZFS on **Linux public signing key**. All official ZFS on Linux packages are signed using this key, and by default yum will verify a package's signature before allowing it be to install. Users are strongly encouraged to verify the authenticity of the ZFS on Linux public key using the fingerprint listed here.

- Location: /etc/pki/rpm-gpg/RPM-GPG-KEY-zfsonlinux
- [EL6 Package](http://download.zfsonlinux.org/epel/zfs-release.el6.noarch.rpm)
- [EL7.3 Package](http://download.zfsonlinux.org/epel/zfs-release.el7_3.noarch.rpm)
- [EL7.4 Package](http://download.zfsonlinux.org/epel/zfs-release.el7_4.noarch.rpm)
- [EL7.5 Package](http://download.zfsonlinux.org/epel/zfs-release.el7_5.noarch.rpm)
- Download from: pgp.mit.edu
- Fingerprint: C93A FFFD 9F3F 7B03 C310 CEB6 A9D5 A1C0 F14A B620

```bash
sudo yum install http://download.zfsonlinux.org/epel/zfs-release.<dist>.noarch.rpm
gpg --quiet --with-fingerprint /etc/pki/rpm-gpg/RPM-GPG-KEY-zfsonlinux
```

Note: After installing the zfs-release package and verifying the public key users have the following options to install zfs on storage server; either the **kABI-tracking kmod** or **DKMS style packages** follow one as per your requirement;

- [kABI-tracking kmod packages](http://elrepoproject.blogspot.in/2016/02/kabi-tracking-kmod-packages.html) are recommended in order to avoid needing to rebuild ZFS for every kernel update
- [DKMS](https://en.wikipedia.org/wiki/Dynamic_Kernel_Module_Support) packages are recommended for users running a non-distribution kernel or for users who wish to apply local customizations to ZFS on Linux

# Install by kABI-tracking kmod (Method 1)*
By default, the zfs-release package is configured to install DKMS style packages so they will work with a wide range of kernels. In order to install the kABI-tracking kmods the default repository in the /etc/yum.repos.d/zfs.repo file must be switch from zfs to zfs-kmod. Keep in mind that the kABI-tracking kmods are only verified to work with the distribution provided kernel.

```bash
nano /etc/yum.repos.d/zfs.repo
```
> [zfs]
> name=ZFS on Linux for EL 7 - dkms
> baseurl=http://download.zfsonlinux.org/epel/7/$basearch/
> -enabled=1
> +enabled=0
> metadata_expire=7d
> gpgcheck=1
> gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-zfsonlinux
> @@ -9,7 +9,7 @@
> [zfs-kmod]
> name=ZFS on Linux for EL 7 - kmod
> baseurl=http://download.zfsonlinux.org/epel/7/kmod/$basearch/
> -enabled=0
> +enabled=1
> metadata_expire=7d
> gpgcheck=1
> gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-zfsonlinux
> 

The ZFS on Linux packages can now be installed using yum
```bash
sudo yum install zfs
```

# Install by DKMS (Method 2)
To install DKMS style packages issue the following yum command. Note that it is important to make sure that the matching kernel-devel package is installed for the running kernel since DKMS requires it to build ZFS.

```bash
sudo yum install kernel-devel zfs
```

# Creating a zpool
## List all disks
```bash
lsblk
ls -l /dev/disk/by-id/*
```
## Making disks 'gpt' support
```bash
parted /dev/disk/by-id/wwn-0x5000c5008572b443 mklabel gpt
parted /dev/disk/by-id/wwn-0x5000c5008574a913 mklabel gpt
```
Note: do for all **>= 2TB** storage disks

## zpool create
Name: jbod1
ZRAID Type: raidz
No of disks: 10

```bash
zpool create -m none -o ashift=12 jbod1 raidz /dev/disk/by-id/wwn-0x5000c5008572b443 /dev/disk/by-id/wwn-0x5000c5008574a913 /dev/disk/by-id/wwn-0x5000c5008574ac3b /dev/disk/by-id/wwn-0x5000c5008572601f /dev/disk/by-id/wwn-0x5000c500857087c7 /dev/disk/by-id/wwn-0x5000c50085726e73 /dev/disk/by-id/wwn-0x5000c50085728763 /dev/disk/by-id/wwn-0x5000c5008572677f /dev/disk/by-id/wwn-0x5000c5008572962f /dev/disk/by-id/wwn-0x5000c50085727e97
```

Note: here the zpool name is **jbod1**, change as per your zpool name

## Add hot-spares
No of spare: 2

```bash
zpool add jbod1 spare /dev/disk/by-id/wwn-0x5000c50085724d67 /dev/disk/by-id/wwn-0x5000c50085726ddb
```

## Add log and cache drive
```bash
zpool add jbod1 cache /dev/disk/by-id/wwn-0x50025388401ea3c0
zpool add jbod1 log /dev/disk/by-id/wwn-0x50025388401cdf6d
```

# Modifiy zpool properties
**set 'autoreplace= on'** 
[Referance](http://docs.oracle.com/cd/E19253-01/819-5461/6n7ht6r00/index.html)

```bash
zpool get all jbod1
zpool set autoreplace=on jbod1
```

# Create zfs dataset and mount
[Create zfs dataset and mount]()

#Reference
* Ref: [ZFS on Linux project Documentation](https://github.com/zfsonlinux/zfs/wiki/RHEL-%26-CentOS), check **RHEL and CentOS** in **Pages list**
* [zfs, zpool Management and troubleshoting]()
