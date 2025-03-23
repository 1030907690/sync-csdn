---
layout:					post
title:					"启动tomcat报错apache-tomcat-7.0.76\bin\tcnative-1.dll: Can't load AMD 64-bit .dll on a IA 32-bit platfor"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​

java.lang.UnsatisfiedLinkError: D:\software\Tomcat\apache-tomcat-7.0.76\bin\tcnative-1.dll: Can't load AMD 64-bit .dll on a IA 32-bit platform
意思是当前tcnative-1.dll是64bit的但是要运行在32bit机子上

解决办法：

找一个和当前版本接近或相同的32bit tomcat版本替换tcnative-1.dll文件就可以正常运行了

​