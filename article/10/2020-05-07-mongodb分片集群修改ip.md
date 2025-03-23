---
layout:					post
title:					"mongodb分片集群修改ip"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
 @[TOC](目录)
 ### 背景
 - 因为是恢复的镜像，服务器ip全变了，所以就需要修改ip了。
- 我分片集群构成:3个Config servers  ；1个分片复制集(3个节点)；1个路由
- 要注意开防火墙端口哦；后面就不在赘述了。
- 分片集群3个角色，修改顺序是`Config servers -> Shard -> Router` 

### 修改`Config servers` ip
- 以`standlone`模式启动一个`Config servers`，`--dbpath`的值是我之前配置文件里db存储路径
```bash
/root/software/mongodb-linux-x86_64-rhel70-4.0.13/bin/mongod  --port 37017 --dbpath    /home/DB-DATA/mongo_config-0
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/144ee7ad486d7a5735bcf079ed868383.png)

- 到另外一个控制台中登录config节点

```bash
/root/software/mongodb-linux-x86_64-rhel70-4.0.13/bin/mongo --port 37017
```

```bash
use local
db.system.replset.find()
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/15cc45fa1479aa647b04774d2215fbbf.png)

```bash
cfg = db.system.replset.findOne({_id: 'configs'})
cfg.members[0].host = "172.31.28.85:37017"
cfg.members[1].host = "172.31.28.85:37018"
cfg.members[2].host = "172.31.28.85:37019"
db.system.replset.update({_id: 'configs'}, cfg)
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e9aad43b61fa79e1c672555cd5a85fa4.png)

- 再查询看看是否修改成功
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c294b87af6e60143a9323eaec66f8e39.png)
- 然后就是另外的`Config servers`节点了；依然是standlone模式启动，另一个控制台登录进去修改就行了。

-  最后启动全部`Config servers`节点，选举成功的
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5d242775f9ebe9059b5e7f4a5fcade81.png)
- 登录到Config servers `primary`节点，修改分片信息
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e5f2b5a51a148b198739d39b7bdcc176.png)

```bash
  /root/software/mongodb-linux-x86_64-rhel70-4.0.13/bin/mongo --port 37017 -u root -p  xxx --authenticationDatabase "admin"
  use config
  cfg=db.shards.findOne({_id:'rs1'})
  cfg.host="rs1/172.31.28.85:27017,172.31.17.101:27018,172.31.17.101:27019"
  db.shards.update({_id:'rs1'},cfg)
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ea9123760bcd769ea7a46966f6d67d35.png)


### 修改`shard` ip
- 依旧是standlone模式启动，然后登录进去
```bash
/root/software/mongodb-linux-x86_64-rhel70-4.0.13/bin/mongod  --port 27017 --dbpath  /home/DB-DATA/mongodb-0/
```

```bash
/root/software/mongodb-linux-x86_64-rhel70-4.0.13/bin/mongo --port 27017
```
- 修改`Config servers`配置信息

```bash
use admin
db.system.version.find()
db.system.version.update({"_id" : "shardIdentity"},{"$set":{"configsvrConnectionString" : "configs/172.31.28.85:37017,172.31.28.85:37018,172.31.28.85:37019"}})
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e6cd73e17a15f21cd18567ab8ddcd58a.png)
- 修改`replica set`的配置信息, replica set的信息都保存在local数据库的system.replset集合中

```bash
 use local
 cfg = db.system.replset.findOne({_id: 'rs1'})
 cfg.members[0].host="172.31.28.85:27017"
 cfg.members[1].host="172.31.17.101:27018"
 cfg.members[2].host="172.31.17.101:27019"
 db.system.replset.update({_id:'rs1'},cfg)
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/21d8c9deed1712e4a12aaeb6fc8f016d.png)
- 依然还是和上面`Config servers`一样的对其他shard节点进行类似的操作
- 最后节点启动起来，看到主节点，一般就成功了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7c88b8195b766e9840d6548fa865e770.png)
### 路由（router）节点
- 修改地址
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4930d3a1ce40c87fb7efee4e22e517b2.png)
- 启动路由，登录测试成功
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4ffd8c51c8502658e53f3e51d147e642.png)



### 参考
[https://blog.csdn.net/lengchanguo/article/details/81482737](https://blog.csdn.net/lengchanguo/article/details/81482737)
