---
layout:					post
title:					"idea没有tomcat选项也没有Application Servers"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 原因背景:windows10系统因为自动更新后,idea未正常关闭,重启后发现，Tomcat的选项不见了，File->Setting->Build,Excution,Deployment里面Application Servers也不见了。
- 解决办法:到File->Setting->Plugins里面的 Application Servers View勾选取消掉 应用 重启， 然后在勾选上 重启idea后就可以了