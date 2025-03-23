---
layout:					post
title:					"flume+kafka+storm整合"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
flume采集数据

kafka做消息队列（缓存）

storm做流式处理

flume版本 apache-flume-1.7.0-bin

kafka版本 kafka_2.11-0.10.1.0（要注意的是有些flume的版本和kafka的版本不兼容，flume采集的数据无法写入到kafka的话题中去，我在这里被坑过）

storm版本 apache-storm-0.9.2-incubating

一、配置（必须先安装zookeeper）

flume配置：

在conf文件夹下新建demoagent.conf文件

（1）监听端口配置

A simple example 

# example.conf: A single-node Flume configuration

# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source
a1.sources.r1.type = netcat
a1.sources.r1.bind = localhost
a1.sources.r1.port = 44444

# Describe the sink
a1.sinks.k1.type = logger

# Use a channel which buffers events in memory
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100

# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
  （2）命令监听程序

# example.conf: A single-node Flume configuration

# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source       netcat 
a1.sources.r1.type = exec
a1.sources.r1.command = tail -f /home/zzq/flumedemo/test.log
a1.sources.r1.port = 44444
a1.sources.r1.channels = c1

# Describe the sink
a1.sinks.k1.type = logger

# Use a channel which buffers events in memory
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100

# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
 （3）flume 和 kafka整合

# example.conf: A single-node Flume configuration

# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source       netcat 
a1.sources.r1.type = exec
a1.sources.r1.command = tail -f /home/zzq/flumedemo/test.log
a1.sources.r1.port = 44444
a1.sources.r1.channels = c1


# Describe the sink
#a1.sinks.k1.type = logger

# Use a channel which buffers events in memory
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100




a1.sinks.k1.type = org.apache.flume.sink.kafka.KafkaSink
a1.sinks.k1.kafka.topic = testKJ1
a1.sinks.k1.kafka.bootstrap.servers = weekend114:9092,weekend115:9092,weekend116:9092
a1.sinks.k1.kafka.flumeBatchSize = 20
a1.sinks.k1.kafka.producer.acks = 1
a1.sinks.k1.kafka.producer.linger.ms = 1
a1.sinks.ki.kafka.producer.compression.type = snappy


# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
我们现在要用的就是第3种flume 和 kafka整合，我们将这个内容放到demoagent.conf文件

[zzq@weekend110 conf]$ cat demoagent.conf 
# example.conf: A single-node Flume configuration

# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source       netcat 
a1.sources.r1.type = exec
a1.sources.r1.command = tail -f /home/zzq/flumedemo/test.log
a1.sources.r1.port = 44444
a1.sources.r1.channels = c1


# Describe the sink
#a1.sinks.k1.type = logger

# Use a channel which buffers events in memory
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100




a1.sinks.k1.type = org.apache.flume.sink.kafka.KafkaSink
a1.sinks.k1.kafka.topic = testKJ2
a1.sinks.k1.kafka.bootstrap.servers = weekend110:9092
a1.sinks.k1.kafka.flumeBatchSize = 200
a1.sinks.k1.kafka.producer.acks = 1
a1.sinks.k1.kafka.producer.linger.ms = 1
a1.sinks.ki.kafka.producer.compression.type = snappy


# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
配置kafka：

vim config/server.properties 
broker.id=1
zookeeper.connect=weekend114:2181,weekend115:2181,weekend116:2181
加入id和zookeeper地址（我的是zookeeper集群）

配置storm：

修改配置文件storm.yaml

#所使用的zookeeper集群主机
storm.zookeeper.servers:
     - "weekend114"
     - "weekend115"
     - "weekend116"
#nimbus所在的主机名
nimbus.host: "weekend114"
supervisor.slots.ports
-6701
-6702
-6703
-6704
-6705

二、启动

       （1）、启动strom

在nimbus主机上
nohup ./storm nimbus 1>/dev/null 2>&1 &
nohup ./storm ui 1>/dev/null 2>&1 &

在supervisor主机上
nohup ./storm supervisor 1>/dev/null 2>&1 &
   （2）启动kafka

在每一台节点上启动broker
bin/kafka-server-start.sh config/server.properties
kafka其他实用操作：

5、在kafka集群中创建一个topic
bin/kafka-topics.sh --create --zookeeper weekend114:2181 --replication-factor 3 --partitions 1 --topic order


6、用一个producer向某一个topic中写入消息
bin/kafka-console-producer.sh --broker-list weekend110:9092 --topic order

7、用一个comsumer从某一个topic中读取信息
bin/kafka-console-consumer.sh --zookeeper weekend114:2181 --from-beginning --topic order

8、查看一个topic的分区及副本状态信息
bin/kafka-topics.sh --describe --zookeeper weekend114:2181 --topic order


查看全部话题
./bin/kafka-topics.sh --list --zookeeper weekend114:2181
（3）启动flume
 

bin/flume-ng agent --conf conf --conf-file conf/demoagent.conf --name a1 -Dflume.root.logger=INFO,console
我们现在向/home/zzq/flumedemo/test.log文件追加内容

[zzq@weekend110 ~]$ echo '您好啊' >> /home/zzq/flumedemo/test.log
此时我们查看kafka话题的内容



可以看到kafka已经接收到了，我们现在再用storm读kafka做流式处理





storm代码下载地址：http://download.csdn.net/detail/baidu_19473529/9746787



这样整合就完成了

​