# Diagnose Network Speed within the Nodes
https://linode.com/docs/networking/diagnostics/install-iperf-to-diagnose-network-speed-in-linux/

"iPerf" is a command-line tool used in the diagnostics of network speed issues. iPerf measures the **maximum network throughput** a server can handle. It is particularly useful when experiencing network speed issues, as you can use iPerf to determine which server is unable to reach maximum throughput.

## How to Use iPerf
iPerf must be installed on both computers between which you are testing the connection. If you are using a Unix or Linux-based operating system on your personal computer, you may be able to install iPerf on your local machine.
=== Install iPerf ===
== On Debian and Ubuntu: ==
You can use ''apt-get'' to install **iPerf** on Debian and Ubuntu:
    apt-get install iperf
== On CentOS: ==
CentOS repositories do not have **iPerf** by default. Use the **EPEL repository**, which is a repository used to install **third-party software packages** on RedHat systems such as RHEL and CentOS
    yum install epel-release
    yum update
    yum install iperf
=== TCP Clients & Servers ===
iPerf requires two systems because one system must act as a **server**, while the other acts as a **client**. The client connects to the server you’re testing the speed of.
  - On one node you wish to test, launch **iPerf in server mode** as

    iperf -s

  - On your second node, **connect to the first**. (Replace 10.10.0.2 with the first node’s IP address).

    iperf -c 198.51.100.5

  - To stop the **iPerf server process**, press ''CTRL + c''
