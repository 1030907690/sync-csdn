---
layout:					post
title:					"eclipse java.lang.Error: Unresolved compilation problem并且项目依赖一堆感叹号"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
>确定Windows -> Preferances  Java Compiler  、Java build Path Librarie 、 Project Facets(web项目有这个)  jdk版本一致
	再到 Windows -> Preferances -> Java -> Installed JREs 切换一下默认jdk(换一下勾选，我这里有个jdk7和jdk8) ,Apply 等待一下progress，它应该在构建， 然后再把默认jdk切换回来，感叹号消失项目就可以运行了。