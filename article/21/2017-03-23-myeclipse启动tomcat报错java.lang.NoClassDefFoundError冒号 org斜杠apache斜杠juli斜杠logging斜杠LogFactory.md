---
layout:					post
title:					"myeclipse启动tomcat报错java.lang.NoClassDefFoundError: org/apache/juli/logging/LogFactory"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​

java.lang.NoClassDefFoundError: org/apache/juli/logging/LogFactory
	at org.apache.catalina.startup.Bootstrap.<clinit>(Bootstrap.java:49)
Caused by: java.lang.ClassNotFoundException: org.apache.juli.logging.LogFactory
	at java.net.URLClassLoader$1.run(URLClassLoader.java:200)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.net.URLClassLoader.findClass(URLClassLoader.java:188)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:307)
	at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:301)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:252)
	at java.lang.ClassLoader.loadClassInternal(ClassLoader.java:320)
	... 1 more
Exception in thread "main" ERROR: JDWP Unable to get JNI 1.2 environment, jvm->GetEnv() return code = -2
JDWP exit error AGENT_ERROR_NO_JNI_ENV(183):  [../../../src/share/back/util.c:820]
解决办法：



打开myeclipse，Preferentces->MyEclipse->Servers->Tomcat->Tomcat 6.x->Paths
到prepend to classpath加载tomcat7下的……/bin/tomcat-juli.jar

​