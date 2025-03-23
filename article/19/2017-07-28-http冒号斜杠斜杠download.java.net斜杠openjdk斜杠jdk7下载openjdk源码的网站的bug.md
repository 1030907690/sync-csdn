---
layout:					post
title:					"http://download.java.net/openjdk/jdk7下载openjdk源码的网站的bug"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​


获取OpenJDK源码大致有两种方式，其中一种是通过Mercurial代码版本管理工具从Repository中直接取得源码http://hg.openjdk.java.net

第二种就是从网站上下载 ：http://jdk7.java.net/source.html(这个地址好像不能用了)还有个就是http://download.java.net/openjdk/jdk7  jdk7后面jdk版本可以自己输比如可以是jdk7 也可以是jdk8

从网上找到这个地址http://download.java.net/openjdk/jdk7下载openjdk源码不管是jdk8还是jdk7都提示找不到资源，后来找到一个能下载的地址，发现a标签的地址不对头



正确的地址应该是这样的：

http://download.java.net/openjdk/jdk7/promoted/b147/openjdk-7-fcs-src-b147-27_jun_2011.zip
域名应该是http://download.java.net/哇有点坑啊

​