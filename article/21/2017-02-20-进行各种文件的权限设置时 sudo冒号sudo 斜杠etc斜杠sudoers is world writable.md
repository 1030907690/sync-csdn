---
layout:					post
title:					"进行各种文件的权限设置时 sudo:sudo /etc/sudoers is world writable"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
进行各种文件的权限设置时

报错

sudo:sudo /etc/sudoers is world writable
sudo:no valid sudoers sources found ,quitting
sudo:unable to initialize policy plugin

使用

pkexec chmod 0440 /etc/sudoers

解决



​