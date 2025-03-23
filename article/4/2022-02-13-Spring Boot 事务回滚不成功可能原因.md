---
layout:					post
title:					"Spring Boot 事务回滚不成功可能原因"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
#### 1、是否使用`EnableTransactionManagement`注解
#### 2、被调用的方法是否直接（注解方式间接的方法不行哦）使用注解（`Transactional`，注意Transactional注解默认只能拦截`RuntimeException和Error`，源码在`DefaultTransactionAttribute#DefaultTransactionAttribute`）事务或者方法内部编程式事务
####  3、使用`Transactional注解`方法内`不要捕获异常`，即使需要捕获，也必须再抛出。
#### 4、检查数据库表是否是`支持事务`的引擎(今天我卡在这里)。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7793ec884eff4fbd219051487aaab1db.png)
- 明明看着事务源码进入了回滚代码(源码在`TransactionAspectSupport#invokeWithinTransaction`)，数据依然保存了，就很神奇。
- 后面查到有可能是存储引擎问题，一对比，发现我以前建的表是`MyISAM`存储引擎，不支持事务的，汗颜啊。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3a86c6a74932ff87f59bc841cc3d78dc.png#pic_center)
