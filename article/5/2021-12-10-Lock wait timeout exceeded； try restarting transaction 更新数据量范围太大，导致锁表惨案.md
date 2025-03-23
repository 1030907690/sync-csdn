---
layout:					post
title:					"Lock wait timeout exceeded； try restarting transaction 更新数据量范围太大，导致锁表惨案"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 应产品需求，每日统计数据要重新刷一遍，于是用代码写了个接口，代码如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d40da21630c07bba3e1d42f0c5df2116.png)
- 谁知在执行这段代码时，刚好其他地方来了个修改的操作，我模拟了一下当时的场景，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8381145491d365eea0d9a92f1d5257f9.png)
- 因为我代码是加过事务的，此时还没执行完，没有提交事务，如果上面SQL和我的代码操作是同一条数据（因为有加索引，严格意义来说还不算表锁，所以操作同一条数据有问题），极有可能发生锁超时`Lock wait timeout exceeded; try restarting transaction`，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/df6609119477fad60af2f8795d0378e6.png)
## 反思
- 尽量避免长事务。我把事务去掉了，并记录好回滚方案。
- 当然调整获取锁的超时时间也能解决问题，只是本例不适用。