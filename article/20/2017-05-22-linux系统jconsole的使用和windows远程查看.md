---
layout:					post
title:					"linux系统jconsole的使用和windows远程查看"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
一、jconsole能干什么

查看jvm内存使用情况就可以使用jconsole，从Java 5开始 引入了 JConsole。JConsole 是一个内置 Java 性能分析器，可以从命令行或在 GUI shell 中运行。您可以轻松地使用 JConsole（或者，它更高端的 “近亲” VisualVM ）来监控 Java 应用程序性能和跟踪 Java 中的代码。

二、开始部署和运行

1、先安装好jdk和一个tomcat

2、修改tomcat中bin/catalina.sh文件

vi bin/catalina.sh


if [ "$1" = "start" ] ; then  #判断是否为启动
JAVA_OPTS="-Dcom.sun.management.jmxremote.port=10000 -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false -Djava.rmi.server.hostname=192.168.217.128"
fi

在cygwin=false前面加入这段话

   authenticate为false，jconsole连接远程jvm时，就不需要输入用户名和密码。
   否则，要配置密码文件和密码。
   可以指定密码文件的位置
   JAVA_OPTS="$JAVA_OPTS -Dcom.sun.management.jmxremote.pwd.file=/root/soft/jdk7/jre/lib/management/jmxremote.password"

 -Dcom.sun.management.jmxremote.port=10000 是设置jconsole监听端口号

 -Djava.rmi.server.hostname=192.168.217.128 设置的是我linux本机地址

加入if判断是否为start的原因是 由于配置了上述文件，在停止tomcat的时，会由于上述配置的端口被占用而无法停掉，会抛出端口占用的异常

3、把10000端口添加进白名单（最好关闭防火墙，不知道为什么我这边只有关闭了防火墙才能连接成功）

   

       4、在windows上打开jconsole程序连接，输入地址和端口(jconsole在jdk bin目录下)



然后连接

        

这样也就成功了



​