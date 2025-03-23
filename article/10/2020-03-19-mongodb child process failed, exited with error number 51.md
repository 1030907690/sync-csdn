---
layout:					post
title:					"mongodb child process failed, exited with error number 51"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---

```bash
about to fork child process, waiting until server is ready for connections.
forked process: 12233
ERROR: child process failed, exited with error number 51
To see additional information in this output, start without the "--fork" option.
```
- mongodb4.0.13分片集群报`child process failed, exited with error number 51`我遇到了这个异常，百度、Google一波，面向搜索引擎编程，得到的结果是这个异常大部分是因为mongodb 服务的不正常关闭，导致mongod 被锁；解决办法：1、删除MongoDb安装目录下的 mongod.lock 文件 2、`mongod  -f xxx.conf --repair`  修复
- 但是一顿操作后依然没有解决；后面仔细看了下`To see additional information in this output, start without the "--fork" option.` 它说把`fork`去掉可以得到详细日志；于是便
注释了这个参数，便有了下面的:
- `Unrecognized option: sharding.pidFilePath` 不能解析这个属性这个属性的值就是`/var/run/mongodb/mongos.pid`,我看了下没有`/var/run/mongodb/`这个路径
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1da66fa332722afb30e3f91ff0014b43.png)
- 创建了这个路径就能启动了`/var/run/mongodb/`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/946277db1b6472e837249cb457e82eb5.png)
- 这个问题应该是刚加了块磁盘的原因。
- 总结:`child process failed, exited with error number 51`这个异常原因可能很多最好把`fork`参数注释掉，好对症下药。