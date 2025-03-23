---
layout:					post
title:					"lua no resolver defined to resolve"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 使用resty.http模块请求报 `no resolver defined to resolve`，错误日志提示`attempt to index local 'resp'`，代码如下所示。

```
local resp, err = httpc:request_uri("http://xxx.com",{method = "GET",keepalive = false}) -- 发起请求
	ngx.say(  err)
```
- 解决方案，增加`DNS`配置，在conf配置文件中增加`resolver`配置。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4fd77d7becd36f0f36aa63b071043d70.png)
