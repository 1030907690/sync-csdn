---
layout:					post
title:					"windows安装多个Apache"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
复制出一个Apache



然后修改httpd.conf配置文件



修改的地方

<Directory "D:/php2/Apache/cgi-bin">
    AllowOverride None
    Options None
    Require all granted
</Directory>
ServerRoot "D:/php2/Apache"

然后cmd运行添加服务



可以看到这个服务运行就成功了





​