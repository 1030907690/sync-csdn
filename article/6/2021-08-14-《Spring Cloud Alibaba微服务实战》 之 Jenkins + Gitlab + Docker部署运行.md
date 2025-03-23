---
layout:					post
title:					"《Spring Cloud Alibaba微服务实战》 之 Jenkins + Gitlab + Docker部署运行"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)

- 前面已经分别使用过Docker、Jenkins + GitLab 了，本小节就将它们整合起来使用。在Java项目中直接使用Dockerfile构建镜像还是有些不方便，最直观的有一些路径问题要解决，好在可以使用Maven插件构建镜像。
- 1．在服务消费者和2个服务提供者项目的pom.xml文件plugins标签下增加docker-maven-plugin插件，新增的代码如下所示。

```
<!--maven构建docker镜像 -->
<plugin>
		<groupId>com.spotify</groupId>
		<artifactId>docker-maven-plugin</artifactId>
		<version>0.4.13</version>
		<configuration>
				<imageName>${artifactId}:${version}</imageName> <!-- 镜像名称 -->
				<baseImage>java:8</baseImage> <!-- 依赖的基础镜像 -->
				<entryPoint>["java","-jar","${project.build.finalName}.jar"]</entryPoint> <!--执行ENTRYPOINT指令-->
				<resources>
						<resource>
								<targetPath>/</targetPath>
								<directory>${project.build.directory}</directory> <!-- 表示target目录 -->
								<include>${project.build.finalName}.jar</include><!-- 指定要复制的文件-->
						</resource>
				</resources>
		</configuration>
</plugin>
```
- 执行的大概流程几乎与直接使用Dockerfile时别无二致。

- 2．定位到Maven安装目录下，修改conf/settings.xml文件，在pluginGroups标签下新增docker插件的配置，新增代码如下所示。

```
<pluginGroup>com.spotify</pluginGroup>
```

>注意：如果没有此配置打包时会报No plugin found for prefix 'docker' in the current project and in the plugin groups。

- 3．来到Jenkins项目主界面，点击配置（Configure），修改之前的配置，定位到构建（Build）一栏。

（1）首先要先执行一段脚本，因为镜像和容器的名称都不能重复，所以这段脚本停止正在运行的容器、删除以前的容器、删除以前的镜像，具体代码如下所示。

```
#!/bin/bash
array=("nacos-consumer-sample" "nacos-provider-sample8081" "nacos-provider-sample8082") #数据
for item in  ${array[@]};  # for循环
do
	instance=`docker ps -a | grep $item | head -1`; # 查找这个容器
	image=`docker images | grep $item | awk '{print $1}' | head -1`; # 查找这个镜像
	if [ "$instance"x != ""x ] ; then # 判断是否运行过这个容器
		docker stop $item    # 停止容器
		docker rm $item    # 删除容器
	fi
	if [ "$image"x != ""x ] ; then # 判断是否有这个镜像
		docker rmi $item:0.0.1-SNAPSHOT    # 删除镜像
	fi
done
```
（2）下一步就是执行打包了，打包不再是clean package了，而是填入如下命令。

```
clean package docker:build 
```

>注意：如果是命令行直接执行那就是mvn clean package docker:build。

（3）最后一个步骤执行创建并运行容器。填入的命令如下所示。

```
#!/bin/bash
docker run --name nacos-consumer-sample -d -p 8086:8086   nacos-consumer-sample:0.0.1-SNAPSHOT 
docker run --name nacos-provider-sample8081 -d -p 8081:8081   nacos-provider-sample8081:0.0.1-SNAPSHOT
docker run --name nacos-provider-sample8082 -d -p 8087:8087   nacos-provider-sample8082:0.0.1-SNAPSHOT
```


- 这三个步骤完整配置如图14.27所示。 
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e0e411eb2853befe51142259626efecb.png#pic_center)
<center>图14.27  构建（Build）步骤
</center>

- 保存后，回到Jenkins项目主界面，点击Build Now按钮，确认构建时控制台日志未报错后，尝试请求/test，再使用docker ps查看正在运行的容器，结果如图14.28所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/73cece4db12761445b7164e943993088.png#pic_center)
<center>图14.28  请求/test接口结果和查看正在运行的容器
</center>


- 这样算是运行成功了，并且之前配置了Webhook，每次有稳定代码提交上来时，就能自动构建了，像一个“流水线”一样有序生产了。
- 如果遇到一些复杂的场景，可以选择Docker插件与Dockerfile联合使用。
- 首先修改项目pom.xml配置，修改后的缩略配置如下所示。


```
<!--maven构建docker镜像 -->
<plugin>
		<groupId>com.spotify</groupId>
		<artifactId>docker-maven-plugin</artifactId>
		<version>0.4.13</version>
		<configuration>
				<imageName>${artifactId}:${version}</imageName> <!-- 镜像名称 -->
				<dockerDirectory>${project.basedir}/src/main/docker</dockerDirectory> <!-- Dockerfile文件位置 -->
				<resources>
						<resource>
								<targetPath>/</targetPath>
								<directory>${project.build.directory}</directory> <!-- 表示target目录 -->
								<include>${project.build.finalName}.jar</include><!-- 指定要复制的文件-->
						</resource>
				</resources>
		</configuration>
</plugin>
```


- 然后在项目目录下创建docker文件夹，新增Dockerfile文件，例如服务提供者的文件内容如下所示。

```
FROM java:8 #依赖的基础镜像
COPY nacos-consumer-sample-0.0.1-SNAPSHOT.jar nacos-consumer-sample-0.0.1-SNAPSHOT.jar #复制Jar包
EXPOSE 8086 # 暴露端口
ENTRYPOINT ["java","-jar","nacos-consumer-sample-0.0.1-SNAPSHOT.jar"] #运行Jar包
```
- 其他的项目也是类似的，这样就把构建容器更多的操作（指令）给了Dockerfile了。

- 本文是《Spring Cloud Alibaba微服务实战》书摘之一，如有兴趣可购买书籍。[天猫](https://detail.tmall.com/item.htm?spm=a230r.1.14.40.4d013ed4NkvyPZ&id=650584628890&ns=1&abbucket=3)、[京东](https://item.jd.com/13365970.html)、[当当](http://product.dangdang.com/29275400.html)。书中内容有任何问题，可在本博客下留言，或者到[https://github.com/1030907690](https://github.com/1030907690)提issues。
