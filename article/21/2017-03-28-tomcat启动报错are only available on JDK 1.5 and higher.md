---
layout:					post
title:					"tomcat启动报错are only available on JDK 1.5 and higher"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
具体异常为 ：

org.springframework.beans.factory.BeanDefinitionStoreException: Unexpected exception parsing XML document from class path resource [beans.xml]; nested exception is Java.lang.IllegalStateException: Context namespace element 'annotation-config' and its parser class [org.springframework.context.annotation.AnnotationConfigBeanDefinitionParser are only available on JDK 1.5 and higher
原因是当前我用的spring2.5的版本不支持我的jdk1.8

 解决办法 修改项目使用的jdk：

右键项目--》BUILD PATH--》Config Build Path--》Libraries-->Jre System Library--》Edit--》然后选择小一点的版本，我重启了一下myeclipse 就OK 啦

​