---
layout:					post
title:					"VMware Intel i5-10400 安装Mac 14 Sonoma"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
#  安装完后的效果
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/740ecb1a70cfff3cd4d9eadd21977d6f.png)


# 安装前的准备
- 开启CPU虚拟化。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/92cba8dc5e6542926bf15fbe701fd21f.png)


- VMware虚拟机（我使用的版本是17.5.0 build-22583795） ，激活码可以网上找。
- MacOS 14  ISO镜像（我是在[https://sysin.org/blog/macOS-Sonoma/](https://sysin.org/blog/macOS-Sonoma/)下载的）。
- VMware解锁MacOS工具，下载地址 [https://github.com/DrDonk/unlocker](https://github.com/DrDonk/unlocker)或 [https://github.com/BDisp/unlocker](https://github.com/BDisp/unlocker)。解压后管理员运行unlock.exe。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5cea7b4939531e25c3f71f3bf62a5d5b.png)
# 创建虚拟机
## 创建虚拟机，选择典型安装。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/36e01eae955a761cf03a73bc8cb7d553.png)

## 选择ISO文件

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/98849ba755f6d9be58fb8f457e971b8c.png)

## 选择系统类型
-  `如果这一步没有 Mac OS那就是解锁没成功`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a6becb7eefa3ac1a143a21f6bbcc7b2c.png)

## 命名虚拟机
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/95716a10196e34664b441955bbc823cc.png)

## 设置磁盘

> 单个文件：读速比较快，但是系统负载比较大，占用内存高。
>多文件：读速一般，但是占用内存小，系统负载小。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a24023f7822b1fda3e5d987c940dad92.png)

## 完成
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b8b425452f506bd26ea6c6afb62a46ee.png)

# 配置虚拟机文件
## 修改配置文件
- 打开虚拟机目录，找到vmx文件。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f8c51d77307ac90a6e8016e7b616f35c.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c6a3eb8642a8d3de31ed6efac3e0a833.png)

- 改动这2行：

```
 board-id.reflectHost = "FALSE" 
ethernet0.virtualDev = "vmxnet3"
```

 - 新增内容（如果登录Apple帐户 ： MOBILEME_CREATE_UNAVAILABLE_MAC，serialNumber 自己改一下数值）：

```
board-id = "Mac-AA95B1DDAB278B95" 
hw.model.reflectHost = "FALSE" 
hw.model = "MacBookPro19,1" 
serialNumber.reflectHost = "FALSE" 
serialNumber = "C02154569190"
```


# 第一次运行虚拟机

## 选择语言
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6fe476652d704608f013ea2f003280e0.png)

## 选择磁盘工具

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/12f1a91d0375072347072ebc28e2bb2a.png)
## 格式磁盘
- 点击抹掉。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ed9907c8e0c2d667f7a5caff5085b46e.png)
- 完成后，退出磁盘工具。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d6831ae684188f8c8f3ebe8eedd56e9e.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/65a8289c50cbe2968b2d969953f81837.png)

## 安装macOS Sonoma
- 继续，然后同意。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/de70c10f489ce42bf3399cf0bc766d80.png)
- 选择安装在磁盘。点继续。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b7eddd367a94144d8a04f1a824dba772.png)
- 安装需要一些时间。如出现 安装Mac提示安装无法继续,因为安装器已损坏 ，请参考 我的另一篇文章 [安装Mac提示安装无法继续,因为安装器已损坏](https://blog.csdn.net/baidu_19473529/article/details/135607073)，排查下是不是文件的问题。

- ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cf0dfe1485fd1b76bbc7c59e11e98ac8.png)


![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bc5ed4a49411921aa1c338b3d6285492.png)

- 后面就是配置系统的引导，按照中文说明配置就行。

# 其他问题

## 登录Apple帐户 ： MOBILEME_CREATE_UNAVAILABLE_MAC
- 修改serialNumber值

## AMD安装Mac 14 Sonoma
- 我尝试在AMD R5-5600G上安装Mac 14，但多次没有成功，Mac 12可以成功，Intel CPU比较好安。


# 参考
- [https://zhuanlan.zhihu.com/p/658521465](https://zhuanlan.zhihu.com/p/658521465)