---
layout:					post
title:					"class file has wrong version 55.0, should be 52.0"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 今早更新代码，准备编译启动启动时，项目报`class file has wrong version 55.0, should be 52.0`异常，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/da3adce87cf04c15f71c76b8601ffc1d.png)
## 分析
- 错误提示：类文件有错误的版本 55.0，应该是 52.0。这里的`55和52是主版本(Major Version)`，主版本(Major Version)和JDK版本的对应关系如下表所示。


| 主版本(Major Version) | 对应JDK版本 |
|--| --| 
|52|JDK 8|
|53|JDK 9|
|54 | JDK 10|
|55 | JDK 11|
### 确认Jar的主版本
- 我们可以把Jar包用解压软件，得到class文件。使用`javap -v xxx`翻译生成汇编代码输出行号、局部变量表信息、常量池、版本号等信息。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/916aed1f925fb8a88cad3c1b3e6c9f3a.png)
- 或者使用`HexView`也能查看主版本号，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4851def4ab1ee7017c22c5b4bbe7d81e.png)
> 0x0037转为10进制就是`55`。
### 确认问题
- 我们看到主版本是`55`，对应上表就是JDK 11，这样局势就明朗了。

- 提示上说这个class（或者说这个Jar）用的是`JDK 11`编译出来的，而我本地的是`JDK 8`，所以低版本没能力兼容高版本的东西导致了报错。
## 解决方案
- 第一种：不要使用这个Jar或者里面的任何类。
- 第二种：升级自己的JDK。
- 第三种：有条件的可以把源码下载下来，用自己本地JDK，编译出来Jar，这样就和自己本来JDK兼容了。