---
layout:					post
title:					"Could not resolve: com.ibm.websphere:uow:6.0.2.17"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 导入Spring源码时，总是无法下载`com.ibm.websphere:uow:6.0.2.17`包，原来的地址`https://repo.spring.io/libs-release`需要认证，我替换为`https://maven.aliyun.com/repository/public`。至于为什么要换地址这个事情的详细情况请看上篇[xxx.jar‘. Received status code 401 from server: Unauthorized](https://sample.blog.csdn.net/article/details/112330695)。
-![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0e035ce9ab87418101a492b01f499100.png#pic_center)

## 问题分析
  - 从网上得知这个包需要从`spring`的仓库下载，查看`https://maven.aliyun.com/mvn/guide`这个地址后，发现`public`仓库并不包含`spring`仓库。`public`仓库如下图描述。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e2f646054958a131b92a0ef22639a218.png)

 ## 解决方案
  - 于是增加`https://maven.aliyun.com/repository/spring`配置，再次下载成功，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e5c7f5f958ff38e41fe85aab4b5ab94d.png)

