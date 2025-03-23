---
layout:					post
title:					"pull docker hub中的镜像失败 Error response from daemon: manifest for xxx not found: manifest unknown:"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- pull自己在docker hub中镜像报错，始终找不到这个镜像:

```
Error response from daemon: manifest for a1030907690/php-ubuntu:latest not found: manifest unknown: manifest unknown
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/64b509c44b5181a05dce456ffa696982.png)
- 后面发现自己当时根本没有上传`latest`tag
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cf85cded65ec8feef5e796d565a7a34b.png)
- 使用`a1030907690/php-ubuntu:14.04`就好了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8de633f6dc8641dce0b66ca5857c5ecc.png)
