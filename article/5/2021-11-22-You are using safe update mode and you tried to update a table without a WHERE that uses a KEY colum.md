---
layout:					post
title:					"You are using safe update mode and you tried to update a table without a WHERE that uses a KEY colum"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
## 具体报错

```bash
delete from xxx where xxx= 'xxx'	Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect.	0.016 sec
```
- 由于`sql_safe_updates`为`ON`，不加主键更改操作会报错。
- `show variables like 'SQL_SAFE_UPDATES';`查看状态
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b1aa2db4b4ed01b06558e7111abb4feb.png)
## 解决方案
### 第一种
- 执行命令`SET SQL_SAFE_UPDATES = 0;`修改下数据库模式

### 第二种
- 在SQL语句后面加上`and id>0`。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1cef84ab5be5a863d21a9796151ef8c3.png)


