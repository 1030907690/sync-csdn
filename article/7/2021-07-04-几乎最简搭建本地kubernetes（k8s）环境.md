---
layout:					post
title:					"几乎最简搭建本地kubernetes（k8s）环境"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---

@[TOC](目录)
## 前言
- 去年我用的是`Minikube`，并写过一篇[Linux使用Minikube搭建本地Kubernetes(k8s)](https://sample.blog.csdn.net/article/details/109675448)，今年我再使用这个`Minikube`，好家伙，给我报了一大堆错，想着`Minikube`就不去纠结它了，正式环境不太可能用这个；索性直接正儿八经的安装下`kubernetes`。这里做个记录。
## 简介
- `Kubernetes` 是一套容器集群管理系统，是一个开源平台，可以实现容器集群的自动化部署、自动扩缩容、维护等功能，充分发挥容器技术的潜力，给企业带来真正的便利。 `Kubernetes` 拥有自动包装、自我修复、横向缩放、服务发现、负载均衡、自动部署、升级回滚、存储编排等特性，不仅支持`Docker`，还支持`Rocket`。`Kubernetes`与`DevOps`、微服务等相辅相成，共同推进现代的数字化变革。
>以上摘抄自《Kubernetes从入门到实战》
- `Kubernetes` 源于希腊语，意为 "舵手" 或 "飞行员"。是目前最流行的容器编排系统，简单地来说主要功能就是管理容器的。旨在提供“跨主机集群的自动部署、扩展以及运行应用程序容器的平台”。它支持一系列容器工具, 包括`Docker`等。
## 为什么要用Kubernetes
- 自带服务发现和负载均衡功能。
- 存储编排，允许您自动挂载您选择的存储系统。
- 自动部署和回滚。
- 自动二进制打包。
- 自我修复，重新启动失败的容器、替换容器、杀死不响应用户定义的运行状况检查的容器。
- 密钥与配置管理。
## 搭建Kubernetes的方式
- `软件包管理工具`安装。
- `kubeadm`：是一个工具，用于快速搭建kubernetes集群。
- `Minikube`：用于本地开发、测试和学习。
- `二进制包`：官网下载相关的组件的二进制包，手动安装。
- `KubeSphere`：利用kubernetes `restful api`管理kubernetes，提供友好的dashboard界面，安装时可选择 `Linux 上以 All-in-One 模式`一键安装。官方文档[https://kubesphere.com.cn/docs/quick-start/all-in-one-on-linux/](https://kubesphere.com.cn/docs/quick-start/all-in-one-on-linux/)

本篇使用的是`软件包管理工具`，我的操作系统是`Centos`，所以使用的是`yum`。
## 节点规划
- 为了能达到标题上`几乎最简`，避免从入门到放弃，我们只使用一台主机。
	- 我们只需要`1个Etcd`、`1个Master`、`1个Node`。
	- 像`Flannel`、`CoreDNS`组件先不管，这些是和网络相关的，要你的集群规模比较大才会用到，本篇的目的搭建环境后能完成常用的练习就好了。
 - 下面用表格展示出规划。

| IP | 名称 | 
| --- | --- |
|192.168.42.133| Etcd|
|192.168.42.133| Master|
|192.168.42.133| Node|

## 安装前准备
- 禁用SELinux。

```
[root@localhost ~]# setenforce 0
setenforce: SELinux is disabled
```
- 禁用firewalld。

```
[root@localhost ~]# systemctl stop firewalld
[root@localhost ~]# systemctl disable firewalld
```
- 更新软件包（可选）。

```
[root@localhost ~]# yum -y update
```
- 同步系统时间（可选）。

```
 [root@localhost ~]# yum install -y ntpdate
 [root@localhost ~]# ntpdate -u cn.pool.ntp.org
  4 Jul 01:27:20 ntpdate[2732]: adjust time server 94.237.64.20 offset -0.062611 sec
```
- 生成`/etc/rhsm/ca/redhat-uep.pem`文件，如果没有会遇到`image pull failed for registry.access.redhat.com/rhel7/pod-infrastructure:latest, this may be because there are no credentials on this request. details: (open /etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt: no such file or directory)`。
 
  - 1、下载python-rhsm-certificates-1.19.10-1.el7_4.x86_64.rpm文件

	```
	 wget http://mirror.centos.org/centos/7/os/x86_64/Packages/python-rhsm-certificates-1.19.10-1.el7_4.x86_64.rpm
	```
   - 2、生成`/etc/rhsm/ca/redhat-uep.pem`文件

		```
			rpm2cpio python-rhsm-certificates-1.19.10-1.el7_4.x86_64.rpm | cpio -iv --to-stdout ./etc/rhsm/ca/redhat-uep.pem | tee /etc/rhsm/ca/redhat-uep.pem
     ```
## 安装、配置、启动Etcd
- 安装

```
 [root@localhost ~]# yum install -y etcd
```

- 修改配置文件。

```
[root@localhost ~]# vim /etc/etcd/etcd.conf
```
- 主要修改`ETCD_LISTEN_PEER_URLS`、`ETCD_INITIAL_ADVERTISE_PEER_URLS`、`ETCD_INITIAL_CLUSTER`

```
#[Member]
#ETCD_CORS=""
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
#ETCD_WAL_DIR=""
ETCD_LISTEN_PEER_URLS="http://localhost:2380"
ETCD_LISTEN_CLIENT_URLS="http://localhost:2379"
#ETCD_MAX_SNAPSHOTS="5"
#ETCD_MAX_WALS="5"
ETCD_NAME="default"
#ETCD_SNAPSHOT_COUNT="100000"
#ETCD_HEARTBEAT_INTERVAL="100"
#ETCD_ELECTION_TIMEOUT="1000"
#ETCD_QUOTA_BACKEND_BYTES="0"
#ETCD_MAX_REQUEST_BYTES="1572864"
#ETCD_GRPC_KEEPALIVE_MIN_TIME="5s"
#ETCD_GRPC_KEEPALIVE_INTERVAL="2h0m0s"
#ETCD_GRPC_KEEPALIVE_TIMEOUT="20s"
#
#[Clustering]
ETCD_INITIAL_ADVERTISE_PEER_URLS="http://localhost:2380"
ETCD_ADVERTISE_CLIENT_URLS="http://localhost:2379"
#ETCD_DISCOVERY=""
#ETCD_DISCOVERY_FALLBACK="proxy"
#ETCD_DISCOVERY_PROXY=""
#ETCD_DISCOVERY_SRV=""
ETCD_INITIAL_CLUSTER="default=http://localhost:2380"
#ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
#ETCD_INITIAL_CLUSTER_STATE="new"
#ETCD_STRICT_RECONFIG_CHECK="true"
#ETCD_ENABLE_V2="true"
#
#[Proxy]
#ETCD_PROXY="off"
#ETCD_PROXY_FAILURE_WAIT="5000"
#ETCD_PROXY_REFRESH_INTERVAL="30000"
#ETCD_PROXY_DIAL_TIMEOUT="1000"
#ETCD_PROXY_WRITE_TIMEOUT="5000"
#ETCD_PROXY_READ_TIMEOUT="0"
#
#[Security]
#ETCD_CERT_FILE=""
#ETCD_KEY_FILE=""
#ETCD_CLIENT_CERT_AUTH="false"
#ETCD_TRUSTED_CA_FILE=""
#ETCD_AUTO_TLS="false"
#ETCD_PEER_CERT_FILE=""
#ETCD_PEER_KEY_FILE=""
#ETCD_PEER_CLIENT_CERT_AUTH="false"
#ETCD_PEER_TRUSTED_CA_FILE=""
#ETCD_PEER_AUTO_TLS="false"
#
#[Logging]
#ETCD_DEBUG="false"
#ETCD_LOG_PACKAGE_LEVELS=""
#ETCD_LOG_OUTPUT="default"
#
#[Unsafe]
#ETCD_FORCE_NEW_CLUSTER="false"
#
#[Version]
#ETCD_VERSION="false"
#ETCD_AUTO_COMPACTION_RETENTION="0"
#
#[Profiling]
#ETCD_ENABLE_PPROF="false"
#ETCD_METRICS="basic"
#
#[Auth]
#ETCD_AUTH_TOKEN="simple"

```
- 启动etcd

```
 systemctl start etcd
```
- 设为开机自启动（可选）

```
systemctl enable etcd
```

- 查看状态，使用 `systemctl status etcd`， active (running)表示启动成功。或者使用 `etcdctl cluster-health`命令 is healthy表示成功，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/827bc1231ddf6cc26ce7cbcfb4fb5078.png)
## 安装、配置、启动Master
- 安装

```
[root@localhost ~]# yum install -y kubernetes-master
```
- 生成密钥（如果没有创建Pod会失败，报 `No API token found`）

```
 openssl genrsa -out /etc/kubernetes/serviceaccount.key 2048
```

- 修改配置文件

```
[root@localhost ~]# vim /etc/kubernetes/apiserver
```
- 修改`KUBE_API_ADDRESS`、`KUBE_API_ARGS`

```
# The address on the local server to listen to.
KUBE_API_ADDRESS="--address=0.0.0.0"

# The port on the local server to listen on.
# KUBE_API_PORT="--port=8080"

# Port minions listen on
# KUBELET_PORT="--kubelet-port=10250"

# Comma separated list of nodes in the etcd cluster
KUBE_ETCD_SERVERS="--etcd-servers=http://127.0.0.1:2379"

# Address range to use for services
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"

# default admission control policies
KUBE_ADMISSION_CONTROL="--admission-control=NamespaceLifecycle,NamespaceExists,LimitRanger,SecurityContextDeny,ServiceAccount,ResourceQuota"

# Add your own!
 KUBE_API_ARGS="--service_account_key_file=/etc/kubernetes/serviceaccount.key"

```
- 修改kube-controller-manager配置文件`vim /etc/kubernetes/controller-manager`。

```
###
# The following values are used to configure the kubernetes controller-manager

# defaults from config and apiserver should be adequate

# Add your own!
KUBE_CONTROLLER_MANAGER_ARGS="--service_account_private_key_file=/etc/kubernetes/serviceaccount.key"

```

- 启动

```
[root@localhost ~]# systemctl start kube-apiserver
[root@localhost ~]# systemctl start kube-controller-manager
[root@localhost ~]# systemctl start kube-scheduler
```
- 开机自启动（可选）

```
[root@localhost ~]# systemctl enable kube-apiserver
[root@localhost ~]# systemctl enable kube-controller-manager
[root@localhost ~]# systemctl enable kube-scheduler
```
- 查看状态，使用以下命令。

```
 systemctl status kube-scheduler
 systemctl status kube-apiserver
 systemctl status kube-controller-manager
```
- 结果如下表示启动成功。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/94b800c1d77be35d7f7e850e2b84267b.png)

## 安装、配置、启动Node
- 安装，容器我们选择使用`Docker`。

```
 [root@localhost ~]# yum install  -y kubernetes-node  docker
 #安装完成后启动docker
 [root@localhost ~]# systemctl start docker
```

- 这里有3个配置文件， `/etc/kubernetes/config`、`/etc/kubernetes/proxy`、`/etc/kubernetes/kubelet`。
- 因为我们是单机，所以 `/etc/kubernetes/config`和`/etc/kubernetes/kubelet`可以不动，只修改`/etc/kubernetes/proxy`，修改后内容如下。

```
 ###
# kubernetes proxy config

# default config should be adequate

# Add your own!
KUBE_PROXY_ARGS="--bind-address=0.0.0.0"

```
- 启动

```
[root@localhost ~]# systemctl start kube-proxy
[root@localhost ~]# systemctl start kubelet
```
- 设置开机自启动（可选）

```
[root@localhost ~]# systemctl enable kube-proxy
[root@localhost ~]# systemctl enable kubelet
```
- 查看node是否启动成功。

```
[root@localhost ~]# kubectl get nodes
NAME        STATUS    AGE
127.0.0.1   Ready     7d
```
已经有1个node节点了。

## 测试验证
#### 创建Deployment
- 测试我们的kubernetes是否搭建成功，就创建一个nginx的deployment试试。
- 新建`nginx-deployment.yaml`文件，内容如下。

```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3  # 3个副本
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
- 然后开始创建。

```
[root@localhost software]# kubectl apply -f nginx-deployment.yaml 
```
- 使用 `kubectl get deployment`命令查看是否创建成功。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6522229f24f4f28f78f1bba48aadaf82.png)
- 使用`kubectl get pods`查看pod信息。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b5181e81e37a8979eb818682607dece0.png)
- 使用 `kubectl get pods -o wide`查看详情。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/72747c50837971a302117d8b038369c2.png)
- 我们现在可以通过`curl`命令访问下nginx服务，来验证服务是否启动成功，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/aeca39cd0aa45652da31dde034119230.png)
测试结果3个服务都是访问成功的。


#### 创建Service
- 我们知道，kubernetes是可以动态伸缩的，每当新的Pod创建时，IP是不一样的，我们肯定要给前台提供一个相对稳定的地址。这就需要Service（服务）了，它能自动发现，并将请求转发到对应Pod中。有点类似我们应用系统`网关`的概念了。
- 这里我们使用`NodePort`的方式创建Service。
- 新建`nginx-service.yaml`文件。内容如下。
```
apiVersion: v1
kind: Service
metadata:
  name: nginx-service-nodeport
spec:
  selector:
    app: nginx
  ports:
    - name: http
      port: 8000
      protocol: TCP
      targetPort: 80
  type: NodePort
```
- 开始创建

```
[root@localhost software]# kubectl apply -f nginx-service.yaml 
service "nginx-service-nodeport" created
```

- 查看服务

```
[root@localhost software]# kubectl get svc
NAME                              CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes                        10.254.0.1      <none>        443/TCP          7d
nginx-service-nodeport            10.254.56.192   <nodes>       8000:31047/TCP   20s
```
- 然后我们可以使用curl命令， CLUSTER-IP + 端口访问。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4f926cb5c34ee073fa7c878d273da77f.png)
-  Service会给我们做负载均衡，所以每次发起的请求，进入的可能不是同一个Pod。这里我没有改文件内容所以看不出来，有兴趣的可以自动登录到Pod修改下文件内容，就可以看到。


## 常见问题

#### 创建Deployment后没有Pod（No API token found）。详情参考[创建Deployment后没有Pod](https://sample.blog.csdn.net/article/details/118265804)。
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

#### kubernetes pod一直是ContainerCreating,READY是0/1，详情参考[kubernetes pod一直是ContainerCreating,READY是0/1](https://sample.blog.csdn.net/article/details/118267036)。
- 具体异常
 

```
image pull failed for registry.access.redhat.com/rhel7/pod-infrastructure:latest, this may be because there are no credentials on this request.  details: (open /etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt: no such file or directory)
```

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