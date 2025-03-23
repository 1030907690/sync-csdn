---
layout:					post
title:					"mybatis pagehelper自定义count语句"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
### 背景
- 数据库里有120W的操作日志数据，已经查询不出来了。在`count`语句的时候就卡住了。最开始语句如下所示。
- 我想着加个带索引的键后面的查询语句会快些，所以加了`order by oper_id desc` 。(`/*keep orderby*/` 是啥意思，有兴趣的可以看[mybatis pagehelper count order by 不生效](https://sample.blog.csdn.net/article/details/119216433))，sql如下所示。

```c
select count(0) from ( /*keep orderby*/ select ...省略... order by oper_id desc ) tmp_count
```
- 这个sql感觉非常慢了，archery执行直接报`(3024, 'Query execution was interrupted, maximum statement execution time exceeded')`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7d0ab95abdded8ec57366ca0d51f3be3.png)
- 其实我想要的结果类似于这样的。

```c
SELECT count(0) FROM xxx_log order by oper_id desc 
```
### 解决方案
- 在pagehelper的文档中有自定义count语句的办法，[https://github.com/pagehelper/Mybatis-PageHelper/blob/master/wikis/zh/Changelog.md#504---2017-08-01](https://github.com/pagehelper/Mybatis-PageHelper/blob/master/wikis/zh/Changelog.md#504---2017-08-01)，只要我们在xml中定义好，执行count的时候就会走我们自定义的逻辑代码，如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/57fcf27748c39f75b4f65d49b07a81cb.png)
- 安装文档自定义了count代码`selectOperLogList_COUNT`（我查列表的方法就是`selectOperLogList`），如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/760da1a1945ba97e61eb80de0a0ce08a.png)
- 然后查看效果，果然走了我们自定义的count语句逻辑，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e11846ef49a879954741e30c91bafebb.png)
- 还引申出一个另类解决方案，假设我们知道该表的总条数，那么可以直接参数传进来，然后返回出去就可以了。

```c
<select id="selectOperLogList_COUNT" resultType="Long">
		SELECT #{count}
</select>
```
