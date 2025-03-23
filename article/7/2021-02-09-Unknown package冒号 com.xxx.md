---
layout:					post
title:					"Unknown package: com.xxx"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 我把整个项目打包，换到另一台电脑运行会报：

```
Unknown package: com.xxx
```
- 原因可能是前一台电脑编译出来的东西不适合。

## 解决方案
- 先清理`Clean Project`，然后重新构建`Rebuild Project`或者`Make Project`，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/41491ceed2834a8ebc905d61bf198dd2.png)

- 重新编译后，运行成功，如下图所示

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ad8b03cb2aa1aaa44075eb12c6054d18.png)

