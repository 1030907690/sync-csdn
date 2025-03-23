---
layout:					post
title:					"设置的crontab脚本无法启动、关闭tomcat解决"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
写了一个脚本每天重启tomcat

restartTomcat.sh 

#!/bin/bash 
procId=`ps -ef | grep tomcat |grep -v 'grep' | awk '{print $2}' | head -1`;
/usr/local/apache-tomcat-7.0.62/bin/shutdown.sh;
dateTime=`date`;
echo  $dateTime ' 正在关闭tomcat进程id : '$procId >>  ./restartTomcat.log;
kill -9 $procId;
/usr/local/apache-tomcat-7.0.62/bin/startup.sh

发现了一个问题就是单独执行这个脚本能关闭、启动tomcat放到crontab里面定时执行就不行了。

解决办法：

在catalina.sh里面加入jdk和jre的路径，配环境：

    

export JAVA_HOME=/usr/java/jdk1.7.0_67 
export JRE_HOME=$JAVA_HOME/jre
这样放到crontab是执行成功了的

​