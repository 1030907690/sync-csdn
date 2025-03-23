---
layout:					post
title:					"Criteria already contains 'xxx ："
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- mongodb查询报错详情如下:

```
org.springframework.data.mongodb.InvalidMongoDbApiUsageException: Due to limitations of the com.mongodb.BasicDocument, you can't add a second '_id' expression specified as '_id : Document{{$in=[1000090]}}'. Criteria already contains '_id : 1000090'.
```

- 报错的原因是因为前面已经用了`_id`字段查询了又用了`_id`,语句如下:

```
Criteria.where("_id").in(id).and("_id").in(userIdArray);
```
- 解决方案可以使用`andOperator`语句

```
new Criteria().andOperator(Criteria.where("_id").is(id),
                            Criteria.where("_id").in(userIdArray));
```
