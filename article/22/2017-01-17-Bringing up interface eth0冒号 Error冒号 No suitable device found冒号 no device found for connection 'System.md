---
layout:					post
title:					"Bringing up interface eth0: Error: No suitable device found: no device found for connection 'System"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
linux修改ip重启后出现

service network restart
Bringing up interface eth0: Error: No suitable device found: no device found for connection 'System eth0'.

用ifconfig查看网卡默认切换到eth1了

解决办法： 将ifconfig查看到的HWaddr值替换到ifcfg-eth0里面，把eth0改为eth1

[zzq@weekend111 ~]$ ifconfig 
eth1      Link encap:Ethernet  HWaddr 00:0C:29:66:DA:E5  
          inet addr:192.168.16.135  Bcast:192.168.16.255  Mask:255.255.255.0
          inet6 addr: fe80::20c:29ff:fe66:dae5/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:30372 errors:0 dropped:0 overruns:0 frame:0
          TX packets:15047 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:40538308 (38.6 MiB)  TX bytes:1365035 (1.3 MiB)
          Interrupt:19 Base address:0x2024 

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:12 errors:0 dropped:0 overruns:0 frame:0
          TX packets:12 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:720 (720.0 b)  TX bytes:720 (720.0 b)
sudo vim  /etc/sysconfig/network-scripts/ifcfg-eth0
DEVICE=eth1
BOOTPROTO=static
IPADDR=192.168.16.135
IPV6INIT=yes
NM_CONTROLLED=yes
ONBOOT=yes
TYPE=Ethernet
UUID="825ee66f-10f7-4a55-899b-cdcd1042064b"
NETMASK=255.255.255.0
USERCTL=no
DEFROUTE=yes
IPV4_FAILURE_FATAL=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
NAME="System eth0"
HWADDR=00:0C:29:66:DA:E5
PEERDNS=yes
PEERROUTES=yes
IPV6_PEERDNS=yes
IPV6_PEERROUTES=yes
LAST_CONNECT=1477567305
[zzq@weekend111 ~]$ sudo service network restart
Shutting down interface eth0:                              [  OK  ]
Shutting down loopback interface:                          [  OK  ]
Bringing up loopback interface:                            [  OK  ]
Bringing up interface eth0:  Active connection state: activating
Active connection path: /org/freedesktop/NetworkManager/ActiveConnection/1
state: activated
Connection activated


​