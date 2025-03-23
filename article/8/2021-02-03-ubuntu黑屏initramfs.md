---
layout:					post
title:					"ubuntu黑屏initramfs"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- Ubuntu虚拟机突然无法保存文件，文件报只读；然后重启Ubuntu，发现出现黑屏，出现`initramfs`命令行。提示如下所示。

```
......
The root filesystem on /dev/sda1 requires a manual fsck
......
```
## 解决方案
- 使用`fsck`修复磁盘，命令如下所示。

```
fsck -t ext4 /dev/sda1   #/dev/sda1 就是上面的提示
```
- 然后一直按住`y`。
- 最后`reboot`重启。

