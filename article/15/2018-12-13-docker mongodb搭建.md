---
layout:					post
title:					"docker mongodb搭建"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 运行镜像

```
#即使没有mongo 4.0镜像run时会自动拉
docker run -p 27017:27017 --privileged=true -d --name some-mongo  -v /data/mongodb/datadir:/data/db -e MONGO_INITDB_ROOT_USERNAME=test -e MONGO_INITDB_ROOT_PASSWORD=xxx mongo:4.0
```
- 登录进去设置db的密码:

```
docker exec -i -t some-mongo /bin/bash
mongo --port 27017 -u "test" -p "xxx" --authenticationDatabase "admin"
```
- 切换到db并设置访问该db的用户

```
	#如果数据库不存在，则创建数据库，否则切换到指定数据库。
 	use game_server 
	db.createUser(
		 {
		   user: "test",
		   pwd: "xxx",
		   roles: ["readWrite"]
		 }
	)
```
- 最后用刚创建的帐号密码连接mongodb。
