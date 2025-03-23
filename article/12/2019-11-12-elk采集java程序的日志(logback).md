---
layout:					post
title:					"elk采集java程序的日志(logback)"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
### 衔接上篇[elk搭建和采集nginx日志](https://blog.csdn.net/baidu_19473529/article/details/103025043)
### 构建项目
- 我的是一个spring boot项目，日志用的logback
- pom.xml加入

```bash
	<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-logging</artifactId>
		</dependency>
		<dependency>
			<groupId>net.logstash.logback</groupId>
			<artifactId>logstash-logback-encoder</artifactId>
			<version>4.11</version>
		</dependency>
		<dependency>
			<groupId>net.logstash.log4j</groupId>
			<artifactId>jsonevent-layout</artifactId>
			<version>1.7</version>
		</dependency>
```
- resources增加logback.xml

```bash
<?xml version="1.0" encoding="UTF-8"?>
<configuration scan="true" scanPeriod="60 seconds" debug="false">
    <include resource="org/springframework/boot/logging/logback/base.xml" />
    <contextName>logback</contextName>
    <!-- 记录文件到特定目录 -->
    <!-- <property name="log.path" value="E:\\test\\logback.log" /> -->
    <property name="log.path" value="/Users/chang/Desktop/CHLogs/logback.log" />
    <appender name="stash" class="net.logstash.logback.appender.LogstashTcpSocketAppender">
        <destination>192.168.137.137:9601</destination>
        <encoder class="net.logstash.logback.encoder.LogstashEncoder" />
    </appender>
    <!--输出到控制台-->
    <appender name="console" class="ch.qos.logback.core.ConsoleAppender">
        <!-- <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
         <level>ERROR</level>
        </filter>-->
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} %contextName [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    <!--输出到文件-->
    <appender name="file" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${log.path}</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>logback.%d{yyyy-MM-dd}.log</fileNamePattern>
        </rollingPolicy>
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} %contextName [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    <root level="info">
        <appender-ref ref="stash"/>
        <appender-ref ref="console" />
        <appender-ref ref="file" />
    </root>
    <!-- logback为 java 中的包
    <logger name="com.dudu.controller"/>
    logback.LogbackDemo：类的全路径
    <logger name="com.dudu.controller.LearnController" level="WARN" additivity="false">
     <appender-ref ref="console"/>
    </logger> -->
</configuration>
```
- 写一个供外部调用的接口
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/205bd3eee635219189f0b82fbdcabcee.png)
### 配置logstash
- 新建 logstash-tomcat-access-log.conf

```bash
input {
    tcp{      
                port => 9601  # 这个端口是刚才logback.xml文件那个
                mode => "server"
                codec => json_lines
        }
}



output {
  elasticsearch {
        hosts => ["192.168.137.137:9200"]
        index => "logstash-tomcat-log"
    }
stdout{
         codec => rubydebug
	}
}

```
- 启动logstash `nohup bin/logstash -f logstash-tomcat-access-log.conf  &`

### 采集日志
- 应用程序启动
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/62134cc665855b78cec4326ea4c7a20d.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b12382979b5ad93042f31beb9c402f54.png)
- 访问应用程序接口
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/acbb8f46d38c919e33ef09b04775c7cb.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2275d0d65c70d7e973794dc2943e8475.png)
- 现在来看kibana的展示；依然要先建索引； Management-> Index Patterns -> Create index pattern；然后到Discover界面。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c1abf1c7a08aae8b0132a8786f7ceedc.png)
- 基本上完工了。附上配套程序例子[https://github.com/1030907690/elk-demo](https://github.com/1030907690/elk-demo)；如果文章有错误的地方，希望批评指正。


