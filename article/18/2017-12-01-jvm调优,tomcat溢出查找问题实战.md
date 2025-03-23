---
layout:					post
title:					"jvm调优,tomcat溢出查找问题实战"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
###前言
- **之前公司的一个项目部署在tomcat运行一段时间后老是jvm堆内存溢出,项目是用的jfanl框架做的,翻看整个项目的源码,并没有发现会大量占用内存的地方，开始用了个治标不治本的办法；通过curl命令监听web服务的状态[shell脚本使用curl获取访问网站的状态码](http://blog.csdn.net/baidu_19473529/article/details/73292535)**,后面通过一些对jvm的学习,终于找到症结所在。
###一、准备好工具
- **JVisualVM， 是一款免费的性能分析工具。它通过 jvmstat、JMX、SA（Serviceability Agent）以及 Attach API 等多种方式从程序运行时获得实时数据，从而进行动态的性能分析，这是jdk自带的,在jdk bin目录下可以找到jvisualvm.exe**
- **MAT(Memory Analyzer Tool)，一个基于Eclipse的内存分析工具，是一个快速、功能丰富的JAVA heap分析工具，它可以帮助我们查找内存泄漏和减少内存消耗。使用内存分析工具从众多的对象中进行分析，快速的计算出在内存中对象的占用大小，看看是谁阻止了垃圾收集器的回收工作，并可以通过报表直观的查看到可能造成这种结果的对象。下载地 址[http://www.eclipse.org/mat/downloads.php](http://www.eclipse.org/mat/downloads.php)**

###二、配置tomcat,OOM时转储详细的堆栈日志文件
- **linux配置文件bin/catalina.sh **
	
- **先创建/tomcatHeap目录,只需要配置这两个参数就可以了-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath**

```
-XX:+HeapDumpOnOutOfMemoryError #这是OOM后转储文件

 -XX:HeapDumpPath  #配置文件存储的路径,如果没有这个参数默认保存在tomcat根目录下
```
- 完整的配置，在cygwin=false前面加上这段
```
JAVA_OPTS=-server -Xms512m -Xmx1024m -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tomcatHeap
```
- -Xms512m -Xmx1024m这两个参数或者其他的参数可以根据自己的需求去设置，这里只是一个参考,配置好后重启tomcat。
###三、观察,分析

- 我使用jstat -gcutil 11454 1s  
	 jstat是用于监视虚拟机各种运行状态信息的命令行工具，-gcutil是输出Eden区、两个survivor区、老年代、永久代等的容量、已用空间所占总空间的总空间的百分比；还有GC时间合计等信息，这里的2567是我的tomcat进程id,然后是每一秒打印一次
![这里写图片描述](https://img-blog.csdn.net/20171201223410986?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

- **这个图已经比较明显了，eden和old区域占比100% ，YGC,FGC次数很高,但是还是回收不了了,最后OOM,现在我们已经得到了oom日志文件了,下载下来用工具来分析更直观,看是哪一个大对象占用。**

- **打开jvisualvm.exe，点击文件->装入 ,选择文件一般生成的是后缀.hprof的文件**

![这里写图片描述](https://img-blog.csdn.net/20171201225621535?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

- **然后开类的视图**
![这里写图片描述](https://img-blog.csdn.net/20171201225806197?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

- **可以看到这个HashMap的占用很高,存储了很多key,value的数据,我们再用mat工具看看**


- **打开mat工具,点击File->Open Heap Dump  点击进入 Leak Suspects**

![这里写图片描述](https://img-blog.csdn.net/20171201230948061?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
- **看到net.sf.ehcache.store.MemoryStore这一段我相信大部分做过JAVAEE的朋友应该都会有印象吧。看到这里我在去找了关于ehcache相关的代码，终于找到了原来是配置的问题,缓存超时时间配置了一天,一直占用着jvm堆内存**

![这里写图片描述](https://img-blog.csdn.net/20171201231848066?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

```
timeToLiveSeconds=x：缓存自创建日期起至失效时的间隔时间x；
timeToIdleSeconds=y：缓存创建以后，最后一次访问缓存的日期至失效之时的时间间隔y；
举例说明：timeToLiveSeconds =3600 timeToIdleSeconds =300
以上配置代表缓存有效时间为3600秒（自缓存建立起一个小时有效 ），在有效的一个小时内，如果连续五分钟未访问缓存，则缓存失效。
```

- 这是我解决这个问题的大致思路,希望能帮助大家解决问题。