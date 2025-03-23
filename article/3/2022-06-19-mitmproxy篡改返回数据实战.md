---
layout:					post
title:					"mitmproxy篡改返回数据实战"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- `mitmproxy`是一个非常强大的抓包工具，还可以篡改数据，充当中间人的角色。支持使用使用`python`脚本完成一些对流量的自定义操作。
- 有以下3中方式可启动`mitmproxy`：
	- `mitmproxy`是一个交互式的、支持SSL/TLS的拦截代理，具有HTTP/1、HTTP/2和WebSockets的控制台接口。
	- `mitmweb`是mitmproxy基于web的界面。
	- `mitmdump`是mitmproxy的命令行版本。
- 本文使用`mitmweb`完成篡改数据。

## 实战
### 安装对应证书
- 要先安装证书。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b54de8b6bfbd879e676d8c3ca1747965.png)
- 点击后，会进入[http://mitm.it/](http://mitm.it/)，注意：这个页面必须使用mitmproxy代理才能进入正确的页面。正确的页面如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f930a48c3453ed2540c2feaf436750ca.png)

### 拦截
- 我们先来熟悉下操作界面。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/04a569bbaee78096c3d46a82f66a0103.png)
- 主要使用的功能就是拦截的输入框，比如我要拦截如下图的界面。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0164653d7c372fb81a92d1a8f281549f.png)

- 我想让它返回`hello world`。
> 这个网页事先要使用mitmproxy的代理。我用了`SwitchyOmega`

- 我先在拦截的输入框输入框`baidu`。
- 当我发起请求时，`mitmproxy`已经拦截住了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d2ef1a9565beeea5a17ee495ee3576f7.png)
- 我并不修改请求，直接点击`Resume`，现在就有返回值了，如下图所示。 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3c378b10ba56bd0960b1543aca2dafbf.png)

### 修改返回数据
- 点击Edit修改好返回数据，Done完成，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/854a267f54b22e6f8eddfd5454f766b4.png)
- 继续点击`Resume`，然后查看网页。修改成功，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ebc837725857441acf7c2638a3e54c1f.png)


## 小结
- `mitmproxy`可以在很多个平台上使用，非常强大，我这里只用了它一小点点功能特性。具体的可看[https://docs.mitmproxy.org/stable/overview-features/](https://docs.mitmproxy.org/stable/overview-features/)。
- 之前写过一篇[绕过反调试fuck-debugger](https://blog.csdn.net/baidu_19473529/article/details/122768471)，现在想想用`mitmproxy`同样能达到效果。

>`mitmproxy`可以拿到到`https`的数据，并不意味着它把https破了，因为前提是被监听机器上要事先安装好证书。



