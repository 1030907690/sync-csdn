---
layout:					post
title:					"windows MongoDB 远程连接"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
![这里写图片描述](https://img-blog.csdn.net/20180304091731377?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

- 在内网一台windows电脑安装好MongoDB,DOS命令运行 D:\software\MongoDB\Server\3.6\bin/mongod.exe --dbpath D:\software\MongoDB\Server/mongodbData ， 在我自己的电脑上telnet 192.168.0.55 27017发现端口是不通的，开始以为是防火墙 的问题，结果windows的防火墙压根儿没开。后面想这个MongoDB远程连接是否跟MySQL数据库一样要配置什么参数,查了下果真是。

- DOS命令运行的参数：
```
		--bind_ip 192.168.0.55  //绑定服务IP，若绑定127.0.0.1，则只能本机访问，不指定默认本地所有IP
		--logpath D:\software\MongoDB\Server/logs\mongodb.log  // 定MongoDB日志文件，注意是指定文件不是目录
		--logappend  // 使用追加的方式写日志
		--dbpath E:\MongoDB_Data\db  // 指定数据库路径
		--port 27017 // 指定服务端口号，默认端口27017
		--service // 以服务方式启动
		--serviceName //指定服务名称
		--serviceDisplayName//
```

- 我修改了一下启动的参数改为(可以写成bat执行)：
	

```
D:\software\MongoDB\Server\3.6\bin/mongod.exe --dbpath D:\software\MongoDB\Server/mongodbData --logpath D:\software\MongoDB\Server/logs\mongodb.log  --logappend  --bind_ip 192.168.0.55  
```

运行后终于可以其他ip连接了
![这里写图片描述](https://img-blog.csdn.net/20180304092434785?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

