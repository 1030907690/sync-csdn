---
layout:					post
title:					"升级到MySQL8 GROUP BY的异常"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 异常详情
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9ead555a78a7473babbdfa5ca4ab249a.png) 
- **1055 - Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'xxx.xxx.value' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by**
 

## 异常原因
- 在严格模式下（MySQL8默认开启），对于group by聚合操作，若使用的列没有在group by中出现，那么这个SQL就是不合法的。

## 解决方案
### 方案一
- 报错的列加入`any_value`函数，返回一个特定列的任意值。这个函数特别适用于那些不需要确定具体哪一个值的场景，可以避免group by时出现的错误。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/73a9b4a9cbb34828872b08ecc3afed64.png)
### 方案二
- 先查询出当前`sql_mode`，然后删除其中`ONLY_FULL_GROUP_BY`，执行SQL重新设置全局sql_mode。如下图所示。
![请添加图片描述](https://i-blog.csdnimg.cn/direct/90b25e1e3faf4b5983c5da0333afd669.png)
- 设置全局sql_mode语句如下：

```shell
set global sql_mode=’XXXX';
```
- **注：重启后失效，适用于不方便重启MySQL的情况。**

### 方案三
- 先查询一下当前`sql_mode`，在原基础上删除sql_mode删除ONLY_FULL_GROUP_BY,放到MySQL配置文件[mysqld]里,重启MySQL。结果如下图。
![请添加图片描述](https://i-blog.csdnimg.cn/direct/7022f71cb0a54ccbbb7e4802a92952f0.png)
![请添加图片描述](https://i-blog.csdnimg.cn/direct/5fdee57977244088960998a016723603.png)



![请添加图片描述](https://i-blog.csdnimg.cn/direct/969182e1ec9441b1bcfadd1d604097c6.png)

- 使用的命令：

```python
select @@GLOBAL.sql_mode # 先查询当前的sql_mode
```

- MySQL配置文件中新增一行：

```python
[mysqld]
...省略...
sql_mode='xxx' #在原基础上删除sql_mode删除ONLY_FULL_GROUP_BY
```


















