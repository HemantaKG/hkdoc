===== GPG error, signatures couldn't be verified because the public key is not available =====
==== Solution 1 ====
==apt update fails with error==
    W: GPG error: https://ftp.iitm.ac.in/cran/bin/linux/ubuntu xenial/ InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 51716619E084DAB9
    E: The repository 'https://ftp.iitm.ac.in/cran/bin/linux/ubuntu xenial/ InRelease' is not signed.
resolved as:
    root@icts:~# gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E084DAB9
    gpg: requesting key E084DAB9 from hkp server keyserver.ubuntu.com
    gpg: key E084DAB9: "Michael Rutter <marutter@gmail.com>" not changed
    gpg: Total number processed: 1
    gpg:              unchanged: 1
    root@icts:~# gpg -a --export E084DAB9 | sudo apt-key add -
    OK
==== Solution 2 ====
==fails with error==
    W: GPG error: http://software.ligo.org jessie InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY CE050D236DB6FA3F
resolve as:
    NOTE: install the following package 
    apt-get install debian-keyring
    
    NOTE: run the following by changing the "key-value"
    gpg --keyserver pgp.mit.edu --recv-keys 670079F6
    gpg --armor --export 670079F6 | apt-key add -