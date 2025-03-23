---
layout:					post
title:					"shell脚本使用curl获取访问网站的状态码"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​

 
curl -I -m 10 -o /dev/null -s -w %{http_code} www.baidu.com

-I 仅测试HTTP头
-m 10 最多查询10s
-o /dev/null 屏蔽原有输出信息
-s silent
-w %{http_code} 控制额外输出
 
绑定 ip 测试：


curl -I -m 10  -H "www.baidu.com"  http://220.xxx.112.143 -o /dev/null -s -w %{http_code}

特别需要注意的是访问的url地址不能写localhost或者是127.0.0.1 ，这样写curl一直返回的状态码都是000,我测试了下本机的话写路由器分配的那个ip地址是可以正常返回状态值的。

现在附上我写的监听tomcat重启脚本，监听可以用crontab来实现

#!/bin/bash 
justWeb=`curl -I -m 10 -o /dev/null -s -w %{http_code} http://192.168.18.2/gw`;
echo 'justWeb ' $justWeb;
if [ "$justWeb"x != "200"x ] ; then
 
 procId=`ps -ef | grep tomcat |grep -v 'grep' | awk '{print $2}' | head -1`;
 /usr/local/apache-tomcat-7.0.62/bin/shutdown.sh;
 #/home/zzq/app/apache-tomcat-7.0.76/bin/shutdown.sh;
 dateTime=`date`;
 echo  $dateTime '检测到web服务状态码为: ' $justWeb  ' 正在关闭tomcat进程id : '$procId >>  ./restartTomcat.log;
 kill -9 $procId;
 /usr/local/apache-tomcat-7.0.62/bin/startup.sh;
 #/home/zzq/app/apache-tomcat-7.0.76/bin/startup.sh;
fi


​