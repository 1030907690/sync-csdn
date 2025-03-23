---
layout:					post
title:					"Unable to import maven project: See logs for details"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 今天刚搭建的idea+maven居然用不了，这就尴尬了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e4e63d858b2b81e4231e02cc19fee2c0.png)
- 解决方案:查找日志
	- 1、打开日志目录Help->Show  Log in FIles
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b3c6bd7a73a90a1b1702439175e57dec.png)
	- 2、打开文件查看日志
	```
	2020-02-10 11:01:36,438 [ 123574]  ERROR -      #org.jetbrains.idea.maven - com.google.inject.CreationException: Unable to create injector, see the following errors:
	
	1) No implementation for org.apache.maven.model.path.PathTranslator was bound.
	  while locating org.apache.maven.model.path.PathTranslator
	    for field at org.apache.maven.model.interpolation.AbstractStringBasedModelInterpolator.pathTranslator(Unknown Source)
	  at org.codehaus.plexus.DefaultPlexusContainer$1.configure(DefaultPlexusContainer.java:350)
	
	2) No implementation for org.apache.maven.model.path.UrlNormalizer was bound.
	  while locating org.apache.maven.model.path.UrlNormalizer
	    for field at org.apache.maven.model.interpolation.AbstractStringBasedModelInterpolator.urlNormalizer(Unknown Source)
	  at org.codehaus.plexus.DefaultPlexusContainer$1.configure(DefaultPlexusContainer.java:350)
	
	2 errors 
	java.lang.RuntimeException: com.google.inject.CreationException: Unable to create injector, see the following errors:
	
	1) No implementation for org.apache.maven.model.path.PathTranslator was bound.
	  while locating org.apache.maven.model.path.PathTranslator
	    for field at org.apache.maven.model.interpolation.AbstractStringBasedModelInterpolator.pathTranslator(Unknown Source)
	  at org.codehaus.plexus.DefaultPlexusContainer$1.configure(DefaultPlexusContainer.java:350)
	
	2) No implementation for org.apache.maven.model.path.UrlNormalizer was bound.
	  while locating org.apache.maven.model.path.UrlNormalizer
	    for field at org.apache.maven.model.interpolation.AbstractStringBasedModelInterpolator.urlNormalizer(Unknown Source)
	  at org.codehaus.plexus.DefaultPlexusContainer$1.configure(DefaultPlexusContainer.java:350)
	
	```

	![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5be487274de095dd81740d91033a6bc8.png)
	- 3、写java的朋友应该对`implementation` 不陌生吧!就是没有对应的实现，这应该就是版本问题了；想来也是我idea用的是2017.2，但是我maven用的目前最新的3.6。
	- 4、于是我在maven [存档](https://archive.apache.org/dist/maven/binaries/)中下载了旧版本3.0.5
	- 5、更换了低版本的的确可以用了
		![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fc3e9c21ca3f6e1b79815dec12584184.png)