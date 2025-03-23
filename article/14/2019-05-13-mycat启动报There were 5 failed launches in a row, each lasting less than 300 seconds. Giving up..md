---
layout:					post
title:					"mycat启动报There were 5 failed launches in a row, each lasting less than 300 seconds. Giving up."
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- mycat使用wrapper方式启动报错如下:

```
 	INFO   | jvm 5    | 2019/04/24 19:04:12 | Java HotSpot(TM) 64-Bit Server VM warning: ignoring option MaxPermSize=64M; support was removed in 8.0
	ERROR  | wrapper  | 2019/04/24 19:04:41 | Startup failed: Timed out waiting for a signal from the JVM.
	ERROR  | wrapper  | 2019/04/24 19:04:41 | JVM did not exit on request, terminated
	INFO   | wrapper  | 2019/04/24 19:04:41 | JVM exited on its own while waiting to kill the application.
	STATUS | wrapper  | 2019/04/24 19:04:42 | JVM exited in response to signal SIGKILL (9).
	FATAL  | wrapper  | 2019/04/24 19:04:42 | There were 5 failed launches in a row, each lasting less than 300 seconds.  Giving up.
	FATAL  | wrapper  | 2019/04/24 19:04:42 |   There may be a configuration problem: please check the logs.
	STATUS | wrapper  | 2019/04/24 19:04:42 | <-- Wrapper Stopped
```
- 这是因为wrapper注册的java服务起动超时,conf/wrapper.conf即可

```
 #设置超时时间
 wrapper.startup.timeout=7200
```
