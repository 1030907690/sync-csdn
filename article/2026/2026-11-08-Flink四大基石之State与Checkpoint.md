@[TOC](目录)

# 背景
- Flink State Backends默认使用 `HashMapStateBackend`，随着数据量增大，内存不太够用了。所以切换`RocksDB ` ，配置少量Managed内存，状态落到TaskManager 本地磁盘，大幅降低JVM堆压力，把JVM 堆内存占用降下来。
- 上面说切换到`RocksDB `,状态落到TaskManager 本地磁盘,我们知道内存和磁盘读写速度差距是很大的。如果我们对任务有计划内重启。那么重启时候状态需要从源头重新载入，磁盘相较于内存Job启动和Sink阶段很慢。如果我们开启Checkpoint，指定Checkpoint路径恢复，增量Checkpoint通过硬链接引用本机上已有的 SST 文件。恢复过程就很快。另外Checkpoint也适用于故障恢复。



# State 
- 在`conf/config.yaml`增加以下配置。
```yml
# 使用 RocksDB 状态后端，状态落盘，降低堆内存占用

state:
  backend:
    type: rocksdb       
    rocksdb:
      localdir: /home/xxx/software/flink-1.20.3/data/rocksdb-local

```
- 重启后就能看到使用了`Managed Memory`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e5b456e0e5a84d158945994a5a31639d.png)

- 关于`Managed Memory`配置如下(二选一)：
```
# 下面的配置二选一
taskmanager.memory.managed.size: 256mb
taskmanager.memory.managed.fraction: 0.1

```


# Checkpoint
- 在`conf/config.yaml`增加以下配置。

```yml
# 开启 checkpoint（如果作业还没开的话）
execution:
  checkpointing:
    storage: filesystem
    dir: file:///home/xxx/software/flink-1.20.3/data/flink-checkpoints   # 状态和 checkpoint 存储目录（改成你的实际路径）
    incremental: true           # 开启增量 checkpoint，减少 checkpoint 数据量
    interval: 10min              # 10 分钟一次 checkpoint
    num-retained: 3
    mode: EXACTLY_ONCE          # 精确一次语义
    timeout: 10min
    max-concurrent-checkpoints: 1    # 同一时刻最多 1 个 checkpoint 在做（unaligned 的硬性要求，默认即 1）
    min-pause: 30s                   # 上一个 checkpoint 结束后至少歇 30s 再触发下一个，防止背靠背连发
    tolerable-failed-checkpoints: 12  # 容忍 12 次 checkpoint 失败不重启作业
    externalized-checkpoint-retention: RETAIN_ON_CANCELLATION
    unaligned:
      enabled: true                    # 核心：barrier 可越过缓冲数据，checkpoint 时长与反压解耦——治 风暴期间对齐卡死
    aligned-checkpoint-timeout: 30s     #前 30s 先尝试对齐（省 I/O），超时自动降级 unaligned；注意：必须和 unaligned: 平级，且只在 unaligned.enabled=true 时生效

```


- 启动时要指定checkpoint路径，我用的是sql-client.sh启动命令如下：
```shell
./bin/sql-client.sh -D execution.state-recovery.path=file:///home/xxx/software/flink-1.20.3/data/flink-checkpoints/c0aef69e3e54a44a804cd37706eb4c31/chk-6 -f xxx.sql
```
- 指定checkpoint路径就会发现作业拓扑图很快就会完成。


- 另外checkpoint也适用于故障恢复，配置了重启策略。比如Job运行过程中OOM，前面的状态不会丢失。重启策略配置如下：
```
restart-strategy:
  type: fixed-delay
  fixed-delay: 
    attempts: 3
    delay: 3s

```


# 遇到的问题
- 双流Join的问题：在开启Rocksdb和Checkpoint后，修改一个分类表的数据同步更慢了，而且同步时间是与这条分类数据关联数据条数成正比。但是我又不能排除这个分类表数据一定不更新，基于数据量不算太大，改动频率很低，所以我开启了`unaligned`。




# 参考
- [https://nightlies.apache.org/flink/flink-docs-release-1.20/zh/docs/ops/state/state_backends/](https://nightlies.apache.org/flink/flink-docs-release-1.20/zh/docs/ops/state/state_backends/)
- [https://nightlies.apache.org/flink/flink-docs-release-1.20/zh/docs/ops/state/checkpoints/](https://nightlies.apache.org/flink/flink-docs-release-1.20/zh/docs/ops/state/checkpoints/)
- 豆包
- deepseek-v4-pro