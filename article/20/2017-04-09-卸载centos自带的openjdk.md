---
layout:					post
title:					"卸载centos自带的openjdk"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
一、使用rpm -qa | grep java命令查看包

[zzq@weekend110 jdk1.7.0_80]$ rpm -qa | grep java
javapackages-tools-3.4.1-11.el7.noarch
java-1.8.0-openjdk-headless-1.8.0.102-4.b14.el7.x86_64
java-1.8.0-openjdk-1.8.0.102-4.b14.el7.x86_64
tzdata-java-2016g-2.el7.noarch
python-javapackages-3.4.1-11.el7.noarch
java-1.7.0-openjdk-headless-1.7.0.111-2.6.7.8.el7.x86_64
java-1.7.0-openjdk-1.7.0.111-2.6.7.8.el7.x86_64

二、卸载

[zzq@weekend110 jdk1.7.0_80]$ sudo rpm -e --nodeps java-1.8.0-openjdk-1.8.0.102-4.b14.el7.x86_64
rpm -e 为卸载  

--nodeps  忽略掉rmp包的依赖关系

​