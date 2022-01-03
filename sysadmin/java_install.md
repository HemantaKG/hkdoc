==== install java ====
Ref: [[https://medium.com/coderscorner/installing-oracle-java-8-in-ubuntu-16-10-845507b13343|java 8 installation on Ubuntu]]
    https://medium.com/coderscorner/installing-oracle-java-8-in-ubuntu-16-10-845507b13343
==== check h=java version ====
    java -version
==== set default java version ====
If you have multiple Java packages installed on your machine, to check which version to use as the default type use the following command
    sudo update-alternatives --config java


=== Oracle Jave installation ===
Ref:
  * https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04

set repository:
<code>sudo add-apt-repository ppa:webupd8team/java</code> 
update system:
<code>sudo apt update</code>
install java (version 6):
<code>sudo apt-get install oracle-java7-installer</code>
install java (version 7):
<code>sudo apt-get install oracle-java7-installer</code>
install java (version 8):
<code>sudo apt install oracle-java8-installer</code>
install java (version 9):
<code>sudo apt install oracle-java9-installer</code>
managing java:
<code>sudo update-alternatives --config java</code>
