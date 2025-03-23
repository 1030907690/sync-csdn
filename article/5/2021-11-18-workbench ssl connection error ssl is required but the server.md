---
layout:					post
title:					"workbench ssl connection error ssl is required but the server"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- workbench连接报错`ssl connection error ssl is required but the server`，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ccb0dd1ee9031c6ee8ba7457a85787a9.png)
## 解决方案
- 在[https://stackoverflow.com/questions/69824631/mysql-workbench-ssl-connection-error-ssl-is-required-but-the-server-doesnt-sup/69828778](https://stackoverflow.com/questions/69824631/mysql-workbench-ssl-connection-error-ssl-is-required-but-the-server-doesnt-sup/69828778)找到解决方案，Use SSL要选择`If available`
。但是发现当前最新版的`MySQL Workbench 8.0.27`没有这个选项。
- 于是我就下载了老版本`MySQL Workbench 8.0.16`，修改SSL选项，测试结果，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3ada9ee6cfd0686f2487be85b4a74041.png)
- 考虑到下载`workbench` 要登录，为了方便大家，我已经准备好了下载地址。[https://sourceforge.net/projects/generic-software/files/workbench/](https://sourceforge.net/projects/generic-software/files/workbench/)

## 其他
- 如果出现 `workbench requires the visual c++ 2015`，先安装 visual c++，`VC_redist.x64.exe`下载地址：[https://sourceforge.net/projects/generic-software/files/VisualC/](https://sourceforge.net/projects/generic-software/files/VisualC/) 或者[https://docs.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170](https://docs.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)
