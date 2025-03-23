---
layout:					post
title:					"mysql limit优化"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- MySQL自超过百万条数据后使用limit查询发现会很慢了;那么该如何不通过分库分表的方案进行优化呢？答案还是加索引。
- 我这里就没有开慢日志查询去验证了，而是直接使用mysql的查询计划`explain`
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/bbcbaedbf61d19c2f303ca5d386f7d33.png)
>简单的介绍下explain结果的意思：
	-  id：SQL执行的顺序的标识,SQL从大到小的执行
	- select_type : 查询中每个select子句的类型
	- table:显示是属于哪张表的结果
	- type：表示MySQL在表中找到所需行的方式，又称“访问类型”。常用的类型有： ALL, index,  range, ref, eq_ref, const, system, NULL（从左到右，性能从差到好）
	- possible_keys：指出MySQL能使用哪个索引在表中找到记录，查询涉及到的字段上若存在索引，则该索引将被列出，但不一定被查询使用。
	- key：key列显示MySQL实际决定使用的键（索引）.
	- key_len:表示索引中使用的字节数，可通过该列计算查询中使用的索引的长度（key_len显示的值为索引字段的最大可能长度，并非实际使用长度，即key_len是根据表定义计算而得，不是通过表内检索出的）
	- ref:表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值
	- rows:表示MySQL根据表统计信息及索引选用情况，估算的找到所需的记录所需要读取的行数
	- Extra:包含MySQL解决查询的详细信息





- create_time字段我是加过索引的,可以看到order by它limit的时候就不会全表扫描了,而是使用了索引,效率很提高很多。

到这儿基本结束了，另外文章代码或者我理解有误的地方,希望能批评指出。