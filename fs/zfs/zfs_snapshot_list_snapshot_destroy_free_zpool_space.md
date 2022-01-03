=== List all zfs snapshots in use ===
The following command list all zfs snapshot
<code>
zfs list -t snapshot -S used
</code>
=== destroy zfs snapshot ===
For example you want to destroy the following zfs snapshot **zfs destroy zsp1/home@2019-03-30-000000**
<code>
zfs destroy mariodatapool/home@2018-03-13-000000
</code>