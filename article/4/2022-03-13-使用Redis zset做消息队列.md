---
layout:					post
title:					"使用Redis zset做消息队列"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 按理来说，Redis做消息队列应该使用`Stream`。没错，但那是5.0及以上的功能，奈何公司用的是3.2.9的，没法用Stream。
- `PubSub`的消息又不持久化，所以选择了`zset`，不仅有序利用`score`特性还能做到延迟队列的效果。

## 实现思路
- 1、有一个线程不断轮询到时间的队列。要注意空轮询的问题。

```
... 省略...
  while (!Thread.interrupted() && !destroyFlag) {
... 省略...
}
```
 

- 2、查询到时间的redis数据，`zset score`实现这个功能。

```
Set<String> strings = stringRedisTemplate.opsForZSet().rangeByScore(queueName, 0, System.currentTimeMillis());
```
- 3、序列号成对象，抢占消息。

```
... 省略 ...
  // 有可能是集群，多个节点，设置抢占
        for (RedisQueueMessage redisQueueMessage : msgList) {
            // TODO 同一个消息可能被多个进程获取到，之后通过删除的方式竞争，那些没抢到的相当于白取了一次任务；可以用lua优化抢占这块
            //TODO 建议增加抢占日志
            if (remove(redisQueueMessage)) { // 为true 表示抢占到了
                return redisQueueMessage;
            }
        }
   ...省略..
```
- 4、这个时候就是处理消息了，为了应对其他消息，我用了`策略模式+模板方法`。

```
...省略...
RedisQueueProcessService redisQueueProcessService = adapterHandler(redisQueueMessage.getBeanName());
... 省略...
    private RedisQueueProcessService adapterHandler(String beanName) {
       return applicationContext.getBean(beanName, RedisQueueProcessService.class);
    }
```
5、执行真正的处理逻辑
```
 
    private void invokeHandler(RedisQueueMessage redisQueueMessage, RedisQueueProcessService redisQueueProcessService) {
        RedisQueueProcessResp result = null;
        try {
            //TODO 建议增加真正消费之前的日志
            result = redisQueueProcessService.handler(redisQueueMessage);
            ifFailAgainAddQueue(redisQueueMessage, result);
            //TODO 建议增加真正消费之后的日志
        } catch (Exception e) {
            //TODO 可以限制下重试次数，如果再失败，后续人工补偿
            // 执行出现异常重新加入队列
            push(redisQueueMessage);
            System.out.println("执行业务代码程序异常");
            //TODO 建议增加真正消费之后的日志，出异常的情况
            throw new RuntimeException("执行业务代码异常");
        }
    }
```
- 完整核心代码

```
 package com.springboot.sample.redis;


import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import com.springboot.sample.bean.RedisQueueMessage;
import com.springboot.sample.bean.RedisQueueProcessResp;
import com.springboot.sample.redis.process.RedisQueueProcessService;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationContext;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.converter.json.Jackson2ObjectMapperBuilder;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

import javax.annotation.PreDestroy;
import javax.annotation.Resource;
import java.io.IOException;
import java.util.List;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
/***
 * zzq
 * 2022年2月13日13:39:34
 * 延迟队列
 * */
@Component
public class DelayingQueueService implements InitializingBean {

    private static ObjectMapper mapper = Jackson2ObjectMapperBuilder.json().build();

    /** 是否销毁标记 volatile 保证可见性 **/
    private volatile boolean destroyFlag = false;

    @Resource
    private StringRedisTemplate stringRedisTemplate;

    @Resource
    private ApplicationContext applicationContext;

    // 设定空轮询最大次数
    private static final int SELECTOR_AUTO_REBUILD_THRESHOLD = 512;

    // deadline 以及任务穿插逻辑处理  ，业务处理事件可能是5毫秒
    private long timeoutMillis = TimeUnit.MILLISECONDS.toNanos(5);

    /**
     * 可以不同业务用不同的key
     */
    @Value("${redisQueue.name}")
    public String queueName;


    /**
     * 插入消息
     *
     * @param redisQueueMessage
     * @return
     */
    public Boolean push(RedisQueueMessage redisQueueMessage)  {
        Boolean addFlag = null;
        try {
            addFlag = stringRedisTemplate.opsForZSet().add(queueName, mapper.writeValueAsString(redisQueueMessage), redisQueueMessage.getDelayTime());
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
        return addFlag;
    }

    /**
     * 移除消息
     *
     * @param redisQueueMessage
     * @return
     */
    public Boolean remove(RedisQueueMessage redisQueueMessage) {
        Long remove = 0L;
        try {
            remove = stringRedisTemplate.opsForZSet().remove(queueName, mapper.writeValueAsString(redisQueueMessage));
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
        return remove > 0 ? true : false;
    }


    /**
     * 拉取最新需要
     * 被消费的消息
     * rangeByScore 根据score范围获取 0-当前时间戳可以拉取当前时间及以前的需要被消费的消息
     *
     * @return
     */
    public RedisQueueMessage dequeue() {
        Set<String> strings = stringRedisTemplate.opsForZSet().rangeByScore(queueName, 0, System.currentTimeMillis());
        if (strings == null) {
            return null;
        }
        List<RedisQueueMessage> msgList = strings.stream().map(msg -> {
            RedisQueueMessage redisQueueMessage = null;
            try {
                redisQueueMessage = mapper.readValue(msg, RedisQueueMessage.class);
            } catch (JsonProcessingException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return redisQueueMessage;
        }).collect(Collectors.toList());

        // 有可能是集群，多个节点，设置抢占
        for (RedisQueueMessage redisQueueMessage : msgList) {
            // TODO 同一个消息可能被多个进程获取到，之后通过删除的方式竞争，那些没抢到的相当于白取了一次任务；可以用lua优化抢占这块
            //TODO 建议增加抢占日志
            if (remove(redisQueueMessage)) { // 为true 表示抢占到了
                return redisQueueMessage;
            }
        }
        return null;
    }


    @Override
    public void afterPropertiesSet() throws Exception {
        Thread thread = new Thread("loop-redis-queue") {
            @Override
            public void run() {
                int selectCnt = 0;

                while (!Thread.interrupted() && !destroyFlag) {
                    long currentTimeNanos = System.nanoTime();

                    RedisQueueMessage redisQueueMessage = dequeue();
                    System.out.println("拉取的数据 " + redisQueueMessage);
                    if (!StringUtils.isEmpty(redisQueueMessage)) {
                        try {
                            RedisQueueProcessService redisQueueProcessService = adapterHandler(redisQueueMessage.getBeanName());

                            invokeHandler(redisQueueMessage,redisQueueProcessService);

                        }catch (Exception e){
                            e.printStackTrace();
                        }
                    }
                    selectCnt++;


                    // 解决空轮询问题
                    long time = System.nanoTime();
                    System.out.println("执行纳秒数" + (time - currentTimeNanos));
                    System.out.println(time + " -- " + (time - TimeUnit.MILLISECONDS.toNanos(timeoutMillis)) + "--" + currentTimeNanos);
                    // 当前时间减去阻塞使用的时间  >= 上面的当前时间
                    if (time - timeoutMillis >= currentTimeNanos) {
                        // 有效的轮询
                        selectCnt = 1;
                    } else if (SELECTOR_AUTO_REBUILD_THRESHOLD > 0 && selectCnt >= SELECTOR_AUTO_REBUILD_THRESHOLD) {
                        // 如果空轮询次数大于等于SELECTOR_AUTO_REBUILD_THRESHOLD 默认512
                        selectCnt = 1;
                        threadSleep();
                    }
                }
            }
        };
        thread.setDaemon(true);
        thread.start();
    }

    private void invokeHandler(RedisQueueMessage redisQueueMessage, RedisQueueProcessService redisQueueProcessService) {
        RedisQueueProcessResp result = null;
        try {
            //TODO 建议增加真正消费之前的日志
            result =  redisQueueProcessService.handler(redisQueueMessage);
            ifFailAgainAddQueue(redisQueueMessage, result);
            //TODO 建议增加真正消费之后的日志
        } catch (Exception e) {
            //TODO 可以限制下重试次数，如果再失败，后续人工补偿
            // 执行出现异常重新加入队列
            push(redisQueueMessage);
            System.out.println("执行业务代码程序异常");
            //TODO 建议增加真正消费之后的日志，出异常的情况
            throw new RuntimeException("执行业务代码异常");
        }
    }

    protected void ifFailAgainAddQueue(RedisQueueMessage redisQueueMessage, RedisQueueProcessResp result) {
        if (!StringUtils.isEmpty(result) && HttpStatus.OK.value() != result.getCode()) {
            //TODO 可以限制下重试次数，如果再失败，后续人工补偿
            // 错误要重新加入队列
            push(redisQueueMessage);
        }
    }


    private RedisQueueProcessService adapterHandler(String beanName) {
       return applicationContext.getBean(beanName, RedisQueueProcessService.class);
    }

    private void threadSleep() {
        try {
            System.out.println("睡眠了");
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }


    @PreDestroy
    public void destroy() throws Exception {
        System.out.println("应用程序已关闭");
        this.destroyFlag = true;
    }



}

```
## 执行效果
- 请求地址 http://localhost:8080/redis/sendMessage?msg=%E5%BC%A0%E4%B8%89&delay=3，delay=3延迟了3秒
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b452d0f8b54c864d8ccd288c282344b8.png)


## 结语和代码
- 核心逻辑就是一个线程不断轮询redis，有数据的时候先抢占，抢到了就找对应的处理类，执行业务代码。这中间可以记录下消费日志，方便人工补偿和排查问题。
- 完整代码地址：`https://gitee.com/apple_1030907690/spring-boot-kubernetes/tree/v1.0.1`