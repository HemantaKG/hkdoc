## InfiniBand Principles

### Bacis point
- Infiniband is a switch fabric architecture
- High bandwidth btween 10Gb/s to 120Gb/s
- Low latency (~170nanosec/HOP)
- Low CPU utilization using RDMA (Remote Direct Memory Access) i.e bypass the OS and the CPU's
- Automatic cluster switches and ports configuration/management is performed by the Subnet Manager Software (SM)
- Channel copy manager is call Host Channel Adapter (HCA) or IB network card. HCA has two sides, one side is PCIe3 bus and another side a QFP connectors 
----
> NOTE:
* short distance -> copper cable
* long distance -> fiber cable
* QFP connector (SSP and SSP+ connectors??)
----

- What is layer 2 network or switching?
```
one subnet or layer two switching means "that all the nodes belongs to the same subnet"
```

- Is the a layer 3 network?
````
Currently in partical we working without layer 3 network.
But is InfiniBand protocal we have router in the standerd. We have layer 3 for routing of infiniBand addresses.
The routing will helpus to move traffic between one subnet to another subnet.
Its in theory. (Currently not implemented)
````

- How to move traffic between two different envs (two computer in ethernet and other computer in infiniBand env)?
````
Using Gateway.
The gateway is a conveter bewteen protocals here the protocals are eth to IB and IB to eth. (i.e IP over IB, IP/IB)
````

- What is software definded network (SDN)?
````
In infiniBand env the SDN manages the noetwork automatically no need to network administater.
The SDN is infiniBand is called subnet manager (SM).
Its most importent enetity in the infiniBand network. *sometiem is doesn't work.
Active and fallback SMs is important to have in any network for HPC reliability.
````

- What are the HCA bandwith optinons or InfiniBand speed?
````
Single Data Rate (SDR) 2.5GB/s* 4= 10GB/s
Double Data Rate (DDR) 5GB/s* 4= 20GB/s
Quadruple Data Rate (QDR) 10GB/s* 4= 40GB/s
Fourteen Data Rate (FDR) 14GB/s* 4= 56GB/s
Enhanced Data Rate (EDR) 25GB/s* 4= 100GB/s 
````

- GUID (Global Unique Identifier), it is 64 bit address, it is like a ethernet MAC address.
  * Assigned by IB vendor
  * Persistent through reboots (it is fixed)
  * HCA has a unique GUID
  * IB switch has only on GUID
  * It is a layer one address

- Every IB switch has only on GUID. is it correct? if yes, How you indentify the each port or What is the unique id of each port of the IB switch?
````
Yes, IB switch has only one GUID to uniquely identify hte IB switch.
The port GUID is calculated by adding the port number to the switch GUID.

port GUID= IB switch GUID + port number
````

- What is system GUID?
````

````

- What is ASIC in IB switch?
````

````

- What is leaf switchs?
- What is spine switchs?
- What is non-blocking netwrok?
- What is semi-non-blocking netwrok? How to calculate blocking ratio?
- Unicast and Multicast (no broadcast in infiniBand)
- What is LID and who provides LID? What are the LID ranges? (it is layer two address)
- What is partitioning in InfiniBand? What is use of it?
----

- What is GID (Global Indentifier)? What is the use of it?
- What is responsibility of MAD (Management Datagram)
- What is responsibility of SM (Subnet Manager? LFT (Linear Forwording Table)?
- 

