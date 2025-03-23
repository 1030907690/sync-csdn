---
layout:					post
title:					"idea中无法启动tomcat,一直是卡住的状态"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
今天在idea中运行tomcat是一直卡住在

```
27-Oct-2017 17:25:49.794 信息 [main] org.apache.catalina.startup.Catalina.load Initialization processed in 5946 ms
27-Oct-2017 17:25:49.817 信息 [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
27-Oct-2017 17:25:49.817 信息 [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet Engine: Apache Tomcat/8.5.20
27-Oct-2017 17:25:49.824 信息 [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
27-Oct-2017 17:25:49.829 信息 [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["ajp-nio-8009"]
27-Oct-2017 17:25:49.831 信息 [main] org.apache.catalina.startup.Catalina.start Server startup in 36 ms
27-Oct-2017 17:25:59.826 信息 [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deploying web application directory [D:\software\apache-tomcat-8.5.20\webapps\manager]
27-Oct-2017 17:26:00.048 信息 [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory [D:\software\apache-tomcat-8.5.20\webapps\manager] has finished in [222] ms

```
![这里写图片描述](https://img-blog.csdn.net/20171027194424731?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

- **我看见卡住的是tomcat webpps自带的项目，于是就想着删除掉试试看**
 - 但是删除后依旧没有解决掉开启tomcat卡住的问题只是卡住的地方不一样了
 
![这里写图片描述](https://img-blog.csdn.net/20171027194637971?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
```
27-Oct-2017 17:52:03.585 信息 [main] org.apache.catalina.startup.Catalina.start Server startup in 31 ms
```

- **最后终于找到是catalina.bat问题，因为我在catalina.bat文件加入了jvm的启动参数**

![这里写图片描述](https://img-blog.csdn.net/20171027195425311?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

  - **注释掉或者删除这段代码再次运行tomcat就正常了， rem 是注释**
 

```
rem set JAVA_OPTS=-server -Xms1024m -Xmx1024m  
```


  
![这里写图片描述](https://img-blog.csdn.net/20171027195658451?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)