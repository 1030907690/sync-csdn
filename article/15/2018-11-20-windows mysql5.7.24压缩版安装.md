---
layout:					post
title:					"windows mysql5.7.24压缩版安装"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 里面没有`my.ini`文件，在根目录创建my.ini文件,内容如下:

```
[client]
	port=3306
	default-character-set=utf8
	[mysqld]
	character-set-server=utf8 
	#collation-server=utf8_unicode_ci
	basedir="D:/software/mysql-5.7.24-winx64"
	datadir="D:/software/mysql-5.7.24-winx64/data"

```
- 初始化mysql数据库
cmd运行:
```
mysqld --initialize-insecure --user=mysql
```
可能的异常:

```
2018-11-08T03:14:48.030809Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is
		 deprecated. Please use --explicit_defaults_for_timestamp server option (see doc
		umentation for more details).
		2018-11-08T03:14:48.032810Z 0 [ERROR] --initialize specified but the data direct
		ory has files in it. Aborting.
```
换成:

```
 mysqld --initialize-insecure --user=mysql --explicit_defaults_for_timestamp=true
```

- 安装mysql服务

```
mysqld install
```
运行后会看到服务里有mysql,就成功了。


- 其他命令

```
 删除服务
  sc delete mysql
```

