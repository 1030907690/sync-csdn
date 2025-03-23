---
layout:					post
title:					"eclipse Access restriction: The type 'xxx' is not API (restriction on required library '')"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
eclipse报错：

Access restriction: The type 'ProxyGenerator' is not API (restriction on required library 'D:\software\Java8\jdk1.8.0_144\jre\lib\rt.jar')

后面查看到配置，原来是不知道怎么的导入了2份jdk了



 解决方法： 
        Project -> Properties -> libraries， 
          remove  一个 JRE System Library就可以了。 

​