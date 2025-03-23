---
layout:					post
title:					"docker redis搭建"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
 
- 事先在`/data/redis/conf`路径先创建配置文件redis.conf,找一个redis.conf的样例,主要就是设置下redis密码之类的`requirepass root`
```bash
docker run -d -p 6379:6379 -v /data/redis/conf:/usr/local/etc/redis --name redis-standard redis redis-server /usr/local/etc/redis/redis.conf
```
- 进去查看一下

```bash
 docker exec -i -t redis-standard /bin/bash
```

- 登录进redis

```bash
redis-cli -a root
或者
redis-cli        
auth root
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5501b10007a4bf788e9e14f01c37817d.png)
- 这样简单的单机版redis就算完成了，参考资料可以参考[docker hub](https://hub.docker.com/_/redis?tab=description) 