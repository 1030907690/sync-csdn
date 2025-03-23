---
layout:					post
title:					"mysql 不等于(!=) 数字无效，无视Null值的“小坑“"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 问题背景
- 例如我现在有一张简单的`t_users`表，表结构如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fba68570501f9a51034f33199510254d.png)

- 后续随着功能增加，新增加一个字段，判断这个人是不是vip用户（0 - 不是  1 - 是vip），修改后表结构如下。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a02fc4a5ad7bf77cb086525c577ee138.png)
- 注意，之前数据库我已有2条数据，如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e7c70719c500a7e170b8e5bf05564b5c.png)

- 后面又注册了一个新用户，数据如下所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2f8c80e921571cbfaccc4b5e8da1285c.png)
- 好了，然后我现在想找一下`不是vip的用户`，使用如下SQL。

```
SELECT * FROM `t_users` where is_vip != 1;
```
- 结果如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e6437f3a23a5cdac035ed76dcf62dd3e.png)
- 这就很尴尬了，按照一般程序的逻辑不等于1，本例中为`0`和`Null`的数据都应该查询出来。结果却只有为数字的0查出来，为Null的被过滤了。

## 原因
- `在mysql中，Null不能直接用算术运算符进行比较值`。

## 解决方案
### 第一种方案：使用OR
- 增加或者是等于NULL的，SQL和执行效果如下所示。

```
SELECT * FROM `t_users` where (is_vip != 1 or is_vip is NULL);
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/feb7f2873a92fe5b46afcefcc8e8f8e5.png)
### 第三种方案：使用IFNULL函数
- 使用IFNULL函数，如果为NULL就让它返回0，就认为不是vip，SQL和执行结果如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/aee5e2aca42c7ce7d5b31e5baea73ff1.png)

### 第三种方案：设置默认值
- 先修改表结构，设置字段为空时的默认值。比如本例，如果在程序中没有设置该值，给它默认为0，不是vip，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c8f2d4c463c1c2c0b2b16e33ea7b50f8.png)
- 然后修复老数据，本例中可以把为Null的数据设置为0，不是vip，使用如下SQL。

```
UPDATE t_users set is_vip = 0 WHERE is_vip is NULL;
```
- 再执行查询就能够得到正确的结果了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3b941aac2055b3ccdf1d5fbbfa405aa3.png)

