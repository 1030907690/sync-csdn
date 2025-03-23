---
layout:					post
title:					"building for iOS Simulator, but linking in object file built for iOS"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 项目中使用了openinstall，报错不支持模拟器运行。

```
building for iOS Simulator, but linking in object file built for iOS
```

## 解决方案
- 到项目的Build Settings，定位到User-Defined的VALID_ARCHS属性，增加x86_64。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7a410ef7a5a12cbb4c499190d814d442.png)

 