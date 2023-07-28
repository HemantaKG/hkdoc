# NagiOS3 installation and configuration
## install NagiOS3:
````
apt-get instal nagios
````
NOTE: *give a strong password

## Configure NagiOS3 to monitor resources:
create "cluster-nagios.cfg" file and resource properties:
````
nano /etc/nagios3/conf.d/cluster-nagios.cfg 

#Add all node details in the following format:
    define host {
            host_name   HOSTNAME
            alias       ALIAS
            address     IP
            use         generic-host
            check_command    
            _ipmi_ip    IPMI IP
    }
````
## Edit 'contacts_nagios2.cfg' to get alert messages:
````
nano /etc/nagios3/conf.d/contacts_nagios2.cfg
    email    <<your email id>>
````

## Edit 'hostgroups_nagios2.cfg' to add all hosts you want to monitor using NagiOS:
````
nano /etc/nagios3/conf.d/hostgroups_nagios2.cfg
    # A list of your Master servers
    define hostgroup {
        hostgroup_name  Master-nodes
                alias           Master Nodes
                members         server1,server2
        }
        
    # A list of your Compute Nodes
    define hostgroup {
        hostgroup_name  Compute-nodes
                alias           Compute Nodes
                members         node001,node002,node003,node004,node005,node006,node007,node008
        }
        
    # A list of your Storage Nodes
    define hostgroup {
        hostgroup_name  Storage-nodes
                alias           Storage Nodes
                members         storage01,archive
        }
        
    # A list of your Condor Manager node i.e. CRM
    define hostgroup {
        hostgroup_name  CRM-nodes
                alias           CRM Nodes
                members         crm
        }
        
    # A list of your IPMI servers exclude
    define hostgroup {
        hostgroup_name  ipmi-servers
                alias           IPMI
                members         *
        }
        
    # A list of your apache web servers
    define hostgroup {
        hostgroup_name  http-servers
                alias           HTTP servers
                members         server1,server2
        }
        
    # A list of your ssh-accessible servers
    define hostgroup {
        hostgroup_name  ssh-servers
                alias           SSH servers
                members         server1,server2
        }
````

## Restart NagiOS service:
````
/etc/init.d/nagios3 restart
````
