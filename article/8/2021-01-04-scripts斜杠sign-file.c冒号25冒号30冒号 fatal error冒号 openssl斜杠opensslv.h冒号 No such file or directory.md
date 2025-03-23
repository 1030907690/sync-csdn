---
layout:					post
title:					"scripts/sign-file.c:25:30: fatal error: openssl/opensslv.h: No such file or directory"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)   
## 错误详情
- 编译linux5.10.4内核时报错`scripts/sign-file.c:25:30: fatal error: openssl/opensslv.h: No such file or directory`。
## 解决方案
- 安装依赖
	- Centos/RedHat/Fedora
	
	```bash
	 yum install openssl-devel -y
	```
	- Ubuntu/Debian
	
	```bash
	 apt-get install libssl-dev 
	```
