---
layout:					post
title:					"Windows Bochs没有进入debug界面"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 本来是想用bochs来调试程序的，谁知程序执行完了都没进入debug界面，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/983ee3c88d06e526cf6278cc156dc268.jpeg)
## 解决方案
- 原来Windows的bochs有2个入口 。`bochs.exe`和`bochsdbg.exe`。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3fca17f2f4942f24325dcde4a75fac56.png)
- 使用`bochsdbg.exe`才会进入`debug`。下图就进入debug了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/48914df58d245be8b3236a46b5f1ba8d.png)
## 参考
- [https://zhuanlan.zhihu.com/p/59980855](https://zhuanlan.zhihu.com/p/59980855)