---
layout:					post
title:					"MySQL LIMIT + order by limit n,m 和 limit n的小坑"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)

## 背景
- 场景：数据刚刚初始化，`order by的字段值一样`，想获取列表的第一条数据，但是发现`limit`后不是第一条。
## 看数据
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7a95216e3588b727cadb74718aa270aa.png)
- 此时有3条数，id分别为38 、39、40。 
### limit n 
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2355baee85f799ba67cf78d175ad5780.png)
- 此时查询到的数据是id为40的。
### limit n,m
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e83f9669cd57acf2a074c8f080c00ae3.png)

 ### 问题
 > 注意：问题发生的场景 `order by`的两个值是相等的。然后`limit`
- 其实我要的是id为`39`那条数据，但我取一条的时候总是返回了id为`40`的数据。
- 这个问题是在排序字段数据内容相同的情况下出现，而且不稳定。
- 有可能下一页还会看到前一页的数据。


## 解决方案

- 查了一圈，还是以官方文档为准[https://dev.mysql.com/doc/refman/5.7/en/limit-optimization.html](https://dev.mysql.com/doc/refman/5.7/en/limit-optimization.html)
### 第一种：增加排序字段索引，多个字段增加联合索引
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ffa41c048536bf9d8c97ece82cd3c397.png)
- 增加索引
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5b77a425df3c4dd3b45838f6b87c3271.png)

- 查询结果
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bbf1ef273c5f5b2f4d1424d4a79d862b.png)

### 第二种：排序增加一个唯一字段，例如id，获得稳定排序
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9a1cf70f32ab15e93f5883c07da6549e.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6cd81ee1d6021b55faa77644a7924fb1.png)
### 第三种方式：代码获取第一条数据
- 这是我目前使用的方式，因为我只需要第一条诉，我查询了列表（取消了limit），然后Java代码获取列表的第一条。