---
layout:					post
title:					"postgresql 序列 - currval尚未定义"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- postgresql 序列：从1开始，最小是1，每次自增1，代码如下所示。
	- 需要自定义的参数
		- sequence_name ：定义序列名称。
```
create sequence sequence_name increment by 1 minvalue 1 no maxvalue start with 1;
```

- 如果在添加数据时报错：“currval尚未定义”。代码如下所示。
	- 需要自定义的参数
		- table_name：表名。
		- column_name：列名
		- sequence_name：序列名称
```
ALTER TABLE table_name ALTER COLUMN column_name SET DEFAULT nextval('sequence_name'::regclass);
```
