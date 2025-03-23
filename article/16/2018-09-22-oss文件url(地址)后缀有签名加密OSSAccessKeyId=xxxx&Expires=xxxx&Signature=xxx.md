---
layout:					post
title:					"oss文件url(地址)后缀有签名加密OSSAccessKeyId=xxxx&Expires=xxxx&Signature=xxx"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- oss对象存储服务里面文件的访问地址后缀有OSSAccessKeyId=xxxx&Expires=xxxx&Signature=xxx；oss前缀+文件相对路径始终访问不了，一段要加上?那段才能访问；是因为bucket被设置成了私有读;**解决办法:把bucket设置为公共读。(注意:公共读启用这样的设置所有人拿到这个oss前缀+文件相对路径都可以访问了)**