---
layout:					post
title:					"Cannot find a valid baseurl for repo: base/7/x86_64"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
Linux出现这种情况一般是没有联网

解决办法：

1、打开 vi /etc/sysconfig/network-scripts/ifcfg-eth0（每个机子都可能不一样centos7就不是ifcfg-eth0了，但格式会是“ifcfg-xxx”），把ONBOOT=no，改为ONBOOT=yes(ONBOOT是指明在系统启动时是否激活网卡，只有在激活状态的网卡才能去连接网络，进行网络通讯)

                2、service network restart （重启网络）