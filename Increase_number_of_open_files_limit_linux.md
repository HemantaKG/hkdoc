# How to Increase Number of Open Files Limit in Linux

## Method 01
Please follow the steps to increase the open file limit at user level.

### step01: 
Create a new file _/etc/security/limits.d/30-nofile.conf_ with these contents **to set global limits**
> nano /etc/security/limits.d/30-nofile.conf
```
[Manager]
DefaultLimitNOFILE=2097152
```
### step02:
Add the following lines in _/etc/security/limits.conf_ to **apply limits per user**
> nano /etc/security/limits.conf
```
...
# user level
hemanta.kumar    hard    nofile          1048576
vaishak.p        hard    nofile          1048576
# group level
@pdf        hard    nofile          1048576
...
```
NOTE:
- Users will need to logout and login again for the changes to take effect.
- If you want to apply the limit immediately, you can use the following command:
```
sysctl -p
```
---
## Method 02
---

# How to set and check the user level hard and soft limits
If you want to see the hard and soft limits, you can use the following commands:
### set Hard and Soft limits
```
ulimit -n 1048576
```
### Check Hard Limit in Linux
```
ulimit -Hn
```
### Check Soft Limits in Linux
```
ulimit -Sn
```
