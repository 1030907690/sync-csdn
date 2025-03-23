---
layout:					post
title:					"ssh连接报Connection closed by foreign host."
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
今天连接linux时居然连不上，报错信息是：

Connecting to 192.168.16.133:22...
Connection established.
To escape to local shell, press 'Ctrl+Alt+]'.

Connection closed by foreign host.

Disconnected from remote host(hadoop3) at 10:56:11.

Type `help' to learn how to use Xshell prompt.

查了一下终于找到了解决办法，只需要一些命令就可以了：

    cd /etc/ssh
    sudo chmod 644 ./*
    sudo chmod 600 ssh_host_dsa_key
    sudo chmod 600 ssh_host_rsa_key
    sudo chmod 755 .
    /etc/init.d/sshd restart
完成后在重新连接就行了。
 



​