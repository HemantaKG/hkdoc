# ssh to compute node without password
generate a ssh rsa key (if not generated) and copy the key from **~/.ssh/id_rsa.pub** to **~/.ssh/authorized_keys**
````
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
````

# copy ssh key to other system
generate a ssh rsa key (if not generated) and copy the key from the local system to remote system (password required to copy ssh key).
Note:
- Remote system: storage
- Local system: master
````
ssh-keygen -t rsa
ssh-copy-id root@<<FQHN>>
````
