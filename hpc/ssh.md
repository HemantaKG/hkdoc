===== SSH key share =====
=== General Password less SSH login ===
<code>
ssh-keygen -t rsa
ssh-copy-id <<username>>@<<hostname>>
</code>
=== for non-shared directory ===
<code>
ssh-keygen -t rsa
cat .ssh/id_rsa.pub | ssh root@node* 'cat >> .ssh/authorized_keys'
</code>
=== for shared directory ===
<code>
ssh-keygen -t rsa
cat .ssh/id_rsa.pub >> .ssh/authorized_keys
</code>
===== Allow root access for system using ssh [Ubuntu 16.04] =====
open **sshd_config** file
    vim /etc/ssh/sshd_config
change **PermitRootLogin** property value form **prohibit-password** to **yes** as below in above file
    #PermitRootLogin prohibit-password
    PermitRootLogin yes
[[https://askubuntu.com/questions/951581/how-to-enable-ssh-root-access-ubuntu-16-04/951583|Ref]]
===== Allow only a specific users to ssh into the system [Ubuntu 16.04/CentOS] ===== 
open **sshd_config** file
    vim /etc/ssh/sshd_config
Add below to above file to allow only **root**, **it** and **hemanta.kumar** to ssh into the system
    AllowUsers root it hemanta.kumar
restart ssh service
    service ssh restart
[[https://askubuntu.com/questions/834069/only-allow-one-user-on-system-to-be-sshd-into|Ref]]
===== Allow only a specific group to ssh to the system [Ubuntu 16.04/CentOS] =====
open **ssh_config** file
    vim /etc/ssh/sshd_config
Add below to above file to allow only **mario** group users to ssh into the system
    AllowGroups mario
restart ssh service
    service ssh restart