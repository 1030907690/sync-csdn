---
layout:					post
title:					"Permission denied (publickey,gssapi-keyex,gssapi-with-mic)."
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 使用`ssh xx@xx -i xx.pem`命令连接服务器总是报权限问题，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b5c6b52fbcfa7fedb6f588a59e0d1a25.png)
- 有可能是`pem`文件权限的问题，解决方法是设置`400`权限。

```java
 chmod 400 xx.pem 
```
- 权限设置好后，就可以登录了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/43cf501c3ee779193d315ecfe5d0e7e1.png)

