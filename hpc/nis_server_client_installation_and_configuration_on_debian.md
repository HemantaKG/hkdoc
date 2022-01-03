===== NIS Server Configuration =====
==== Installation ====
    aptitude -y install nis
    
    NIS domain: server.test
    ok
==== Configure ====
=== modify "/etc/hosts" ===
    nano /etc/hosts
    # master1, condor submit node
    10.0.0.3        slave.server.test        slave
    10.0.0.2        master.server.test        master
=== modify "/etc/yp.conf" ===
    nano /etc/yp.conf
    # ypserver ypserver.network.com
    # SET FOR NIS SERVER
    ypserver master.server.test
    # SET FOR NIS SLAVE AND CLIENTdomain server.test server slave.server.test
    domain server.test server master.server.test
=== modify "/etc/default/nis" ===
    nano /etc/default/nis
    # Are we a NIS server and if so what kind (values: false, slave, master)?
    NISSERVER=master
    # Are we a NIS client?
    NISCLIENT=flase
    # NIS master server.  If this is configured on a slave server then ypinit
    # will be run each time NIS is started.
    NISMASTER=master.server.test
=== modify "/etc/ypserv.securenets" ===
    nano /etc/ypserv.securenets
    # Always allow access for localhost
    255.0.0.0       127.0.0.0
    # This line gives access to everybody. PLEASE ADJUST!
    #0.0.0.0                0.0.0.0
    # IP addresss allow access
    255.255.255.0   10.0.0.0
=== modify "/var/yp/Makefile" ===
    nano /var/yp/Makefile
    # If we have only one server, we don't have to push the maps to the
    # slave servers (NOPUSH=true). If you have slave servers, change this
    # to "NOPUSH=false" and put all hostnames of your slave servers in the file
    # /var/yp/ypservers.
    NOPUSH=false
    #add following line at end
    all:    passwd shadow group hosts rpc services netid protocols
=== modify "/var/yp/ypservers" ===
    nano /var/yp/ypservers
    slave.server.test
=== modify "/etc/nsswitch.conf" ===
    nano /etc/nsswitch.conf
    passwd:         compat nis
    group:          compat nis
    shadow:         compat nis
    hosts:          files dns nis
    networks:       files
    protocols:      db files
    services:       db files
    ethers:         db files
    rpc:            db files
    netgroup:       nis

=== Restart NIS service and make NIS DB ===
== Restart service ==
    /etc/init.d/nis restart
== Build NIS DB ==
    /usr/lib/yp/ypinit -m
    #add list of NIS server host which will run NIS server
    next host to add: master
    next host to add: #push Ctrl+D
    The current list of NIS servers looks like this:
    master
    Is this correct?  [y/n: y]  y
    ...
    ...
=== Final build and puss NIS DB ===
    NOTE: restart is OPTIONAL
    /etc/init.d/nis restart
    
    NOTE: do below step for final congif...
    cd /var/yp
    make
===== NIS Slave Configuration =====
==== Installation ====
    aptitude -y install nis
    NIS domain: server.test
    ok
==== Configure ====
=== "/etc/hosts" ===
    nano /etc/hosts
    # master1, condor submit node
    10.0.0.3        slave.server.test        slave
    10.0.0.2        master.server.test        master
=== modify "/etc/yp.conf" ===
    nano /etc/yp.conf
    #SET FOR NIS SLAVE AND CLIENT
    domain server.test server master.server.test
    domain server.test server slave.server.test
=== modify "/etc/default/nis" ===
    nano /etc/default/nis
    # Are we a NIS server and if so what kind (values: false, slave, master)?
    NISSERVER=slave
    # Are we a NIS client?
    NISCLIENT=true
    # NIS master server.  If this is configured on a slave server then ypinit
    # will be run each time NIS is started.
    NISMASTER=master.server.test
=== modify "/etc/ypserv.securenets" ===
    nano /etc/ypserv.securenets
    # Always allow access for localhost
    255.0.0.0       127.0.0.0
    # This line gives access to everybody. PLEASE ADJUST!
    0.0.0.0 0.0.0.0
    # IP addresss allow access
    #255.255.255.0  10.0.0.0
=== modify "/var/yp/Makefile" ===
    nano /var/yp/Makefile
    # If we have only one server, we don't have to push the maps to the
    # slave servers (NOPUSH=true). If you have slave servers, change this
    # to "NOPUSH=false" and put all hostnames of your slave servers in the file
    # /var/yp/ypservers.
    NOPUSH=true
    # add following line at end
    all:    passwd shadow group hosts rpc services netid protocols
=== modify "/etc/nsswitch.conf" ===
    nano /etc/nsswitch.conf
    passwd:         compat nis
    group:          compat nis
    shadow:         compat nis
    hosts:          nis files dns
    networks:       files
    protocols:      db files
    services:       db files
    ethers:         db files
    rpc:            db files
    netgroup:       nis db file
==== Restart ====
    /etc/init.d/nis restart
===== NIS Client Configuration =====
==== Installation ====
    aptitude -y install nis
==== Configure ====
=== modify "/etc/yp.conf" ===
    nano /etc/yp.conf
    # ypserver ypserver.network.com
    # add NIS server's hostname
    # add at the last: (domain name) (server) (NIS server's hostname)
    domain server.test server master.server.test
    domain server.test server slave.server.test
=== modify "/etc/ypserv.securenets" ===
    nano /etc/ypserv.securenets
    # Always allow access for localhost
    255.0.0.0       127.0.0.0
    # This line gives access to everybody. PLEASE ADJUST!
    0.0.0.0         0.0.0.0
=== modify "/etc/default/nis" ===
    nano /etc/default/nis
    # Are we a NIS server and if so what kind (values: false, slave, master)?
    NISSERVER=false
    # Are we a NIS client?
    NISCLIENT=true
=== modify "/var/yp/Makefile" ===
    nano /var/yp/Makefile
    # If we have only one server, we don't have to push the maps to the
    # slave servers (NOPUSH=true). If you have slave servers, change this
    # to "NOPUSH=false" and put all hostnames of your slave servers in the file
    # /var/yp/ypservers.
    NOPUSH=true
   # add following line at end
   all:    passwd shadow group hosts rpc services netid protocols
=== modify "/etc/nsswitch.conf" ===
    nano /etc/nsswitch.conf
    passwd:         compat nis
    group:          compat nis
    shadow:         compat nis
    # hosts:          files myhostname mdns4_minimal [NOTFOUND=return] dns mdns4
    hosts:          files dns nis
    networks:       files
    protocols:      db files
    services:       db files
    ethers:         db files
    rpc:            db files
    netgroup:       nis
==== Restart ====
    /etc/init.d/nis restart
===== Test NIS =====
Do at ''comput-node''
    ypwhich
    master.server.test

    ypcat passwd

    ypcat group

    ypcat hosts
    127.0.1.1
    127.0.0.1
    10.0.0.1        server.test
===== Rebuild NIS DB =====
Rebuild the ''nis DB'' whenever a ''new user'' added
    make -C /var/yp
===== Referance =====
  * [[http://www.linux-nis.org/doc/nis.debian.howto]]
  * [[https://www.server-world.info/en/note?os=Debian_8&p=nis&f=3]]
