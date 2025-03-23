---
layout:					post
title:					"net::ERR_CONTENT_LENGTH_MISMATCH 206"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 服务用的是nginx+tomcat,发现jQuery的js文件在报`net::ERR_CONTENT_LENGTH_MISMATCH`异常
- 解决方案:加大缓存大小，nginx的代理缓存区，默认较小导致部分文件出现加载不全的问题，比较典型的如jQuery框架，可以通过配置调整nginx的缓存区即可。

```
http{
................................
	proxy_buffer_size 128k;
	proxy_buffers   32 128k;
	proxy_busy_buffers_size 128k;
	.............................
}

```
