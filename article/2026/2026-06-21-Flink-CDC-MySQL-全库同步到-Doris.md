@[TOC](目录)
# 前言
- 之前在[Flink CDC MySQL同步到Elasticsearch](https://blog.csdn.net/baidu_19473529/article/details/155417414)提到过Flink CDC同步有三种方式：
	- 方式一、编写代码引入驱动包（Flink DataStream/Table API）,灵活定制，适用于复杂业务。
	- 方式二、使用Flink SQL，极简搭建，适用于简单业务。
	- 方式三、使用flink-cdc，目前仅适用于单表（不能组宽表）。

- 使用Flink SQL同步少量单表或组宽表效果很不错，如果要同步全库的表用Flink SQL写起来挺麻烦。就需要用`Flink DataStream/Table API` 或 `flink-cdc`。如果用`Flink DataStream/Table API`就要自己写代码，对于简单业务 flink-cdc 更方便。


# 前置准备
## Java 环境
-  JDK 17(Flink和Doris都需要用JDK)， 建议使用 [sdkman](https://sdkman.io/install/) 管理
## 数据库
- MySQL 8+ , 很常用的软件，就不赘述了。
- Doris 4+ ，[安装文档](https://doris.apache.org/zh-CN/docs/4.x/getting-started/quick-start)
	- Doris要修改最大文件句柄数，修改虚拟内存区域。禁止虚拟内存，先启动FE再启动BE，启动命令如下
	```shell
	
	sudo sysctl -w vm.max_map_count=2000000
	sudo swapoff -a
	fe/bin/start_fe.sh --daemon
	be/bin/start_be.sh --daemon
	```
	- 启动完成`8030`是 Web UI 界面，帐号root 无密码，登陆进来大概是这样的。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/1cd10ccc18044996b97bf850fe6f9e15.png)



## Flink
- [Flink-1.20.3](https://archive.apache.org/dist/flink/flink-1.20.1/flink-1.20.1-bin-scala_2.12.tgz) 
	- 设置环境变量`FLINK_HOME`
	```shell
	export FLINK_HOME=/home/zzq/software/flink-1.20.3
	```
	- [mysql-connector-java-8.0.27.jar](https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.27/mysql-connector-java-8.0.27.jar)包放到`lib`目录下
    - 启动flink `bin/start-cluster.sh`

- [flink-cdc-3.5.0](https://www.apache.org/dyn/closer.lua/flink/flink-cdc-3.5.0/flink-cdc-3.5.0-bin.tar.gz)

	- [flink-cdc-pipeline-connector-mysql-3.5.0.jar](https://repo1.maven.org/maven2/org/apache/flink/flink-cdc-pipeline-connector-mysql/3.5.0/flink-cdc-pipeline-connector-mysql-3.5.0.jar) 、[flink-cdc-pipeline-connector-doris-3.5.0.jar](https://repo1.maven.org/maven2/org/apache/flink/flink-cdc-pipeline-connector-doris/3.5.0/flink-cdc-pipeline-connector-doris-3.5.0.jar) 放到`lib`目录



# 任务配置 yaml 文件

- 我要同步`test`库到Doris
```yml
source:
  type: mysql
  hostname: 192.168.81.166
  port: 3306
  username: root
  password: root
  tables: test.\.*
  server-id: 5400-5404
  server-time-zone: Asia/Shanghai
  # 要同步表的中文描述
  include-comments.enabled: true
  # tinyint 不要转布尔值
  treat-tinyint1-as-boolean.enabled: false

sink:
  type: doris
  fenodes: 127.0.0.1:8030
  username: root
  password: ""
  table.create.properties.light_schema_change: true
  table.create.properties.replication_num: 1

pipeline:
  name: Sync MySQL Database to Doris
  parallelism: 1

```
- 更多参数解释请移步官方文档 [https://nightlies.apache.org/flink/flink-cdc-docs-release-3.5/zh/docs/connectors/pipeline-connectors/mysql/](https://nightlies.apache.org/flink/flink-cdc-docs-release-3.5/zh/docs/connectors/pipeline-connectors/mysql/)

- MySQL test库有这些表
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3e05b433d079441b9170079127ded863.png)
- 注意: 表必须有`主键`，否则无法利用`upsert`机制。


# 提交任务
- 执行以下命令提交任务
```shell
bash bin/flink-cdc.sh mysql-to-doris.yaml
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9025296b439b44429c2b6210cefb4ed7.png)
- Flink Web UI也会出现Job。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/aaa3a1e4ed6b47cba3c5189bbb4b88e0.png)

# 验证
- 来到 Doris Web UI，可以看到数据已同步。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5abe4eb55aaf47fcb60fea35cac9ee97.png)


# 参考
- [https://nightlies.apache.org/flink/flink-cdc-docs-release-3.5/zh/docs/get-started/quickstart/mysql-to-doris/](https://nightlies.apache.org/flink/flink-cdc-docs-release-3.5/zh/docs/get-started/quickstart/mysql-to-doris/)
- [https://doris.apache.org/zh-CN/docs/4.x/getting-started/quick-start](https://doris.apache.org/zh-CN/docs/4.x/getting-started/quick-start)