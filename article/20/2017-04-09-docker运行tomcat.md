---
layout:					post
title:					"docker运行tomcat"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
一、下载一个Linux版本的jdk和tomcat解压到同一个目录下

       我解压到了/home/zzq/app目录

二、登录到Ubuntu（或者其他系统）容器中去配置

docker run -i -t -v /home/zzq/app/:/mnt/software/ 0ef2e08ed3fa /bin/bash
docker run <相关参数> <镜像 ID> <初始命令>

相关参数包括：
-i：表示以“交互模式”运行容器
-t：表示容器启动后会进入其命令行
-v：表示需要将本地哪个目录挂载到容器中，格式：-v <宿主机目录>:<容器目录>

我现在把宿主机的/home/zzq/app目录挂载在Ubuntu上的/mnt/software目录下

JAVA_HOME=/opt/software/jdk1.7.0_80
JRE_HOME=$JAVA_HOME/jre
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
将software拷贝到任意一个目录，我拷贝到了/opt下

root@0413329f71d3:/mnt# cp software/ /opt/
cp: omitting directory 'software/'
root@0413329f71d3:/mnt# cp -R software/ /opt/
接下来配置jdk的环境变量：

root@0413329f71d3:/opt/software# vi /etc/profile
加入


JAVA_HOME=/opt/software/jdk1.7.0_80
JRE_HOME=$JAVA_HOME/jre
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin

然后source /etc/profile测试下jdk是否安装成功

注意：可以没有vim，这是最小化的系统需要自己安装vim，请看这里docker保存对容器的修改_docker中修改文件为啥不会保存-CSDN博客

这个时候再写一个shell脚本


vi /opt/software/run.sh #!/bin/bash source /etc/profile sh /opt/software/apache-tomcat-7.0.76/bin/catalina.sh run

并给执行权限 chmod u+x /opt/software/run.sh

三、保存更改commit

这个时候就该保存对容器的更改了，commit请看这里docker保存对容器的修改_docker中修改文件为啥不会保存-CSDN博客

四、启动刚刚保存的容器

[zzq@weekend110 ~]$ docker run -d -p 58080:8080 --name javaweb3 0ef2e08ed3fa  /opt/software/run.sh
45131f0bedc97a67b3917858d747b94035c398f572602e5765d89ded8a2bbb61
稍作解释：


-d：表示以“守护模式”执行/root/run.sh脚本，此时 Tomcat 控制台不会出现在输出终端上。
-p：表示宿主机与容器的端口映射，此时将容器内部的 8080 端口映射为宿主机的 58080 端口，这样就向外界暴露了 58080 端口，可通过 Docker 网桥来访问容器内部的 8080 端口了。
--name：表示容器名称，用一个有意义的名称命名即可。
关于 Docker 网桥的内容，需要补充说明一下。实际上 Docker 在宿主机与容器之间，搭建了一座网络通信的桥梁，我们可通过宿主机 IP 地址与端口号来映射容器内部的 IP 地址与端口号，


在一系列参数后面的是“镜像名”或“镜像 ID”，怎么方便就怎么来。最后是“初始命令”，它是上面编写的运行脚本，里面封装了加载环境变量并启动 Tomcat 服务的命令。


当运行以上命令后，会立即输出一长串“容器 ID”，我们可通过docker ps命令来查看当前正在运行的容器。

[zzq@weekend110 ~]$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                     NAMES
45131f0bedc9        0ef2e08ed3fa        "/opt/software/run.sh"   24 minutes ago      Up 24 minutes       0.0.0.0:58080->8080/tcp   javaweb3
五、浏览器测试访问

http://<宿主机的ip>:58080/



我们就可以看到这熟悉的界面了

​