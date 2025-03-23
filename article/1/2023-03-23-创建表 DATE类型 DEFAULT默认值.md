---
layout:					post
title:					"创建表 DATE类型 DEFAULT默认值"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- date类型直接用`CURRENT_TIMESTAMP或curdate()`会报错。是因为在MySQL默认你输入的是一个常量，而不能是一个表达式，如果必须要使用表达式则应该将该表达式整个用小括号包括起来。

- `(curdate())`，DDL语句显示如下
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/641ec81e7e781b23cda29ec30cf08899.png)

- 参考： [https://blog.51cto.com/u_15127598/4357542](https://blog.51cto.com/u_15127598/4357542)