---
layout:					post
title:					"Could not open xxxxx/jvm.cfg,Java was started but returned exit code=1"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 下载的eclipse打开报错 `Could not open D:\software\Java\jre1.8.0\lib\amd64\jvm.cfg`，如下图所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5ff80b06bf6dba9fbd4990b96589346d.png)
- 点击ok后又报一个错，`Java was started but returned exit code=1`。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6e69848fbfb4695931686e39a708f18b.png)
-----
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4885ce8be497cdef32a5c9a692666291.png#pic_center)

## 解决方案
- 很明显`C:\Program Files (x86)\Common Files\Oracle\Java\javapath\javaw.exe`并不是我的jdk安装路径，可能不完整，有的程序，走这个路径可能会出现意外的情况。
- 我的解决办法是把文件夹改个名字，让它走我配置好的JDK环境。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1fcc172228af8b1f21434b3ad75f18db.png)
- 这样的话，它就只能走我配置的JDK环境了，再次点击eclipse.exe，就能打开了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fc08f94936dc2f63ca91637922c9006a.png)
