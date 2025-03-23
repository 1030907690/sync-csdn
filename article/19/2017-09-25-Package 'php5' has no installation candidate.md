---
layout:					post
title:					"Package 'php5' has no installation candidate"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
国内下载docker镜像大部分都比较慢，下面给大家介绍2个镜像源。


### 一、阿里云的docker镜像源
 > 注册一个阿里云用户,访问 [https://cr.console.aliyun.com/#/accelerator](https://cr.console.aliyun.com/#/accelerator) 获取专属Docker加速器地址
 > ![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/2321c1619a521e66a41dd90eb1d3e172.png)
 
使用的时候修改/etc/docker/daemon.json文件就可以了，修改保存后重启 Docker 以使配置生效




### 二、docker中国官方的镜像源
> ![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/c79dc16f28adfdf12ba574ad2d239b18.png)

大致上操作都是一样的，修改/etc/docker/daemon.json文件

```
vi /etc/docker/daemon.json
```

然后加入代码

```
{
  "registry-mirrors": ["https://registry.docker-cn.com"]
}
```
这是永久性保留更改,修改保存后重启 Docker以使配置生效