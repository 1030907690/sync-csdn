---
layout:					post
title:					"spark Idea Maven开发环境搭建"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
一、下载maven，解压，下载地址Download Apache Maven – Maven

二、安装idea，Scala、和jdk环境

三、创建项目maven项目







选择maven路径



这里我给大家提供一个maven国内镜像，在settings.xml加入

	   <!-- 阿里云仓库 -->
	<mirror>  
      <id>alimaven</id>  
      <name>aliyun maven</name>  
      <url>http://maven.aliyun.com/nexus/content/groups/public/</url>  
      <mirrorOf>central</mirrorOf>          
    </mirror> 


创建项目完成



更新拉包并添加Scala sdk运行代码



如果运行代码出现如上情况，这个错误是由于Junit版本造成的，可以删掉Test，和pom.xml文件中Junit的相关依赖，

​