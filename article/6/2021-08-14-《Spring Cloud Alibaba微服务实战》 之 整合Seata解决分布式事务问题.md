---
layout:					post
title:					"《Spring Cloud Alibaba微服务实战》 之 整合Seata解决分布式事务问题"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录) 
- 前面已经把Seata的服务端程序启动好了，下面开始把Seata整合到上面的案例中，使用AT事务模式解决实际的分布式事务问题。需要有以下几个步骤。
### 1．往项目中添加关于Seata的依赖包。
- 在订单服务和配送服务的pom.xml文件dependencies标签中分别加入如下依赖。
```
<!--seata 依赖-->
<dependency>
	<groupId>com.alibaba.cloud</groupId>
	<artifactId>spring-cloud-starter-alibaba-seata</artifactId>
	<exclusions>
		<exclusion>
			<groupId>io.seata</groupId>
			<artifactId>seata-spring-boot-starter</artifactId>
		</exclusion>
	</exclusions>
</dependency>
<!--引入1.2.0 默认是1.1.0的-->
<dependency>
	<groupId>io.seata</groupId>
	<artifactId>seata-spring-boot-starter</artifactId>
	<version>1.2.0</version>
</dependency>
```
- 因为spring-cloud-starter-alibaba-seata默认的seata-spring-boot-starte依赖是1.1.0的，为了稳妥起见，先排除默认的依赖，然后单独引入seata-spring-boot-starte 1.2.0版本的依赖。

### 2．创建Seata高可用所需的database和表以及业务数据库所需要的undo_log表。
- 创建seata库并新增branch_table、global_table、lock_table表。表结构参考文档https://github.com/seata/seata/blob/1.2.0/script/server/db/mysql.sql后，连接Mysql数据库后，输入如下代码。

```
create database `seata`; -- 创建seata database
use seata; --选择seata database 
CREATE TABLE IF NOT EXISTS `global_table` -- 存储全局会话数据
(
    `xid`                       VARCHAR(128) NOT NULL,
    `transaction_id`            BIGINT,
    `status`                    TINYINT      NOT NULL,
    `application_id`            VARCHAR(32),
    `transaction_service_group` VARCHAR(32),
    `transaction_name`          VARCHAR(128),
    `timeout`                   INT,
    `begin_time`                BIGINT,
    `application_data`          VARCHAR(2000),
    `gmt_create`                DATETIME,
    `gmt_modified`              DATETIME,
    PRIMARY KEY (`xid`),
    KEY `idx_gmt_modified_status` (`gmt_modified`, `status`),
    KEY `idx_transaction_id` (`transaction_id`)
) ENGINE = InnoDB
DEFAULT CHARSET = utf8;
CREATE TABLE IF NOT EXISTS `branch_table`  -- 存储分支会话数据的表
(
    `branch_id`         BIGINT       NOT NULL,
    `xid`               VARCHAR(128) NOT NULL,
    `transaction_id`    BIGINT,
    `resource_group_id` VARCHAR(32),
    `resource_id`       VARCHAR(256),
    `branch_type`       VARCHAR(8),
    `status`            TINYINT,
    `client_id`         VARCHAR(64),
    `application_data`  VARCHAR(2000),
    `gmt_create`        DATETIME(6),
    `gmt_modified`      DATETIME(6),
    PRIMARY KEY (`branch_id`),
    KEY `idx_xid` (`xid`)
) ENGINE = InnoDB
DEFAULT CHARSET = utf8;
CREATE TABLE IF NOT EXISTS `lock_table` -- 存储锁的数据表
(
    `row_key`        VARCHAR(128) NOT NULL,
    `xid`            VARCHAR(96),
    `transaction_id` BIGINT,
    `branch_id`      BIGINT       NOT NULL,
    `resource_id`    VARCHAR(256),
    `table_name`     VARCHAR(32),
    `pk`             VARCHAR(36),
    `gmt_create`     DATETIME,
    `gmt_modified`   DATETIME,
    PRIMARY KEY (`row_key`),
    KEY `idx_branch_id` (`branch_id`)
) ENGINE = InnoDB
DEFAULT CHARSET = utf8;
```
- 在每个业务数据库创建undo_log表，对应到本案例的场景就是分别在distribution和order数据库创建undo_log表。表结构参考文档https://github.com/seata/seata/blob/1.2.0/script/client/at/db/mysql.sql，连接MySql数据库后，输入如下代码。

```
use distribution; -- 选择distribution库
CREATE TABLE IF NOT EXISTS `undo_log` -- AT事务模式distribution库的撤销表
(
    `id`            BIGINT(20)   NOT NULL AUTO_INCREMENT COMMENT 'increment id',
    `branch_id`     BIGINT(20)   NOT NULL COMMENT 'branch transaction id',
    `xid`           VARCHAR(100) NOT NULL COMMENT 'global transaction id',
    `context`       VARCHAR(128) NOT NULL COMMENT 'undo_log context,such as serialization',
    `rollback_info` LONGBLOB     NOT NULL COMMENT 'rollback info',
    `log_status`    INT(11)      NOT NULL COMMENT '0:normal status,1:defense status',
    `log_created`   DATETIME     NOT NULL COMMENT 'create datetime',
    `log_modified`  DATETIME     NOT NULL COMMENT 'modify datetime',
    PRIMARY KEY (`id`),
    UNIQUE KEY `ux_undo_log` (`xid`, `branch_id`)
) ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARSET = utf8 COMMENT ='AT transaction mode undo table';
use `order`; -- 选择order库
CREATE TABLE IF NOT EXISTS `undo_log` -- AT事务模式order库的撤销表
(
    `id`            BIGINT(20)   NOT NULL AUTO_INCREMENT COMMENT 'increment id',
    `branch_id`     BIGINT(20)   NOT NULL COMMENT 'branch transaction id',
    `xid`           VARCHAR(100) NOT NULL COMMENT 'global transaction id',
    `context`       VARCHAR(128) NOT NULL COMMENT 'undo_log context,such as serialization',
    `rollback_info` LONGBLOB     NOT NULL COMMENT 'rollback info',
    `log_status`    INT(11)      NOT NULL COMMENT '0:normal status,1:defense status',
    `log_created`   DATETIME     NOT NULL COMMENT 'create datetime',
    `log_modified`  DATETIME     NOT NULL COMMENT 'modify datetime',
    PRIMARY KEY (`id`),
    UNIQUE KEY `ux_undo_log` (`xid`, `branch_id`)
) ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARSET = utf8 COMMENT ='AT transaction mode undo table';
```
### 3．整理高可用db模式参数配置并提交至Nacos配置中心。
- 配置内容参考https://github.com/seata/seata/blob/1.2.0/script/config-center/config.txt，这里的配置一大堆。不过一般情况下很多用不到，内容可以精简一下，创建config.txt文件，配置内容如下所示。

```
service.vgroupMapping.my_test_tx_group=default
store.mode=db
store.db.datasource=druid
store.db.dbType=mysql
store.db.driverClassName=com.mysql.jdbc.Driver
store.db.url=jdbc:mysql://127.0.0.1:3306/seata?useUnicode=true
store.db.user=root
store.db.password=root
store.db.minConn=5
store.db.maxConn=30
store.db.globalTable=global_table
store.db.branchTable=branch_table
store.db.queryLimit=100
store.db.lockTable=lock_table
store.db.maxWait=5000
```
 - 主要修改store.mode（存储模式）、store.db.url（数据库url）、store.db.user（数据库用户名）、store.db.password（数据库密码）配置项。
- 配置已经整理出来了，下一步就要把配置导入到Nacos配置中心。为此Seata提供了专门的脚本，脚本地址https://github.com/seata/seata/tree/1.2.0/script/config-center/nacos。里面有nacos-config.py和nacos-config.sh。遗憾的是Windows（Windows7之类的）不能直接运行这2个任何一个文件。如果要运行nacos-config.py文件，需要Python2.X的环境；如果要运行nacos-config.sh可以先安装Git，借助Git Bash窗口运行sh脚本。
>注意：使用nacos-config.sh脚本导入配置时，config.txt文件要放到它的上级目录。

- 为此，笔者特意准备好了Windows可直接运行的版本，下载地址为https://github.com/1030907690/public-script/raw/master/generic/nacos-config.exe。
- 将nacos-config.exe和config.txt，放到同级目录，使用如下命令把配置导入到Nacos。

```
nacos-config.exe 127.0.0.1:8848
```

> 注意：第一个参数是Nacos的服务地址，第二个参数是namespace（选填）。

- 命令运行完成后，在Nacos控制台配置列表就能看到刚才导入的配置了，如图10.8所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ed6ba7fdfb888a38c58657cbc4d98f7b.png#pic_center)
<center>图10.8  Seata的db配置</center>

### 4．订单服务和配送服务分别加入Seata的配置。
- 参考官方配置https://github.com/seata/seata/blob/1.2.0/script/client/spring/application.yml，一般情况下，并需要那么多，可以精简一下。

- 订单服务bootstrap.yml配置文件，主要增加的配置项有seata.enabled（是否开启Spring-Boot自动装配）、seata.application-id（应用id）、seata.tx-service-group（事务分组）、seata.enable-auto-data-source-proxy（数据源自动代理）、seata.config.type（使用哪种配置file、nacos之类）、seata.config.nacos.namespace（命名空间）、seata.config.nacos.serverAddr（服务地址）、seata.config.nacos.group（分组）、seata.registry.type（使用哪种注册中心file、nacos之类）、seata.registry.nacos.application（应用名称）、seata.registry.nacos.server-addr（服务地址）、seata.registry.nacos.namespace（命名空间）。完整代码如下所示。

```
seata:
  enabled: true # 开启
  application-id: order-server # application id
  tx-service-group: my_test_tx_group # 事务分组
  enable-auto-data-source-proxy: true # 开启数据源自动代理
  config:
    type: nacos #选择 nacos
    nacos:
      namespace:                 # namespace
      serverAddr: 127.0.0.1:8848 #nacos服务地址
      group:  SEATA_GROUP # group 分组
  registry:
    type: nacos   # 选择nacos
    nacos:
      application: seata-server  # 应用名称
      server-addr: 127.0.0.1:8848  # nacos 服务地址
      namespace:   # namespace命名空间
server:
  port: 8081 #程序端口号
spring:
  application:
    name: transaction-order-sample #应用名称
  cloud:
    sentinel:
      transport:
        port: 8719 #启动HTTP Server，并且该服务将与Sentinel仪表板进行交互，使Sentinel仪表板可以控制应用 如果被占用则从8719依次+1扫描
        dashboard: 127.0.0.1:8080  # 指定仪表盘地址
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848 #nacos服务注册、发现地址
      config:
        server-addr: 127.0.0.1:8848 #nacos配置中心地址
        file-extension: yml #指定配置内容的数据格式
management:
  endpoints:
    web:
      exposure:
        include: '*' #公开所有端点
feign:
  compression:
    request:
      enabled: true # 请求压缩启用
      mime-types: text/xml,application/xml,application/json # 要压缩的类型
      min-request-size: 2048 # 最小请求长度 单位：字节
    response:
      enabled: true  # 响应压缩启用
  sentinel:
    enabled: true  #增加对sentinel的支持 否则自定义的异常、限流等兜底方法不生效
  client:
    config:
      default:
        connectTimeout: 5000 # 建立连接所用的时间 单位：毫秒
        readTimeout: 5000  #建立连接后从服务器读取到资源所用的时间 单位：毫秒
logging:
  level:
    com.springcloudalibaba.openfeignservice.openfeignservice: debug  # 打印com.springcloudalibaba.transaction.openfeignservice包的日志 debug级别
```
- 配送服务同样要增加seata的配置，主要增加的配置项有seata.enabled（是否开启Spring-Boot自动装配）、seata.application-id（应用id）、seata.tx-service-group（事务分组）、seata.enable-auto-data-source-proxy（数据源自动代理）、seata.config.type（使用哪种配置file、nacos之类）、seata.config.nacos.namespace（命名空间）、seata.config.nacos.serverAddr（服务地址）、seata.config.nacos.group（分组）、seata.registry.type（使用哪种注册中心file、nacos之类）、seata.registry.nacos.application（应用名称）、seata.registry.nacos.server-addr（服务地址）、seata.registry.nacos.namespace（命名空间），完整代码如下所示。

```
seata:
  enabled: true # 开启
  application-id: distribution-server # application id
  tx-service-group: my_test_tx_group # 事务分组
  enable-auto-data-source-proxy: true # 开启数据源自动代理
  config:
    type: nacos #选择 nacos
    nacos:
      namespace:                 # namespace
      serverAddr: 127.0.0.1:8848 #nacos服务地址
      group:  SEATA_GROUP # group 分组
  registry:
    type: nacos   # 选择nacos
    nacos:
      application: seata-server  # 应用名称
      server-addr: 127.0.0.1:8848  # nacos 服务地址
      namespace:   # namespace命名空间
server:
  port: 8082 #程序端口号
spring:
  application:
    name: transaction-distribution-sample #应用名称
  cloud:
    sentinel:
      transport:
        port: 8719 #启动HTTP Server，并且该服务将与Sentinel仪表板进行交互，使Sentinel仪表板可以控制应用  如果被占用则从8719依次+1扫描
        dashboard: 127.0.0.1:8080  # 指定仪表盘地址
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848 #nacos服务注册、发现地址
      config:
        server-addr: 127.0.0.1:8848 #nacos配置中心地址
        file-extension: yml #指定配置内容的数据格式
management:
  endpoints:
    web:
      exposure:
        include: '*' #公开所有端点
5．在事务开始的地方加上@GlobalTransactional注解，结合本案例也就是在OrderServiceImpl#createOrder方法上加@GlobalTransactional注解，修改后的方法完整代码如下所示。
@Transactional // Spring事务注解
@GlobalTransactional // seata全局事务注解 -- 新增代码
@Override
public Integer createOrder(Integer id) {
	if (shopMap.containsKey(id)) {
		String orderId = UUID.randomUUID().toString().replace("-", "");
		int update = jdbcTemplate.update("insert into t_order(order_id,shop_id) values(?,?)",
				new Object[]{orderId, id});//新增分配配送员的数据
		Integer result = distributionService.distribution(orderId); // 调用配送服务
		if (result <= 0) {
			throw new RuntimeException("分配配送员失败!"); // 如果小于等于0表示失败抛出RuntimeException异常
		}
		return update;
	}
	return 0;
}
```
- Seata已经整合好了，下面就来测试分布式事务已经解决。
- 使用curl命令调用/createOrder接口，调用结果如下所示。
- 毫无疑问，调用结果抛出RuntimeException异常，再来看看数据库的结果。如图10.9和10.10所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/76b6aa430aba4ff8dd366de7e7884e2d.png#pic_center)
<center>图10.9  t_order表数据</center>

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fb8b4b4e6c318192c09be0ff379ee5c3.png#pic_center)
<center>图10.10  order_distribution表数据</center>

> 注意：超时会导致Seata服务端日志报Could not found global transaction xid，在本案例属正常现象。

- 结果表明，接口出现异常后，t_order表和order_distribution表的数据并没有新增，数据回滚是成功的。达到了数据一致性的效果。

- 本文是《Spring Cloud Alibaba微服务实战》书摘之一，如有兴趣可购买书籍。[天猫](https://detail.tmall.com/item.htm?spm=a230r.1.14.40.4d013ed4NkvyPZ&id=650584628890&ns=1&abbucket=3)、[京东](https://item.jd.com/13365970.html)、[当当](http://product.dangdang.com/29275400.html)。书中内容有任何问题，可在本博客下留言，或者到[https://github.com/1030907690](https://github.com/1030907690)提issues。
