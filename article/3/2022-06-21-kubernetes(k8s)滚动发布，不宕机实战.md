---
layout:					post
title:					"kubernetes(k8s)滚动发布，不宕机实战"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 之前一直想怎么能让自己的服务在发布的时候也能提供服务，做到无缝衔接。所幸k8s就提供滚动发布的功能。下面我们先了解下什么是滚动发布。

## 滚动发布
- 滚动发布就是在升级过程中，先启动一台新版本的服务，等新的那台服务稳定后，就把旧的一台服务干掉，后面的老版本服务都是这样替换的过程。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d89e783206461b0fd53b155c0eb56cfd.png)

 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d04eeb45f8de49c09645d6623e1974c8.png)
- 虚线部分表示服务已经被替换掉了。
- 理论来说可以实现更新时使用户无感知，做到无缝衔接。
## 开始前的准备
### 镜像
- 首先就是镜像。[https://hub.docker.com/r/a1030907690/centos_java/tags](https://hub.docker.com/r/a1030907690/centos_java/tags)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/31a0c25dc774a33009872e40bbf7969e.png)

> 这个镜像其实是我学`kubernetes ConfigMap`的时候准备的，`ConfigMap`怎么使用可参考拙作[kubernetes(k8s) ConfigMap实战](https://sample.blog.csdn.net/article/details/124822703)。
- 看过[kubernetes(k8s) ConfigMap实战](https://sample.blog.csdn.net/article/details/124822703)就知道这2个版本没什么差别，只是`7.7.1909`版本的打印增加了`customValue`。
- 我要做的就是把`7.7.1908`升级到`7.7.1909`。
### k8s配置文件
- k8s的配置文件(spring-boot-kubernetes-deployment.yaml)如下代码。
> a1030907690/centos_java:7.7.1908 ;a1030907690/centos_java:7.7.1909我一早就下载好了。

```yaml
 # 把jar包打到centos里的办法
# 从本地文件创建ConfigMap kubectl create cm spring-boot-kubernetes-conf --from-file=application.yml
# 修改 kubectl edit cm spring-boot-kubernetes-conf  ，也可以先删除 kubectl delete cm spring-boot-kubernetes-conf 再从本地文件创建
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spring-boot-kubernetes-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: spring-boot-kubernetes-deployment
  template:
    metadata:
      labels:
        app: spring-boot-kubernetes-deployment
    spec:
      containers:
        - name: spring-boot-kubernetes
          image: a1030907690/centos_java:7.7.1908
          command: [ "java","-jar","spring-boot-kubernetes-0.0.1-SNAPSHOT.jar" ]
          imagePullPolicy: Never # 只使用本地镜像，防止ErrImagePull异常
          ports:
            - containerPort: 8080
          env: # 解决Java程序时区问题
            - name: TZ
              value: Asia/Shanghai
          volumeMounts:
            - name: config
              mountPath: /config  # 应用配置文件路径
      volumes:
        - name: config
          configMap:
            name: spring-boot-kubernetes-conf  # 这个名字与创建时对应
            items:
              - key: application.yml
                path: application.yml
```
>  注意：这个配置并不完美，先埋个伏笔。

### 验证工具
- 我使用`JMeter`一直调用接口，然后执行滚动发布，看汇总结果就可以了。当然也可以使用其他工具（手写一个也行呀）。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0fa3c3371a27dc7bd18af10ec1eea2a2.png)
## 实战
- 执行命令，创建`deployment`。

```bash
kubectl apply -f spring-boot-kubernetes-deployment.yaml 
```
- 创建`service`的过程就不演示了。可以参考拙作[使用Kubernetes（k8s）+ Docker运行Java服务](https://sample.blog.csdn.net/article/details/121061319)。


- 运行`JMeter`观察接口是否一直能通，如下图所示。
> 中途我会使用`kubectl set image  deployment/spring-boot-kubernetes-deployment  spring-boot-kubernetes=a1030907690/centos_java:7.7.1909 --record`来滚动更新。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/72d4d1cd2f431225d949942b0ad189a2.gif)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9cc6831636998092cddcffc15a7a48d4.png)
- 可以看到有异常情况发生，有的请求不通。
- 本想实现更新时不宕机，无缝衔接，我这波被打脸了。

## 问题
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2e7337ef259d12b718c32b622e2c1893.jpeg#pic_center)
- 经过大半天的苦战，各处搜索，多方实战。终于让我发现了问题。
	- k8s就绪检查：在新的`pod`创建后，这是程序正在初始化，请求不应该转发到新的pod，并且旧`pod`的也不应该在新`pod`真正能接收请求前被删除。配置k8s的`就绪探测器`可以解决。
	- 删除pod前的优雅停机：旧的`pod`内部可能还有些请求未处理，有可能是个耗时操作，我们需要实现优雅停机，简单的利用睡眠，在删除`pod`前阻塞一点时间，给程序多一些时间处理未完成的请求。

- 要解决前面的问题，我新建了yaml文件配置(spring-boot-kubernetes-deployment-rolling-publishing.yaml)，配置如下。
 
```yaml
# 参考 https://www.jianshu.com/p/c63c9efaeac3
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
          image: a1030907690/centos_java:7.7.1908
          command: [ "java","-jar","spring-boot-kubernetes-0.0.1-SNAPSHOT.jar" ]
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
          volumeMounts:
            - name: config
              mountPath: /config  # 应用配置文件路径
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh","-c","echo this pod is stopping. > /stop.log && sleep 90s"]
      volumes:
        - name: config
          configMap:
            name: spring-boot-kubernetes-conf  # 这个名字与创建时对应
            items:
              - key: application.yml
                path: application.yml


```
>`terminationGracePeriodSeconds` 终止宽限期秒属于是一个总的时间控制，默认值是`30s`,如果不修改这个值，后面`preStop`钩子里`sleep 90s`是无效的。

## 再次实战
- 再创建deployment

```bash
kubectl apply -f spring-boot-kubernetes-deployment-rolling-publishing.yaml 
```
- 滚动更新命令还是一样的。

```bash
kubectl set image  deployment/spring-boot-kubernetes-deployment  spring-boot-kubernetes=a1030907690/centos_java:7.7.1909 --record
```
- 依旧来看Jmeter的结果，如下所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/20ea8f4ac85a9878287c9ac3ee95dd05.gif)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/53518f1b3ea593afb0cd40b0cf5b5e67.png)
- 这次滚动发布就没有问题了。实现了不宕机，无缝衔接。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/93aed53e2b8b3c276e7369beafc4dd8f.gif#pic_center)
- 删除`pod`的宽限期差不多是`300`秒，和`terminationGracePeriodSeconds`配置的差不多。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/967b0d91f8aa0dfa9520b8d7ea840e16.png)
> web管理后台我用的是`kubesphere`

- 滚动更新其他命令（`spring-boot-kubernetes-deployment`是我的deployment）。



	- 查看滚动更新状态

	```
	kubectl rollout status deployment/spring-boot-kubernetes-deployment
	```
	
	
	- 历史记录
	```
	kubectl rollout history  deployment/spring-boot-kubernetes-deployment
	
	```
	
	
	- 查看某个历史详情
	```
	kubectl rollout history  deployment/spring-boot-kubernetes-deployment --revision=2
	```
	
	- 回滚(回到上次)
	 ```
	 kubectl rollout undo  deployment/spring-boot-kubernetes-deployment
	 ```
	
	- 回滚(回到指定版本)
	```
	kubectl rollout undo deployment/spring-boot-kubernetes-deployment --to-revision=2
	```


## 小结
- k8s真的很强大，滚动发布很好用，只需要一些配置就可以了。理论上任何编程语言的程序都可以使用。为企业发布程序解决了大难题。
- 不过滚动发布是不像灰度（金丝雀）发布那样可以细粒度控制流量。只要发布好的状态流量就会进来。所以要求生产发布的程序保证经过严密测试，如果到处bug，造成脏数据就尴尬了。
## 参考
- [https://zhuanlan.zhihu.com/p/42671353](https://zhuanlan.zhihu.com/p/42671353)
- [https://www.jianshu.com/p/c63c9efaeac3](https://www.jianshu.com/p/c63c9efaeac3)