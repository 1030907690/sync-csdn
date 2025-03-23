---
layout:					post
title:					"jProfiler远程连接Linux监控jvm、tomcat运行状态(很详细)"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
第一步、下载软件

官网地址：ej-technologies - Download JProfiler ，一个linux服务端，一个windows客户端 GUI界面



第二步、安装

1、下载好后把tar包上传的linux服务器，解压。

   /

2、修改tomcat的bin/catalina.sh文件



      jprofiler的安装路径和端口，我配的端口是10001

3、再重启tomcat

我们可以看看tomcat的启动日志



可以看到10001端口启动成功了。

第三步、安装windows jprofiler客户端和建立远程连接

        1、安装好windows jprofiler软件

2、连接linux监控运行状态

点击



选择远程连接



选择jdk的版本





连接的地址



jprofiler在Linux上安装的路径



后边就是再填端口，我的是10001，然后就点完成。

点击start center可以看到自己配的



然后选中，点击start的界面就是这样的



好，到此完成。

​