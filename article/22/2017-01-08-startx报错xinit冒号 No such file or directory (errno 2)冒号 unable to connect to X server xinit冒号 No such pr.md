---
layout:					post
title:					"startx报错xinit: No such file or directory (errno 2): unable to connect to X server xinit: No such pr"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
startx突然启动不了图形界面了报错

xinit: No such file or directory (errno 2): unable to connect to X server

xinit: No such process (errno 3): Server error.

解决办法：

[root@localhost ~]# yum groupinstall "X Window System"
[root@localhost ~]# yum groupinstall "Desktop"

启动Gnome桌面
[root@localhost ~]# startx


​