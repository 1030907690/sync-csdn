---
layout:					post
title:					"windows安装scrapy异常 error : Unable to find vcvarsall.bat"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
####使用pip install scrapy安装scrapy时抛出异常 `error : Unable to find vcvarsall.bat` 原因就是缺少C的编译环境。

- 解决方案一 ： 安装相对应版本的Visual Studio ，就会有C的编译环境了,Visual Studio软件比较笨重，不推荐这种方法。

- 解决方案二：到https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted下载Twisted的whl文件安装
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/71f1b6bf37bfa592b4ddc4ad10cfb8f8.png)

注意下载自己系统适应的whl，比如我的是python3.5，windows64bbit下载的是Twisted‑17.9.0‑cp35‑cp35m‑win_amd64.whl
然后一步步安装Twisted和scrapy
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/0ba0e579e9139528ce52f37d58d79b6a.png)

![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/a0d7cd450e535bc24f83d7e59290221f.png)

最后用`scrapy -h`命令测试是已经安装成功了。