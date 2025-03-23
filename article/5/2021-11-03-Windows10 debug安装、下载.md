---
layout:					post
title:					"Windows10 debug安装、下载"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 由于Windows 10不支持`debug`命令，如果装虚拟机Windows XP就比较耗内存，所以我用的是`DOSBox`，然后挂载`debug`程序文件目录。
## 下载
-  `DOSBox`、`debug`、`masm`等等，我已经整理好了，下载地址：[https://sourceforge.net/projects/generic-software/files/Windows10-debug/](https://sourceforge.net/projects/generic-software/files/Windows10-debug/)
## 安装和使用
- 解压`DEBUG.zip`文件，记住程序路径（比如我这里是d:\software\debug），安装好`DOSBox`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/98e5239fe90e4d212a8281a5c3789c45.png)
- 然后启动。使用命令挂载所要的程序（d:\software\debug是我自己的路径）。

```bash
mount c d:\software\debug
```
- 切换到挂载路径 `c:`

```bash
c:
```
- 使用`debug` 命令。
- 输入`r`查看下各个寄存器情况，如下图所示，表示安装成功了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/63b0a62cfe5e33a00986709920bfcf6b.png)
