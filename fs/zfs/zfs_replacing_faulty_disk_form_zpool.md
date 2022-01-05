# Faulty disk repalce and detach from zpool

Follow the steps to detach the faulty disk
- check zpool health
- replace the faulty disk with space disk
- let the **resilver process** complete
- detach the faulty disk after **resilver process** complete

## step0: 
Note: zpool status degraded
zpool status showing pool "jbod1" DEGRADED, due to one of the disk UNAVAIL "wwn-0x5000c5008574ac3b"
```bash
zpool status -x
```

	  pool: jbod1
	 state: DEGRADED
	status: One or more devices could not be used because the label is missing or
		invalid.  Sufficient replicas exist for the pool to continue
		functioning in a degraded state.
	action: Replace the device using 'zpool replace'.
		 see: http://zfsonlinux.org/msg/ZFS-8000-4J
		scan: resilvered 17.1M in 0h0m with 0 errors on Tue Jun 20 11:47:49 2017
	config:
		NAME                        STATE     READ WRITE CKSUM
		jbod1                       DEGRADED     0     0     0
			raidz1-0                  DEGRADED     0     0     0
			  wwn-0x5000c5008572b443  ONLINE       0     0     0
			  wwn-0x5000c5008574a913  ONLINE       0     0     0
			  wwn-0x5000c5008574ac3b  UNAVAIL      0     0     0
			  wwn-0x5000c5008572601f  ONLINE       0     0     0
			  wwn-0x5000c500857087c7  ONLINE       0     0     0
			  wwn-0x5000c50085726e73  ONLINE       0     0     0
			  wwn-0x5000c50085728763  ONLINE       0     0     0
			  wwn-0x5000c50085726ddb  ONLINE       0     0     0
			  wwn-0x5000c5008572962f  ONLINE       0     0     0
			  wwn-0x5000c50085727e97  ONLINE       0     0     0
		logs
			wwn-0x50025388401cdf6d    ONLINE       0     0     0
		cache
			wwn-0x50025388401ea3c0    ONLINE       0     0     0
		spares
			wwn-0x5000c50085724d67    AVAIL   
			wwn-0x5000c5008590b16f    AVAIL   


## step1: Replace the UNAVAIL disk by spare disk "wwn-0x5000c50085724d67"
```bash
zpool replace jbod1 /dev/disk/by-id/wwn-0x5000c5008574ac3b /dev/disk/by-id/wwn-0x5000c50085724d67
```

## step2: Resilver in progress, it will take some time to resilver 8.87T data, wait for resilver process complete
```bash
zpool status -x
```

	pool: jbod1
	 state: DEGRADED
	status: One or more devices is currently being resilvered.  The pool will
		continue to function, possibly in a degraded state.
	action: Wait for the resilver to complete.
		scan: resilver in progress since Tue Jan 23 14:13:21 2018
		  306M scanned out of 8.87T at 34.0M/s, 76h2m to go
		  30.2M resilvered, 0.00% done
	config:
		NAME                          STATE     READ WRITE CKSUM
		jbod1                         DEGRADED     0     0     0
			raidz1-0                    DEGRADED     0     0     0
			  wwn-0x5000c5008572b443    ONLINE       0     0     0
			  wwn-0x5000c5008574a913    ONLINE       0     0     0
			  spare-2                   UNAVAIL      0     0     0
			    wwn-0x5000c5008574ac3b  UNAVAIL      0     0     0
			    wwn-0x5000c50085724d67  ONLINE       0     0     0  (resilvering)
			  wwn-0x5000c5008572601f    ONLINE       0     0     0
			  wwn-0x5000c500857087c7    ONLINE       0     0     0
			  wwn-0x5000c50085726e73    ONLINE       0     0     0
			  wwn-0x5000c50085728763    ONLINE       0     0     0
			  wwn-0x5000c50085726ddb    ONLINE       0     0     0
			  wwn-0x5000c5008572962f    ONLINE       0     0     0
			  wwn-0x5000c50085727e97    ONLINE       0     0     0
		logs
			wwn-0x50025388401cdf6d      ONLINE       0     0     0
		cache
			wwn-0x50025388401ea3c0      ONLINE       0     0     0
		spares
			wwn-0x5000c50085724d67      INUSE     currently in use
			wwn-0x5000c5008590b16f      AVAIL   
	errors: No known data errors


## step3: Resilver process compleated 
```bash
zpool status -x
```

	  pool: jbod1
	 state: DEGRADED
	status: One or more devices could not be used because the label is missing or
		invalid.  Sufficient replicas exist for the pool to continue
		functioning in a degraded state.
	action: Replace the device using 'zpool replace'.
		 see: http://zfsonlinux.org/msg/ZFS-8000-4J
		scan: resilvered 908G in 6h0m with 0 errors on Tue Jan 23 20:13:31 2018
	config:
		NAME                          STATE     READ WRITE CKSUM
		jbod1                         DEGRADED     0     0     0
			raidz1-0                    DEGRADED     0     0     0
			  wwn-0x5000c5008572b443    ONLINE       0     0     0
			  wwn-0x5000c5008574a913    ONLINE       0     0     0
			  spare-2                   UNAVAIL      0     0     0
			    wwn-0x5000c5008574ac3b  UNAVAIL      0     0     0
			    wwn-0x5000c50085724d67  ONLINE       0     0     0
			  wwn-0x5000c5008572601f    ONLINE       0     0     0
			  wwn-0x5000c500857087c7    ONLINE       0     0     0
			  wwn-0x5000c50085726e73    ONLINE       0     0     0
			  wwn-0x5000c50085728763    ONLINE       0     0     0
			  wwn-0x5000c50085726ddb    ONLINE       0     0     0
			  wwn-0x5000c5008572962f    ONLINE       0     0     0
			  wwn-0x5000c50085727e97    ONLINE       0     0     0
		logs
			wwn-0x50025388401cdf6d      ONLINE       0     0     0
		cache
			wwn-0x50025388401ea3c0      ONLINE       0     0     0
		spares
			wwn-0x5000c50085724d67      INUSE     currently in use
			wwn-0x5000c5008590b16f      AVAIL   
	errors: No known data errors


## step4: Detach faulty disk
```bash
zpool detach jbod1 /dev/disk/by-id/wwn-0x5000c5008574ac3b
```

## step5: Check zpool status for healthy
```bash
zpool status -x
```
> all pools are healthy

```bash
zpool status
```
	  pool: jbod1
	 state: ONLINE
		scan: resilvered 908G in 6h0m with 0 errors on Tue Jan 23 20:13:31 2018
	config:
		NAME                        STATE     READ WRITE CKSUM
		jbod1                       ONLINE       0     0     0
			raidz1-0                  ONLINE       0     0     0
			  wwn-0x5000c5008572b443  ONLINE       0     0     0
			  wwn-0x5000c5008574a913  ONLINE       0     0     0
			  wwn-0x5000c50085724d67  ONLINE       0     0     0
			  wwn-0x5000c5008572601f  ONLINE       0     0     0
			  wwn-0x5000c500857087c7  ONLINE       0     0     0
			  wwn-0x5000c50085726e73  ONLINE       0     0     0
			  wwn-0x5000c50085728763  ONLINE       0     0     0
			  wwn-0x5000c50085726ddb  ONLINE       0     0     0
			  wwn-0x5000c5008572962f  ONLINE       0     0     0
			  wwn-0x5000c50085727e97  ONLINE       0     0     0
		logs
			wwn-0x50025388401cdf6d    ONLINE       0     0     0
		cache
			wwn-0x50025388401ea3c0    ONLINE       0     0     0
		spares
			wwn-0x5000c5008590b16f    AVAIL   
	errors: No known data errors

## Disk fault analysis: What? and Where?
We can analyze the disk in the following ways
- check the system recorded hardware log at **/var/log/syslog** and **/var/log/messages**
- Using [smartctl](disk_health_check_using_smartctl) tool to detail analysis of disk

## Referance
- [scrub and resilver](https://pthree.org/2012/12/11/zfs-administration-part-vi-scrub-and-resilver/)
