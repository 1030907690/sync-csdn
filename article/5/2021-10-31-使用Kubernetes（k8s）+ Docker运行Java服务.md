---
layout:					post
title:					"使用Kubernetes（k8s）+ Docker运行Java服务"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 前面写下了[几乎最简搭建本地kubernetes（k8s）环境](https://sample.blog.csdn.net/article/details/118459686)，环境是搭建好了，但并不算真正应用上。本篇以运行Java服务为例把k8s真正用起来。
- 首先，k8s要用的是镜像(`image`)，要让k8s运行我们的java服务，java服务必须要做成一个`镜像（image）`。面对只有一个jar包的应用，写个`Dockerfile`就搞定了。
- 不过，面对复杂的目录结构应用，我用`Dockerfile`始终有问题，后面找到一种几乎万能的办法，用一个操作系统作为基础镜像自己自定义一个镜像。下面就会讲到这两种方式。



## 单个Jar的应用
- 这个应用就一个Jar包，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/acf4ba0b3f2ceb365ff02c0f18ce8dda.png)
### Dockerfile
- `Dockerfile`文件内容如下。

```bash
# 基础镜像
FROM java:8 
COPY fastpay-mgr.jar app.jar # 复制jar包
# 暴露端口
EXPOSE 9090 
 # 启动时运行的命令
ENTRYPOINT ["sh","-c","java  -Xms256m -Xmx512m -jar app.jar"]
```
> 注意：Dockerfile文件内容代码后面的注释会引发报错
- 执行命令 `docker build -t fastpay-mgr:1.0.0 .`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d994402ae07a29e2a9c007b4c32734a3.png)
- 执行成功后，用`docker images`命令就能看到新的镜像了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dcd447c06af86ec5c221e6016d7c9bbe.png)
### deployment配置文件和运行
- 接下来，就写k8s的deployment yml文件。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastpay-mgr
spec:
  replicas: 1 # 运行副本个数
  selector:
    matchLabels:
      app: fastpay-mgr
  template:
    metadata:
      labels:
        app: fastpay-mgr
    spec:
      containers:
        - name: fastpay-mgr
          image: fastpay-mgr:1.0.0 # 使用的镜像
          imagePullPolicy: Never # 只使用本地镜像，防止ErrImagePull异常
          ports:
            - containerPort: 9090
          env: # 解决Java程序时区问题
            - name: TZ
              value: Asia/Shanghai
```
- 然后`kubectl apply -f fastpay-mgr-deployment.yml`运行
- 使用`kubectl get deployment`查看，READY状态正常为启动成功
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/163af9eccfe6233f02196c22cc749df6.png)

## 复杂目录结构的应用
- 上面的情况比较比较简单，只有一个Jar包；我遇到了另一种目录结构比较复杂的，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ec9daa7b7652ccfacc8134786ea45440.png)
- 这里面有`主Jar包`，`依赖包`、`配置文件`。这种上k8s比较麻烦。把整个操作系统拉下来，自己自定义下还是能解决的。
### 基础镜像
- 我以centos7.7.1908为基础镜像，先拉下来。

```shell
docker pull centos:centos7.7.1908
```
- 再运行它

```shell
docker run  -i -t centos:centos7.7.1908 bash
```
- 进入这个系统后，安装jdk、把要运行的程序复制(利用`docker cp` 命令)进来,复制后结果如下图所示（因为根目录有lib目录，所以我改成了libs）。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b7ec1981177a309f91e32d71fc391f4c.png)

- 然后在根目录写个`start.sh`脚本。内容如下。
```

#!/bin/bash
java -server -Dfile.encoding=UTF-8 -Xms512m -Xmx512m -cp libs/*:login-1.0.0-SNAPSHOT.jar com.xxx.xxx.xxx.login.LoginApplication
```
> 注意：k8s运行程序必须前台运行，不能加nohub、& 这些。如果遇到执行命令后就立即返回，建议用tail -f xxx.log的方式保持前台运行。
### 生成新镜像
- `docker commit`，生成新的镜像。
	- 找到刚才`docker run`时的`CONTAINER ID`，然后`docker commit  xxx  login:1.0.0`(我这里新生成的镜像是login:1.0.0)，docker commit详情参考[docker保存对容器的修改](https://sample.blog.csdn.net/article/details/69857313)。
- 有了镜像，下面编写k8s deployment文件

### deployment配置和运行
```yml
# 把jar包打到centos里的办法, 依赖包分离的情况
apiVersion: apps/v1
kind: Deployment
metadata:
  name: login-deployment
spec:
  replicas: 1 # 副本数量
  selector:
    matchLabels:
      app: login-deployment
  template:
    metadata:
      labels:
        app: login-deployment
    spec:
      containers:
        - name: login-deployment
          image: login:1.0.0
          #java命令-Dfile.encoding=UTF-8不能放最后，否则无效
          # command 运行java命令必须是多个字符串，把命令写在前面，不然会报no such file or directory: unknown
          # start.sh文件内容 java -Dfile.encoding=UTF-8  -cp libs/*:login-1.0.0-SNAPSHOT.jar  com.xxx.xxx.xxx.login.LoginApplication
          command: [  "/bin/sh","start.sh" ]
          imagePullPolicy: Never # 只使用本地镜像，防止ErrImagePull异常
          ports:
            - containerPort: 8089
          env: # 解决Java程序时区问题
            - name: TZ
              value: Asia/Shanghai

```
- 最后运行`kubectl apply -f login-deployment.yml`。
## Service
- 由于Pod的ip地址是我们无法预知的，每次创建k8s会自动分配，所以k8s推出Service来解决这个问题。创建出的Service的ip是相对固定的，只要声明好配置，它们之间k8s会帮我们做好映射关系。
- Service是主要用来做负载均衡，提供应用统一入口的，这里以前面的`fastpay-mgr`为例，为它做一个`Service`,以`NodePort`方式，配置如下。
```yml
apiVersion: v1
kind: Service
metadata:
  name: fastpay-mgr-service-nodeport
spec:
  selector:
    app: fastpay-mgr #这里要和前面对应
  ports:
    - name: http
      port: 9090 # 暴露出来访问的端口
      protocol: TCP
      targetPort: 9090 # 目标端口
  type: NodePort
```
- `kubectl apply -f fastpay-mgr-service.yml`运行
- k8s会提供一个集群地址，就可以通过，`集群地址:9090`调用程序了。

## 总结
- 如何得到镜像：从本文中有两种方式。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b722b2b9315c131ee21f2c2d9655d405.png)

- 第一种、写个`Dockerfile`，然后`docker build`。
- 第二种、以`一个操作系统作为基础镜像`（例如Centos）,然后`docker commit`。
- 比较复杂的情况选择第二种方式，几乎适用全部的应用类型。
- 本文仅描述了如何使用Kubernetes（k8s）+ Docker运行Java服务,殊途同归，大道归一，其他语言的应用也是类似的方法。