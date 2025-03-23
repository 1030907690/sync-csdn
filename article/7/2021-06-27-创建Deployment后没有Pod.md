---
layout:					post
title:					"创建Deployment后没有Pod"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 我创建一个nginx的Deployment，配置文件如下所示。

 

```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    metadata:
      labels:
          app: nginx
          track: stable
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80

```
- 执行命令`kubectl apply -f nginx-deployment.yaml`。Deployment和Pod的结果如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8ea90f284f8c0b5b909824466f89f0dc.png)
- 并没有创建Pod。
## 查看日志，寻找原因
  -  使用`kubectl apply -f nginx-deployment.yaml`命令后，会交给api-server，然后以对象形式存到etcd里，这时候kube-controller-manager会通过循环的方式来编排工作，创建相应的Pod。所以我们应该看 `kube-controller-manager`服务的日志。
#### 第一种查看办法
- 我们使用`journalctl`查看使用systemctl启动的service。
- 使用`journalctl -u  kube-controller-manager`命令，结果如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/61cb457a1022fff739d6e4564d82fc6c.png)

```
... 省略...
Jun 26 20:58:12 localhost.localdomain kube-controller-manager[8152]: E0626 20:58:12.999019    8152 replica_set.go:448] Sync "default/nginx-deployment-94093859" failed with unable to create pods: No API token found for service account "default", retry after the token is 
... 省略 ...
```

#### 第二种查看办法
- 查看系统日志。
- 使用` tail -f /var/log/messages`命令。结果如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/aa5a9446f407d86c584c6b7221bdbe97.png)

```
...省略...
 Jun 26 20:58:03 localhost kube-controller-manager: E0626 20:58:03.980854    8152 replica_set.go:448] Sync "default/nginx-deployment-94093859" failed with unable to create pods: No API token found for service account "default", retry after the token is automatically created and added to the service account
 ...省略...
 
```

## 解决方案
- 问题原因就是 `No API token found` ，我们创建token就可以了。
- 生成密钥。

```
 openssl genrsa -out /etc/kubernetes/serviceaccount.key 2048
```

- 修改/etc/kubernetes/apiserver内容，`vim /etc/kubernetes/apiserver`。

```
 ...省略...
 KUBE_API_ARGS="--service_account_key_file=/etc/kubernetes/serviceaccount.key"
```
- 修改kube-controller-manager配置文件`vim /etc/kubernetes/controller-manager`。
```
 ...省略...
 KUBE_CONTROLLER_MANAGER_ARGS="--service_account_private_key_file=/etc/kubernetes/serviceaccount.key"
```
- 重启服务

```
systemctl restart etcd kube-apiserver kube-controller-manager kube-scheduler
```
- 删除后重新创建成功，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5161172849f1d360be3ee5888e88619e.png)
