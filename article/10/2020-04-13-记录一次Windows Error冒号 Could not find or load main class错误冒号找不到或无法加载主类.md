---
layout:					post
title:					"记录一次Windows Error: Could not find or load main class错误:找不到或无法加载主类"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
![-](https://i-blog.csdnimg.cn/blog_migrate/86be367fb125e73c23092b7e1fad99d3.png)
 - 下面来看看查错的心路历程
 	- 打开百度、谷歌大部分说是环境问题`CLASSPATH`变量文件
		 - 我设置了变量还是要报错；我在Linux上测试了没问题；即使不配置`CLASSPATH`也能运行
	- 有人说是英文环境问题；我的是windows10 英文版的，我又设置成中文的，还是没有解决。

	- 后面搜索了下`java -cp`发现`windows`依赖中间用分号`;`,Linux用冒号`:`
	- windows正确的格式是这样的`java  -cp library/*;xxxx.jar     xxxx.ServerStart arg1 arg2...` 这回真是阴沟里翻船了，还是自己太粗心大意了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ebfe6f6ea4a6281707c481b1472126cc.png)
