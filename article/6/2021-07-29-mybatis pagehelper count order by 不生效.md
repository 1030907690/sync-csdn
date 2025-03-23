---
layout:					post
title:					"mybatis pagehelper count order by 不生效"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 有一条复杂的SQL语句，涉及子查询内部排序`order by`。发现`mybatis pagehelper`在`count`的时候会把order by删除。
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1e3246fd9bb9559f6395e6a6c6ef2388.png)
- 从上图来看`order by`是被过滤掉了。


## 解决方案
- 在原sql增加`/*keep orderby*/`解决。
- 我们可以在源码上答案，知道为什么这样做？
- 定位到`CountSqlParser#getSmartCountSql`方法。

```
public static final String KEEP_ORDERBY = "/*keep orderby*/";
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4933d6d2d30ac2a9624ad84c5ba48173.png)
- `getSimpleCountSql`方法是直接拼接sql。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/709232668fae94cbf2d3a4b5915b8597.png)

- 从上面源码可得知，sql内容中如果包含`/*keep orderby*/`这个字符串那么count的时候就不会修改原内容。

- 在xml中增加`/*keep orderby*/`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2f6da388551c6c4cd72dcb0bb45088c4.png)

- 重启再次请求`order by`生效了，效果如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/57b70566e9932a63fbaab12aae740395.png)
