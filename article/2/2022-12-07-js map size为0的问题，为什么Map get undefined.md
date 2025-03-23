---
layout:					post
title:					"js map size为0的问题，为什么Map get undefined"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 问题背景
- 我发现Map初始化并不完整，如下图。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/82f70663fa4a4d1122ffd1f445e0a310.png)
- 这里面是有数据的，但是`size为0`。这个Map其实已经在前一个方法初始化赋值了。
- 但是我调用get方法获取值都是`undefined`。
## 解决
- 后面想到可能是异步的问题。在我调用`Map get`方法的时候还没有初始化完成。所以用`setTimeout`去延迟测试了一下，果然是这样。

- 于是我改成`同步`的`async`和`await`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e9940912a610376441940a00bac1a7e2.png)
- 再看输出就有`size`了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a2c0600049447712ce0ea36f9e927a96.png)

## 参考
- [https://segmentfault.com/q/1010000012758482](https://segmentfault.com/q/1010000012758482)，这篇文章让我想到了未初始化完整的问题。