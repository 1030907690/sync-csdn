---
layout:					post
title:					"packet_write_wait: Connection to UNKNOWN port 65535: Broken pipe"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- ssh连接到另一台主机一会儿不动老掉线怎么办？
- 解决办法：可以使用ServerAliveInterval参数设置；`ServerAliveInterval会在隧道无通信后的一段设置好的时间后发送一个请求给服务器要求服务器响应。`在原来的基础上加上`-o ServerAliveInterval=60`即可； 
```
ssh   -o ServerAliveInterval=60  root@47.56.67.xx
```
