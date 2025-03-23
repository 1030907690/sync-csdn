---
layout:					post
title:					"idea自动下载gradle失败解决方案"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 由于要导入源码，源码使用的包管理工具是gradle，之前也没有配置过gradle的环境，一导入源码就自动下载gradle，无奈的是由于网络问题，每次都下载失败。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3ae30f23313f234f16143adf4bd3384e.png#pic_center)

## 解决方案
### 第一种办法：设置代理法
- 有条件的童鞋，可以给IDEA设置代理，点击File->Settings，找到Http Proxy设置代理，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/94ef72386365f59455c5e4d9acb5b112.png)
- 设置代理后下载就不会超时了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6eb91131fa43dcec7783b4cde7faf264.png)
- 如果没有代理环境的童鞋请看第二个方法。
### 第二种办法：替换法
- 我在idea每次下载时发现了一个规律，每次都会在这个位置下载gradle的安装包，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/125a66469a30e645e25c642f96a3d50a.png)
全路径如下：`C:\Users\pn20120162\.gradle\wrapper\dists\gradle-4.4.1-bin\46gopw3g8i1v3zqqx4q949t2x`，也就是`C:\Users\用户名\.gradle\wrapper\dists\gradle版本\随机串`，我们目前就卡在了下载安装包这步。
- 我在想，我先把安装包下载下来，然后放到这个目录（`C:\Users\pn20120162\.gradle\wrapper\dists\gradle-4.4.1-bin\46gopw3g8i1v3zqqx4q949t2x`）去，那么idea就不用再执行下载步骤了。
- 预先下载好所需要的安装包（推荐使用迅雷等软件下载，比较快），放到对应的目录。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/390f2fa9f3ec1d1eb0c338daa2cab54b.png)
- 点击重新导入。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c352859a3a8dcf11ce5967d3ff4419e0.png)
- 然后可以看到，安装包自动解压。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5b4230db6677d1ebbdc294649f6c3462.png)
- 最后gradle执行下载依赖等逻辑
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6e840a2d2f40b944fef2ff6a30dd06e4.png)
