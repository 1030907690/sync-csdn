---
layout:					post
title:					"使用Kubernetes（k8s）+ Docker运行Java服务（续篇）"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 本篇是继[使用Kubernetes（k8s）+ Docker运行Java服务](https://sample.blog.csdn.net/article/details/121061319)之后的续篇，那么到底是续什么呢？
- 前面我们实现了 `复杂目录结构的应用`打包成容器的过程，回顾前面具体过程如下。
	- （1） 拉一个基础的操作系统镜像centos7.7.1908
	- （2）运行这个镜像。
	- （3）docker cp 复制程序进入容器中。
	- （4）写个start.sh脚本。
	- （5）docker commit生成新的镜像。
- 步骤比较多，难道我们每次更新程序都要经历这么多步骤吗？
- 大可不必。我们第一次这样做之后就有了一个基础镜像，在这个基础镜像基础下，写`Dockerfile`生成新镜像。

## 编写Dockerfile文件和生成镜像
- `Dockerfile`文件内容如下所示。

```bash
# 以我们之前生成的login:1.0.0 为基础镜像
FROM login:1.0.0 
# 复制jar包
COPY login-1.0.0-SNAPSHOT.jar login-1.0.0-SNAPSHOT.jar 
```
- 然后生成新的镜像。

```bash
docker build -t   login:1.0.1 .
```
## 重新部署


- 然后复制下login-deployment.yaml，名称就为login-deployment-101.yaml吧，改下k8s deployment配置文件（修改为`image: login:1.0.1`）

```powershell
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
          image: login:1.0.1
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

- 再部署

```powershell
kubectl apply -f login-deployment-101.yaml
```

- 最后删除以前的`deployment`
```powershell
kubectl delete  -f login-deployment.yaml
```
> 这种等新的`deployment`就绪后，再删除旧`deployment`，类似于滚动更新吧！不过我是在手工操作。
## 总结
- 整个思路如下图所示
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f679f902a31ba8fdc552479c19e3ef26.png#pic_center)
- 操作系统能生成新的镜像，把这新的镜像作为Dockerfile基础镜像后，又可以做很多事了。
- 本文的操作步骤还不是很规范，不过能很好认识到`基础镜像`、`新的镜像`、`Dockerfile`的关系，距离`一键部署`，上`Jenkins`等更近一步了。
 