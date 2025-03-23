---
layout:					post
title:					"Jenkins kubernetes(k8s)滚动发布实战"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 前面写过一篇文章，[kubernetes(k8s)滚动发布，不宕机实战](https://blog.csdn.net/baidu_19473529/article/details/125361620)已经实现了滚动发布，不过还得手工输命令，本篇呢想通过`Jenkins`实现一键操作。使发布应用效率提高。
- 其实像`KubeSphere`这类的工具也是集成了`Jenkins`的，之所以直接使用`Jenkins`，是因为那种大而全的工具必然会损耗资源，而我又用不上那么多的功能。
## 开始前的准备
- JDK环境。
- kubernetes。
- Jenkins。安装好之后需要一些基础配置，可以参考拙作[gitlab+jenkins自动发布到Tomcat](https://blog.csdn.net/baidu_19473529/article/details/106139890)。
- Docker。
- 我使用的项目地址是： [https://github.com/1030907690/spring-boot-kubernetes](https://github.com/1030907690/spring-boot-kubernetes)。
## 第一次创建应用

- 首先需要一个yaml文件（deployment.yaml），参考[kubernetes(k8s)滚动发布，不宕机实战](https://blog.csdn.net/baidu_19473529/article/details/125361620)，去掉了`ConfigMap`的配置和`command`，代码如下。

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spring-boot-kubernetes-deployment
spec:
  replicas: 2
  strategy:
    rollingUpdate:
      maxSurge: 1 # 最大峰值用来指定可以创建的超出期望 Pod 个数的 Pod 数量。此值可以是绝对数（例如，5）或所需 Pods 的百分比（例如，10%）
      maxUnavailable: 0 #最大不可用  是一个可选字段，用来指定 更新过程中不可用的 Pod 的个数上限。该值可以是绝对数字（例如，5）也可以是所需 Pods 的百分比（例如，10%）
  selector:
    matchLabels:
      app: spring-boot-kubernetes-deployment
  template:
    metadata:
      labels:
        app: spring-boot-kubernetes-deployment
    spec:
      terminationGracePeriodSeconds: 300 #如果需要的优雅终止时间比较长 (preStop + 业务进程停止可能超过 30s)，可根据实际情况自定义 terminationGracePeriodSeconds，避免过早的被 SIGKILL杀死,与下面preStop有关联，300属于总时间
      containers:
        - name: spring-boot-kubernetes
          image: spring-boot-kubernetes:1.0.0
      
          imagePullPolicy: Never # 只使用本地镜像，防止ErrImagePull异常
          ports:
            - containerPort: 8080
          readinessProbe: #就绪探针
            httpGet:
              path: /
              port: 8080
            initialDelaySeconds: 50 #容器启动后要等待多少秒后才启动存活和就绪探测器， 默认是 0 秒，最小值是 0
            periodSeconds: 5  # 指定了 kubelet 应该每 5 秒执行一次存活探测。
            successThreshold: 1 #探测器在失败后，被视为成功的最小连续成功数。默认值是 1。 存活和启动探测的这个值必须是 1。最小值是 1。
            failureThreshold: 2 #当探测失败时，Kubernetes 的重试次数。 对存活探测而言，放弃就意味着重新启动容器。 对就绪探测而言，放弃意味着 Pod 会被打上未就绪的标签。默认值是 3。最小值是 1
          env: # 解决Java程序时区问题
            - name: TZ
              value: Asia/Shanghai
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh","-c","echo this pod is stopping. > /stop.log && sleep 90s"]
```
- 我需要`spring-boot-kubernetes:1.0.0`这个镜像，我手动创建一下。
 > Dockerfile文件和jar同一级目录

 
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5366ff85f88936eddfa7d742ec59d7e0.png)

- `Dockerfile`文件内容。

```bash
FROM openjdk:8
ADD spring-boot-kubernetes-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT [ "java", "-jar", "/app.jar"]
```

- 然后用命令。

```bash
 docker build -t spring-boot-kubernetes:1.0.0 .
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d795d4686f2c1069cfce7935672c883e.png)


- 开始首次运行，创建应用。

```bash
 kubectl apply -f deployment.yaml
```

- 运行了2个Pod，如下所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0ef1b4b1f740b11abd2c6c748eba2fbc.png)

## 操作Jenkins
- 怎么下载、运行Jenkins就不赘述了，可以参考拙作[gitlab+jenkins自动发布到Tomcat](https://blog.csdn.net/baidu_19473529/article/details/106139890)。
- `Jenkins`配置`maven、jdk、git等等`同样可以参考拙作[gitlab+jenkins自动发布到Tomcat](https://blog.csdn.net/baidu_19473529/article/details/106139890)。
- 下面直接创建自由风格项目。进入配置。
### General
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2792269c2b69be4807209c9a498cabcc.png)

### 源码管理
- 源码管理填写仓库地址和分支，因为我是公共项目，所以不需要帐号密码。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1d485f8cde683a0563f753accbe12e21.png)
### 构建

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/20b64b9dd47b095c0fdd4c2e651d2900.png)

- 先用`maven`打包
> 这里不需要加mvn
- 然后执行脚本。

```bash
#!/bin/bash
sh rolling_update.sh
```

- `rolling_update.sh`脚本内容。

```bash
 #!/bin/bash
ls
cp src/main/resources/Dockerfile target 
ls target
cd target
date=`date "+%Y%m%d%H%M%S"`
# 构建镜像
docker build -t spring-boot-kubernetes:$date .
# 滚动更新
kubectl set image  deployment/spring-boot-kubernetes-deployment  spring-boot-kubernetes=spring-boot-kubernetes:$date --record
# 查看Pod情况
kubectl get pod -o wide
# 查看滚动更新状态
kubectl rollout status deployment/spring-boot-kubernetes-deployment
# 查看Pod情况
kubectl get pod -o wide
```
- `Dockerfile`文件内容。

```bash
FROM openjdk:8
ADD spring-boot-kubernetes-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT [ "java", "-jar", "/app.jar"]
```






## Jenkins构建
- 下面就可以使用`Build Now`一键发布最新的应用。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e3eb909b892479d165bffe17bddca17e.png)
- 可以查看构建历史，如果有错误的时候，方便排查错误。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/da7e46667c007e535d0c826e06b05df7.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/98fe814ef3a161de270e1fb37ccdd2f7.png)
- 如果你不想点`Build Now`，也可以使用`Webhook`，可以参考拙作[gitlab+jenkins自动发布到Tomcat](https://blog.csdn.net/baidu_19473529/article/details/106139890)。
- 以上就把Jenkins和kubernetes(k8s)结合起来实现滚动发布了。
## 小结
- 本文先把应用创建一次。然后`Jenkins`就做滚动发布的事情，分成这2个步骤。