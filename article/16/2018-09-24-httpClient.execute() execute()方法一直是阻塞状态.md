---
layout:					post
title:					"httpClient.execute() execute()方法一直是阻塞状态"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- execute()方法一直是阻塞状态原因:一般是在等待接口的返回。
- 解决办法:接口给个返回值(这个是接口无返回值的情况)或者设置读取接口返回结果的超时时间。