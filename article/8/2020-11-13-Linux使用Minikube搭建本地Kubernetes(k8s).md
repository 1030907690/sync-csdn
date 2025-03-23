---
layout:					post
title:					"Linux使用Minikube搭建本地Kubernetes(k8s)"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
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
本篇使用的是`minikube`。
## 搭建的预置条件
- 操作kubernetes的命令行工具`kubectl`。
- 容器，这里选择`Docker`。
## 安装命令行工具kubectl
- 官方文档：[https://kubernetes.io/docs/tasks/tools/install-kubectl/](https://kubernetes.io/docs/tasks/tools/install-kubectl/)。
- 一般有两种方式（二选一）。
	- 二进制文件。
	- 软件包管理进行安装。
### 第一种方式Kubectl二进制文件
- 下载kubectl文件
 
```bash
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
```
以上命令是下载最新版，如果需要选择版本安装，请使用如下命令，下载 `v1.19.0`版本。

```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.19.0/bin/linux/amd64/kubectl
```

- 增加执行权限

```bash
chmod +x ./kubectl
```
- 移动到`/usr/local/bin/`路径下。

```bash
sudo mv ./kubectl /usr/local/bin/kubectl
```
- 验证是否成功，查看版本。

```bash
kubectl version --client
```
### 第二种方式软件包管理进行安装
#### CentOS，RHEL或Fedora系统
- 添加源。

```bash
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
```
- yum安装。

```bash
yum install -y kubectl
```
#### Ubuntu，Debian或HypriotOS系统
- 添加软件源。

```bash
sudo apt-get update && sudo apt-get install -y apt-transport-https gnupg2 curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
```
- 更新和安装。

```bash
sudo apt-get update
sudo apt-get install -y kubectl
```
 ## 安装Docker
 - 官方文档：[https://docs.docker.com/engine/install](https://docs.docker.com/engine/install)。
- 使用yum命令安装yum-utils软件包和设置稳定的存储库，使用命令如下所示。

```bash
yum install -y yum-utils #安装yum-utils
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo # 设置存储库
```

- 安装Docker CE和containerd。使用命令如下所示。

```bash
yum install -y docker-ce docker-ce-cli containerd.io  #安装最新版
```

上面的命令是直接安装最新版的，如果想要指定版本安装，可以使用如下命令列出可用的版本。

```bash
yum list docker-ce --showduplicates | sort -r # 列出可用版本
```

列出可用版本后，选择一个版本，使用如下命令即可。

```bash
yum install docker-ce-<VERSION_STRING> docker-ce-cli-<VERSION_STRING> containerd.io # 安装指定版本，用版本号把<VERSION_STRING>替换即可
```

- 安装完成后就可以启动了，启动命令如下所示。

```bash
systemctl start docker
```

- 启动完成后，查看Docker版本和使用hello-world镜像并运行它来验证Docker是否安装成功，使用命令运行结果如下。

```bash
docker version  # 查看Docker版本命令
```
```bash
Client: Docker Engine - Community
 Version:           19.03.13
 API version:       1.40
 Go version:        go1.13.15
 ...省略...
Server: Docker Engine - Community
 Engine:
  Version:          19.03.13
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.13.15
...省略...
docker run hello-world  # 运行hello-world镜像命令
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
0e03bdcc26d7: Pull complete 
...省略...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...省略...
```

注意：当本地不存在这个镜像时，使用docker run命令会先去尝试下载。
运行结果是成功的，表示安装完成。
其他命令：
（1）关闭Docker：`systemctl stop docker`。
（2）重启Docker：`systemctl restart docker`。
## 安装Minikube
- 下载minikube。

```bash
curl -Lo minikube https://kubernetes.oss-cn-hangzhou.aliyuncs.com/minikube/releases/v1.14.2/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
```
## 使用Minikube
- 启动，`不要使用root用户`。

```bash
minikube start
```
>可选参数：
--driver=*** 从1.5.0版本开始，Minikube缺省使用本地最好的驱动来创建Kubernetes本地环境，测试过的版本 docker, kvm
--image-mirror-country cn 将缺省利用 registry.cn-hangzhou.aliyuncs.com/google_containers 作为安装Kubernetes的容器镜像仓库 （阿里云版本可选）
--iso-url=*** 利用阿里云的镜像地址下载相应的 .iso 文件 （阿里云版本可选）
--registry-mirror=***为了拉取Docker Hub镜像，需要为 Docker daemon 配置镜像加速，参考阿里云镜像服务
--cpus=2: 为minikube虚拟机分配CPU核数
--memory=2048mb: 为minikube虚拟机分配内存数
--kubernetes-version=***: minikube 虚拟机将使用的 kubernetes 版本

如果要求选择容器，可以使用如下命令。

```bash
minikube start --driver=docker
```

 注意：机器配置最好是`2核CPU2G内存及以上`。 如果出现 `dial unix /var/run/docker.sock: connect: permission denied`权限问题，可使用命令`sudo chmod 777 /var/run/docker.sock`临时解决。
 
- 打开Kubernetes控制台，`不要使用root用户`。

```bash
minikube dashboard
```
控制台如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2f9aa1b271828c3363a53ff2fafd36bd.png#pic_center)

## 参考
- [https://developer.aliyun.com/article/221687](https://developer.aliyun.com/article/221687)
