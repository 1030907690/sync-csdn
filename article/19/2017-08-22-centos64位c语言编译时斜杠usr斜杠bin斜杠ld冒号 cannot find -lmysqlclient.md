---
layout:					post
title:					"centos64位c语言编译时/usr/bin/ld: cannot find -lmysqlclient"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
centos7编译c程序报错：

/usr/bin/ld: cannot find -lmysqlclient
原因：libmysqlclient.so不在/usr/lib目录下，而是在/usr/lib64/mysql目录下
解决：建一个软连接或者复制到/usr/lib目录下
cp -r /usr/lib64/mysql/* /usr/lib/


​