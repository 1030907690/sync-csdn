---
layout:					post
title:					"RPC failed; curl 56 OpenSSL SSL_read: SSL_ERROR_SYSCALL, errno 10054"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- git clone时报错 RPC failed; curl 56 OpenSSL SSL_read: SSL_ERROR_SYSCALL, errno 10054，有文件太大导致的。

```
Administrator@zhouzhongqing MINGW64 /f/work/self
$ git clone https://github.com/xxxxxx/netty-netty-4.1.27.Final.git
Cloning into 'netty-netty-4.1.27.Final'...
remote: Enumerating objects: 3327, done.
remote: Counting objects: 100% (3327/3327), done.
remote: Compressing objects: 100% (1548/1548), done.
error: RPC failed; curl 56 OpenSSL SSL_read: SSL_ERROR_SYSCALL, errno 10054
fatal: The remote end hung up unexpectedly
fatal: early EOF
fatal: index-pack failed

```
- 解决办法,文件大小的上限设置大点: 

```
 git config --global http.postBuffer  524288000
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/aab62a8ecf4740de3f05ad0f6eb5f03f.png)