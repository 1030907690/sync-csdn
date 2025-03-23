---
layout:					post
title:					"eclipse提示Access restriction: The type 'HttpServer' is not API"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
用eclipse导入一个框架源码时发现用到HttpServer地方报错：

```
Access restriction: The type 'HttpServer' is not API
```
- 问题原因:

	 - eclipse有一个称为访问限制的机制，不认为你应该使用Sun的内部软件包,防止您意外使用Eclipse认为不属于公共API的类,Eclipse 默认把这些受访问限制的API设成了error

- 解决方案一 ： 右击项目> Build Path >Config Build Path > Libraries >把当前的jre   remove掉， 然后再add Libary 把它从新添加进来。

- 解决方案二 ： Project properties -> Java Compiler -> Errors/Warnings -> Deprecated and restricted API



- 
