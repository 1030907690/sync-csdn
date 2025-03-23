---
layout:					post
title:					"kubernetes(k8s) ConfigMap实战"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
-  `ConfigMap`将配置和容器分离，容器外挂配置，当有变更时，改动`ConfigMap`，便可以全局生效。相当于一个`配置中心`的角色。

- 下面我将以一个简单的Java应用为例，部署运行。利用`ConfigMap`把配置外挂进来。看下会有什么效果。

## 实战
### 从本地文件创建ConfigMap
- 创建`ConfigMap`的方式，推荐从本地文件创建而不是直接命令，这样好维护些。
- 我们先建立`application.yml`文件，里面内容非常简单，代码如下。

```yaml
server:
  port: 8080
custom:
  value: 'test'
```
- 开始创建，使用如下命令。

```bash
 kubectl create cm spring-boot-kubernetes-conf --from-file=application.yml
```
- 我们可以使用 `kubectl get cm`查看是否创建成功，成功后会出现`spring-boot-kubernetes-conf`，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e7036543cb4312198bb25f771ba87ba3.png)
### 程序镜像
- 我就不再赘述怎么把程序包成一个镜像了，感兴趣的可以参考拙作[使用Kubernetes（k8s）+ Docker运行Java服务](https://blog.csdn.net/baidu_19473529/article/details/121061319)。
-  我使用的程序是我之前上传的一个镜像，地址[https://hub.docker.com/r/a1030907690/centos_java/tags](https://hub.docker.com/r/a1030907690/centos_java/tags)
- 我拉下来，改了下名字。
```bash
docker tag a1030907690/centos_java:7.7.1909 centos:7.7.0
```
### Deployment配置文件
- 要让k8s运行我们的应用肯定要告诉它怎么运行，推荐使用yaml配置文件的方式。新建`spring-boot-kubernetes-deployment.yaml`配置文件如下所示。

```yaml
# 把jar包打到centos里的办法
# 从本地文件创建ConfigMap kubectl create cm spring-boot-kubernetes-conf --from-file=application.yml
# 修改 kubectl edit cm spring-boot-kubernetes-conf  ，也可以先删除 kubectl delete cm spring-boot-kubernetes-conf 再从本地文件创建
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spring-boot-kubernetes-deployment
spec:
  replicas: 1
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
          image: centos:7.7.0
          command: [ "java","-jar","spring-boot-kubernetes-0.0.1-SNAPSHOT.jar" ]
          imagePullPolicy: Never # 只使用本地镜像，防止ErrImagePull异常
          ports:
            - containerPort: 8080
          env: # 解决Java程序时区问题
            - name: TZ
              value: Asia/Shanghai
          volumeMounts:
            - name: config
              mountPath: /config  #应用配置文件路径
      volumes:
        - name: config
          configMap:
            name: spring-boot-kubernetes-conf  # 这个名字与创建时对应
            items:
              - key: application.yml
                path: application.yml
```
> 注意：镜像中的应用Jar包里是有配置文件`application.yml`的。这里取个巧。Spring Boot配置加载是有优先级的，高优先级的内容会覆盖底优先级的内容，形成互补配置。这里`config`文件夹配置高。
> 因为大家配置key是相同的，`config`文件夹里的配置文件优先级比`Jar包里`的高。所以这里会使用`config`文件夹里的配置。
### 运行程序
- 下一步，运行

```bash
kubectl apply -f spring-boot-kubernetes-deployment.yaml
```
- 查看运行状态，使用`kubectl get pod`命令。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3d894302e5f491f30f31406ce7ffca81.png)


- 使用`kubectl get pod -o wide`找到Pod的地址，访问下看是否成功。
 
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cf3713396c68f12143f71caa6ed3178f.png)

### 查看配置文件
- 进入Pod，使用如下命令。

```bash
 kubectl exec -i -t spring-boot-kubernetes-deployment-569bc8bcbc-jtjgv -- bash
```

- 查看配置文件，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/595270d3eee7a2c50ac59207c34e07ad.png)

- 很明显是生成了物理文件的。
### 修改配置
- 假设有个配置要修改或者新增配置key。
- 我来修改下`custom.value`，把配置文件变成这样：

```yaml
server:
  port: 8080
custom:
  value: 'test val'
```
- 我们可以使用`kubectl edit cm spring-boot-kubernetes-conf`直接编辑。
- 但还是推荐从本地文件修改。再删除、再新建一次。

```bash
vim application.yml
kubectl delete cm spring-boot-kubernetes-conf
kubectl create cm spring-boot-kubernetes-conf --from-file=application.yml
```
- 然后我们隔几分钟进入容器，就会惊奇地发现`application.yml`已经同步到刚才的更改，如下图所示。 
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7fbd0de4c19c07c46403dab217a2290d.png)
- 文件已经更新了，然后我们访问一下，看应用有没有使用最新配置。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0e6c01e51fc6df4a162dbb9ae1a34dee.png)
- 依旧是旧的配置。
- 之所以做这样的测试，是想说明`ConfigMap`只会更新物理文件。要使应用能获取最新配置，还得我们`自己实现配置热更新`。
## 小结
- `ConfigMap`还是非常方便的，可以替代`配置中心`了，当然`热更新要自己实现`。可以说整个`k8s体系`对我们的应用回归纯业务代码开发有很大帮助（以后可能每天只能`CURD`了😂）。可以替代`配置中心`、`服务注册、发现`等纯技术性代码开发，业务与技术分离。还有它是与编程语言无关的，即使用`Python`等开发也是一样的。

- 下面表格是Kubernetes与Spring Cloud微服务常用解决方案的对比。

|功能 |Kubernetes |	Spring Cloud |
|--| -- | --|
|弹性伸缩|	根据配置自动伸缩 |	- |
|服务注册、发现|	Service |	Spring Cloud Eureka 、Spring Cloud Alibaba Nacos|
|配置中心|	ConfigMap、Secret(Secret主要用来存密码) |	Spring Cloud Config、Spring Cloud Alibaba Nacos |
|服务网关|	Ingress |	Spring Cloud Zuul 、Spring Cloud Gateway|
|服务安全|	RBAC API(解决服务层面的访问控制问题)|	Spring Cloud Security|
|负载均衡|	Service  |	Spring Cloud Ribbon|
|跟踪监控|	Metrics API |Spring Cloud Turbine|
|降级熔断|	- |Spring Cloud Hystrix 、Spring Cloud Alibaba Sentinel|

- 可以看出Kubernetes对于`降级熔断`比较无力，不过`服务网格`（例如`istio`）可以解决这个问题。