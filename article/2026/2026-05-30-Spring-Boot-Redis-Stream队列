@[TOC](目录)
# 简介
- Redis Stream 是 Redis 5.0+ 新增的轻量级消息队列，队列数据持久化、有序、可回溯。之前使用 Pub/Sub（无持久化、无消费组）、 List（无 ACK、无分组）作为队列的诸多问题，用Stream都能很好解决。

## 核心概念

| 名词 | 说明 |
| --- | --- |
|Stream (流) |  Redis Stream队列核心的数据结构，一个只允许追加（Append-only）的日志文件  |
|Consumer Group (消费组) |  允许多个消费组消费同一个stream，广播机制，那么每个消费组都会消费这个消息一次  |
| Consumer （消费者） |   每个消费组里支持多个消费者，同一个组里会有一个消费者拿到消息  |
| Record Id （消息ID） |  默认为Redis 服务器本地时间戳（毫秒级）+ 序列号 ，例如1780140313854-0 |
|Pending Entries List (PEL，待处理条目) |     已收到但未确认（ACK）的消息列表。Redis 会记录哪些消息被哪个消费者读了，但还没收到 ACK。这保证了消息不丢失  |
|ACK (确认机制) |   消费者处理完消息后，发送XACK已完成。此时消息会从该消费者的 PEL 中移除，表示消费成功 |
| Claim（认领） 机制   |  对于服务器宕机或消费异常，消息处于PEL中，允许一个健康的消费者强行把一个死掉的消费者手里积压且长期未确认的消息“夺过来”，变成自己的任务去处理 |



# 准备
- JDK 21
- Redis 7.0.15


# 核心代码
- 队列配置`RedisStreamConfig`
```java
package com.zzq.config;


import com.zzq.listener.MyStreamConsumer;
import com.zzq.utils.MachineInfoUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.stream.Consumer;
import org.springframework.data.redis.connection.stream.MapRecord;
import org.springframework.data.redis.connection.stream.ReadOffset;
import org.springframework.data.redis.connection.stream.StreamOffset;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.stream.StreamMessageListenerContainer;

import java.time.Duration;

/**
 * @description:
 * @author: Zhou Zhongqing
 * @date: 3/19/2026 10:28 PM
 */
@Configuration
public class RedisStreamConfig {

    private final Logger log = LoggerFactory.getLogger(RedisStreamConfig.class);
    @Autowired
    private MyStreamConsumer myStreamConsumer;

    public static final String STREAM_KEY = "my-stream";

    public static final String GROUP_NAME = "user-group";

    @Bean
    public StreamMessageListenerContainer<String, MapRecord<String, String, String>> streamMessageListenerContainer(StringRedisTemplate stringRedisTemplate) {
        //  容器选项配置
        // 泛型改为 MapRecord<String, String, String>
        StreamMessageListenerContainer.StreamMessageListenerContainerOptions<String, MapRecord<String, String, String>> options =
                StreamMessageListenerContainer.StreamMessageListenerContainerOptions
                        .builder()
                        .batchSize(10)
                        .pollTimeout(Duration.ofSeconds(2))
                        .build();

        //  初始化容器
        StreamMessageListenerContainer<String, MapRecord<String, String, String>> container =
                StreamMessageListenerContainer.create(stringRedisTemplate.getRequiredConnectionFactory(), options);

        // 消费组配置 (重点)
        // 自动创建消费组的健壮性处理
        createGroupSafely(stringRedisTemplate);

        //  注册消费者
        container.receive(
                Consumer.from(GROUP_NAME, MachineInfoUtil.getHostName()), // 消费组名和消费者实例名
                StreamOffset.create(STREAM_KEY, ReadOffset.lastConsumed()), // 从最后一次消费的位置开始
                myStreamConsumer
        );

        //  启动容器
        container.start();
        return container;
    }

    private void createGroupSafely(StringRedisTemplate stringRedisTemplate) {
        try {
            stringRedisTemplate.opsForStream().createGroup(STREAM_KEY, GROUP_NAME);
        } catch (Exception e) {
            // 生产环境下，如果组已存在会抛异常，这里直接捕获忽略即可
            log.info("消费组已存在或初始化跳过: {}", e.getMessage());
        }
    }


}
```
- 监听消费 `MyStreamConsumer`
```java
package com.zzq.listener;


import com.zzq.config.RedisStreamConfig;
import com.zzq.utils.RedisStreamUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.connection.stream.MapRecord;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.stream.StreamListener;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Map;

/**
 * @description:
 * @author: Zhou Zhongqing
 * @date: 3/19/2026 10:29 PM
 */
@Component
public class MyStreamConsumer implements StreamListener<String, MapRecord<String, String, String>> {

    private static final Logger log = LoggerFactory.getLogger(MyStreamConsumer.class);

    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @Autowired
    private RedisStreamUtil redisStreamUtil;

    @Override
    public void onMessage(MapRecord<String, String, String> record) {
        Map<String, String> map = record.getValue();
        log.info("收到消息: {}", map);

        // TODO 业务处理
        stringRedisTemplate.opsForStream().acknowledge(RedisStreamConfig.STREAM_KEY, RedisStreamConfig.GROUP_NAME, record.getId());
    }


}
```


- 如果消费异常的兜底处理，处理`PEL`的数据 `ResendPendingTask`

```java
package com.zzq.task;

import com.zzq.config.RedisStreamConfig;
import com.zzq.utils.MachineInfoUtil;
import com.zzq.utils.RedisStreamUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Range;
import org.springframework.data.redis.connection.stream.MapRecord;
import org.springframework.data.redis.connection.stream.PendingMessages;
import org.springframework.data.redis.connection.stream.PendingMessagesSummary;
import org.springframework.data.redis.connection.stream.RecordId;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.List;
import java.util.Map;

/**
 * @author zzq
 * @since 2026/03/21 14:35:14
 */
@Component
public class ResendPendingTask {

    private static final Logger log = LoggerFactory.getLogger(ResendPendingTask.class);

    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @Autowired
    private RedisStreamUtil redisStreamUtil;

    @Scheduled(fixedRate = 10000)
    public void resendPendingMessages() {

        PendingMessagesSummary summary = stringRedisTemplate.opsForStream().pending(RedisStreamConfig.STREAM_KEY, RedisStreamConfig.GROUP_NAME);

        if (summary != null && summary.getTotalPendingMessages() > 0) {
            // 读取前 10 条 Pending 消息
            PendingMessages pendingMessages = stringRedisTemplate.opsForStream()
                    .pending(RedisStreamConfig.STREAM_KEY, RedisStreamConfig.GROUP_NAME, Range.unbounded(), 10);

            pendingMessages.forEach(message -> {
                // 获取消息 ID 和已投递次数
                RecordId id = message.getId();
                Duration elapsed = message.getElapsedTimeSinceLastDelivery();

                long deliveryCount = message.getTotalDeliveryCount(); // 消息被投递的次数


                // 3. 如果消息超过 30 秒还没处理完，说明原消费者可能挂了，重新处理
                if (elapsed.getSeconds() > 30) {


                    // 这里可以重新读取消息内容并执行业务，或者使用 XCLAIM 转移给其他消费者

                    // 核心优化：使用 claim 转移拥有权并直接获取消息内容
                    // 这相当于 Redis 的 XCLAIM 命令，它会重置该消息的 idle 时间，防止其他节点并发争抢
                    List<MapRecord<String, Object, Object>> claimedRecords = stringRedisTemplate.opsForStream().claim(
                            RedisStreamConfig.STREAM_KEY,
                            RedisStreamConfig.GROUP_NAME,
                            MachineInfoUtil.getHostName(), // 变成当前兜底消费者的名字
                            Duration.ofSeconds(29), // 期望的 idle 时间再去强占
                            id
                    );

                    if (CollectionUtils.isEmpty(claimedRecords)) {
                        return; // 说明可能被其他并发线程抢先处理了
                    }


                    MapRecord<String, Object, Object> valueMapRecord = claimedRecords.stream().findFirst().get();

                    // 防毒丸死循环死锁,先claim保证ack时消费者一致
                    // 如果一条消息连续被捞起来处理了 5 次都无法成功 ACK，说明它是死信（比如格式错误、业务脏数据），执行XCLAIM了算处理1次
                    if (deliveryCount > 5) {

                        log.error("【死信报警】消息连续投递异常超过5次，强行确认并人工接入! ID: {}", valueMapRecord.getId());
                        // 生产环境规范：建议在这里将其记录到 MySQL 死信表或者发送钉钉通知，然后强制 ACK，把道路让给后面的消息
                        stringRedisTemplate.opsForStream().acknowledge(RedisStreamConfig.STREAM_KEY, RedisStreamConfig.GROUP_NAME, valueMapRecord.getId());

                        return;
                    }


                    try {

                        Map<String, String> value = redisStreamUtil.convert(valueMapRecord.getValue());

                        log.info("重新处理消息: {}", value);

                        // TODO: 你的实际业务处理逻辑

                        // 处理成功，确认消息
                        stringRedisTemplate.opsForStream().acknowledge(
                                RedisStreamConfig.STREAM_KEY,
                                RedisStreamConfig.GROUP_NAME,
                                valueMapRecord.getId()
                        );
                    } catch (Exception e) {
                        log.error("处理单条 Pending 消息失败, ID: " + valueMapRecord.getId(), e);
                        // 这里可以做重试次数累加，如果超过 3~5 次一直失败，建议人工介入或进入死信，防止死循环
                    }


                }
            });
        }
    }


}

```

# 验证
- 正常情况,`MyStreamConsumer`能正常处理消息
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/497c17a17bf34d5bafb2c925e687b8ad.png)
- 异常情况，`MyStreamConsumer`未ACK，查看`ResendPendingTask`能处理成功就是闭环的，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0dcc54b776d5487ebb4d6572236958d5.png)

# 小结
- 搞清楚几个概念，实现起来还是很容易的，遗憾的是Redis Stream 原生确实不支持延迟队列，我尝试过改造业务代码代码，但是很别扭遂放弃。如果用Redis做延迟队列首选应还是用`zset`。




# 本文源码地址
- [https://github.com/1030907690/redis-stream-sample](https://github.com/1030907690/redis-stream-sample)


# 参考

- [https://www.bilibili.com/video/BV13R4y1v7sP?p=24](https://www.bilibili.com/video/BV13R4y1v7sP?p=24)
- Gemini AI