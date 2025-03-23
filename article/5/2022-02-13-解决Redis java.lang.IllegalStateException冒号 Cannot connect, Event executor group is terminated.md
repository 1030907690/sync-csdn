---
layout:					post
title:					"解决Redis java.lang.IllegalStateException: Cannot connect, Event executor group is terminated"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 问题产生背景
- 写了个基于`zset`的消息队列（因为公司redis还是3.2.9的，没法用stream），然后有个线程一直轮询取数据。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b40e7f817205b346e0eb3ab7b8ff8dcf.png)

- 然后我关闭应用时可能会报`Cannot connect, Event executor group is terminated`，如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/eacbf8d2f2a31bacb0685f5eeda05cc9.png)

```
 Exception in thread "loop-redis-queue" java.lang.IllegalStateException: Cannot connect, Event executor group is terminated.
	at io.lettuce.core.AbstractRedisClient.initializeChannelAsync(AbstractRedisClient.java:283)
	at io.lettuce.core.RedisClient.connectStatefulAsync(RedisClient.java:314)
	at io.lettuce.core.RedisClient.connectStandaloneAsync(RedisClient.java:271)
	at io.lettuce.core.RedisClient.connect(RedisClient.java:204)
	at org.springframework.data.redis.connection.lettuce.StandaloneConnectionProvider.lambda$getConnection$1(StandaloneConnectionProvider.java:113)
	at java.util.Optional.orElseGet(Optional.java:267)
	at org.springframework.data.redis.connection.lettuce.StandaloneConnectionProvider.getConnection(StandaloneConnectionProvider.java:113)
	at org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory$SharedConnection.getNativeConnection(LettuceConnectionFactory.java:1110)
	at org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory$SharedConnection.getConnection(LettuceConnectionFactory.java:1091)
	at org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory.getSharedConnection(LettuceConnectionFactory.java:872)
	at org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory.getConnection(LettuceConnectionFactory.java:347)
	at org.springframework.data.redis.core.RedisConnectionUtils.doGetConnection(RedisConnectionUtils.java:134)
	at org.springframework.data.redis.core.RedisConnectionUtils.getConnection(RedisConnectionUtils.java:97)
	at org.springframework.data.redis.core.RedisConnectionUtils.getConnection(RedisConnectionUtils.java:84)
	at org.springframework.data.redis.core.RedisTemplate.execute(RedisTemplate.java:212)
	at org.springframework.data.redis.core.RedisTemplate.execute(RedisTemplate.java:185)
	at org.springframework.data.redis.core.AbstractOperations.execute(AbstractOperations.java:96)
	at org.springframework.data.redis.core.DefaultZSetOperations.rangeByScore(DefaultZSetOperations.java:197)
	at com.springboot.sample.redis.DelayingQueueService.pop(DelayingQueueService.java:88)
	at com.springboot.sample.redis.DelayingQueueService$1.run(DelayingQueueService.java:124)

```
## 问题分析
- 我查到GitHub有在说这个问题，[https://github.com/lettuce-io/lettuce-core/issues/1399](https://github.com/lettuce-io/lettuce-core/issues/1399)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/53a09cf036607ee9d0f8f16fd8a6a569.png#pic_center)
- 就说程序关闭的使用不要再去连redis了，得自己处理。

## 解决方案
- Spring有对关闭程序，销毁bean回调的扩展，例如实现`DisposableBean接口`或者 使用`@PreDestroy注解`。@PreDestroy注解被调用早于DisposableBean接口，我用的@PreDestroy。
- 增加销毁标记
```
    /** 是否销毁标记 volatile 保证可见性 **/
    private volatile boolean destroyFlag = false;
```
- 修改标记
```
    @PreDestroy
    public void destroy() throws Exception {
        System.out.println("应用程序已关闭");
        this.destroyFlag = true;
    }
```
- 然后在轮询的地方加入判断

```
...省略...
while (!Thread.interrupted() && !destroyFlag) {
...省略...
```

- 我去掉线程睡眠，测试了大约5次，没有再报异常。结果如下gif图。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3f1713b8c62a962b513aeabb99d9bd51.gif#pic_center)

