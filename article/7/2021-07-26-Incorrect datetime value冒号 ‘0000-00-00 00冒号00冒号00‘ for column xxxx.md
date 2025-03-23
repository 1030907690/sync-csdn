---
layout:					post
title:					"Incorrect datetime value: ‘0000-00-00 00:00:00‘ for column xxxx"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 从测试环境数据导入到本地数据库报`Incorrect datetime value: '0000-00-00 00:00:00'`，报错详情如下所示。
[DTF] Data Transfer started
[DTF] 0> Getting tables
[DTF] 1> xx: Getting table structure
[DTF] 1> xxx: Fetching records
[DTF] 1> xx: Drop table
[DTF] 1> xx: Create table
[DTF] 1> xx: Transferring records
[ERR] 1> INSERT INTO `xxx` VALUES (xxxx
[ERR] 1> 1292 - Incorrect datetime value: '0000-00-00 00:00:00' for column 'create_time' at row 373
[DTF] Process terminated

## 问题分析
- 为什么会有`0000-00-00 00:00:00`呢？
> 官方文档上说明MySQL允许将’0000-00-00’保存为“伪日期”(如果不使用NO_ZERO_DATE SQL模式)。这在某些情况下比使用NULL值更方便(并且数据和索引占用的空间更小)。
## 解决方案
- 解决方案就是设置`sql_mode`，取消`NO_ZERO_DATE`。
- 我们先来看本地环境的sql_mode设置。使用`show variables like '%sql_mode%';`，结果如下。
 
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/217ec94423d0e22101f3cc5852363073.png)
>Value：ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION

- 然后再看测试环境的。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b3022654556c10b295ef782d191fb111.png)
- 对比下很容易发现，的确是没有`NO_ZERO_DATE`的。

- 现在我们修改mysql的`my.cnf`文件，修改`sql_mode`（如果没有就新增，放在[mysqld]下面），去掉`NO_ZERO_DATE`。代码如下所示。

```
sql_mode=ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bed33a331c1e7ffd570b43c64b08bfeb.png)
- 然后再导入，就能成功了，结果如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/745e886be3faf9a7def36301e7729d7d.png)
