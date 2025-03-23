---
layout:					post
title:					"ERROR: Unsupported method: AndroidProject.getVariantNames()"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 背景：android项目导入报错`ERROR: Unsupported method: AndroidProject.getVariantNames().`；我之前是windows环境开发，但是后面换成linux就报错；把as版本换成一致依然报错。
- 解决办法
	- 1、插件版本和所需的 Gradle 版本要对应,官网地址:[https://developer.android.google.cn/studio/releases/gradle-plugin#updating-gradle](https://developer.android.google.cn/studio/releases/gradle-plugin#updating-gradle)
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6950088e8776f2688b72e7a3e344aefd.png)
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3397b0c8af77604f43f9943dec81f1d9.png)
 	- 2、之前as的那些sdk都要下载下来
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c92f755d0d0c2be97be33fdcb16846df.png)

- 当然这个不一定所有都适用，主要还是根据具体错误信息来判定如何解决。