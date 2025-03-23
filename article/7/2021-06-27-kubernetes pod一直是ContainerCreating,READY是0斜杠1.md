---
layout:					post
title:					"kubernetes pod一直是ContainerCreating,READY是0/1"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 新创建的nginx-deployment，情况如下所示。

```
[root@localhost software]# kubectl get pods
NAME                              READY     STATUS              RESTARTS   AGE
nginx-deployment-94093859-51185   0/1       ContainerCreating   0          11m
nginx-deployment-94093859-8744s   0/1       ContainerCreating   0          11m
nginx-deployment-94093859-zvbb1   0/1       ContainerCreating   0          11m

```
- 状态一直是`ContainerCreating` ,`READY`是`0/1`  。
## 解决方案
- 查看pod详情，使用命令 `kubectl describe pod nginx-deployment-94093859-51185`（`nginx-deployment-94093859-51185`是我pod名称）。

```
[root@localhost software]# kubectl describe pod nginx-deployment-94093859-51185
Name:		nginx-deployment-94093859-51185
Namespace:	default
Node:		127.0.0.1/127.0.0.1
Start Time:	Sat, 26 Jun 2021 21:30:06 -0400
Labels:		app=nginx
		pod-template-hash=94093859
		track=stable
Status:		Pending
IP:		
Controllers:	ReplicaSet/nginx-deployment-94093859
Containers:
  nginx:
    Container ID:	
    Image:		nginx:1.7.9
    Image ID:		
    Port:		80/TCP
    State:		Waiting
      Reason:		ContainerCreating
    Ready:		False
    Restart Count:	0
    Volume Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-k3tq8 (ro)
    Environment Variables:	<none>
Conditions:
  Type		Status
  Initialized 	True 
  Ready 	False 
  PodScheduled 	True 
Volumes:
  default-token-k3tq8:
    Type:	Secret (a volume populated by a Secret)
    SecretName:	default-token-k3tq8
QoS Class:	BestEffort
Tolerations:	<none>
Events:
  FirstSeen	LastSeen	Count	From			SubObjectPath	Type		Reason		Message
  ---------	--------	-----	----			-------------	--------	------		-------
  12m		12m		1	{default-scheduler }			Normal		Scheduled	Successfully assigned nginx-deployment-94093859-51185 to 127.0.0.1
  12m		1m		7	{kubelet 127.0.0.1}			Warning		FailedSync	Error syncing pod, skipping: failed to "StartContainer" for "POD" with ErrImagePull: "image pull failed for registry.access.redhat.com/rhel7/pod-infrastructure:latest, this may be because there are no credentials on this request.  details: (open /etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt: no such file or directory)"

  11m	7s	50	{kubelet 127.0.0.1}		Warning	FailedSync	Error syncing pod, skipping: failed to "StartContainer" for "POD" with ImagePullBackOff: "Back-off pulling image \"registry.access.redhat.com/rhel7/pod-infrastructure:latest\""

```
有一个错误` "image pull failed for registry.access.redhat.com/rhel7/pod-infrastructure:latest, this may be because there are no credentials on this request.  details: (open /etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt: no such file or directory)"
`。

- 查看`/etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt`后发现是个软链接。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ebf5886809c9c3ed00a647ea24bfa704.png)
- 并且没有 `/etc/rhsm/ca/redhat-uep.pem`文件。
- 尝试直接`docker pull registry.access.redhat.com/rhel7/pod-infrastructure:latest`也拉不下来，也会报找不到文件。
- 只要我们能生成`/etc/rhsm/ca/redhat-uep.pem`文件，问题也就迎刃而解了。
- 有的人用`yum install *rhsm*`解决了问题，但是在我的电脑上不行，所以下面是另一个方案。
  - 1、下载python-rhsm-certificates-1.19.10-1.el7_4.x86_64.rpm文件

	```
	 wget http://mirror.centos.org/centos/7/os/x86_64/Packages/python-rhsm-certificates-1.19.10-1.el7_4.x86_64.rpm
	```
   - 2、生成`/etc/rhsm/ca/redhat-uep.pem`文件

		```
			rpm2cpio python-rhsm-certificates-1.19.10-1.el7_4.x86_64.rpm | cpio -iv --to-stdout ./etc/rhsm/ca/redhat-uep.pem | tee /etc/rhsm/ca/redhat-uep.pem
     ```
- 再次拉取`registry.access.redhat.com/rhel7/pod-infrastructure:latest`，执行命令 `docker pull registry.access.redhat.com/rhel7/pod-infrastructure:latest`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7b8726b73d61827da08e01f82b3ed17b.png)
- 再次查看pod状态，已经正常了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e4269c60dad9aea38bdcf46f3c110c75.png)
- docker进程运行状态如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/77900f72d82bd4a5a9f9f2d563975855.png)



