---
layout:					post
title:					"docker usvn搭建和数据恢复"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
#### 一、docker usvn搭建
- 首先拉取镜像`kempkensteffen/usvn` docker hub里面是可以找到的(不拉也行,运行时没有它会自己去拉)
- 运行

```

	 docker run -d -p 8881:80 --name usvn_standard --privileged=true -v /home/svn2/usvn/files:/var/www/usvn/files -v /home/svn2/usvn/config:/var/www/usvn/config kempkensteffen/usvn
```
>-d 表示后台运行
>-p 映射端口出来
>--name 容器名称
>--privileged=true 给权限
>-v 相当于挂载的功能，把一些重要数据挂载到宿主机上，便于数据恢复等等
- 运行起来后就可以访问8881端口了，第一次要安装，安装的时候一般使用sqlite数据库就可以了，后面就是设置一些文件路径、设置管理员信息这些。安装好后，登录进去里面就是一个简单的svn仓库后台管理功能。


#### 二、docker usvn数据恢复
- 上面在搭建是已经把重要数据挂载在宿主机上了，如果docker出了问题，恢复数据也不难办。
- 比较重要的数据是这些
>	 /home/svn2/usvn/files/svn/  这里面是仓库文件数据
	 /home/svn2/usvn/files/authz  这是svn的权限认证文件
	 /home/svn2/usvn/files/htpasswd 这也是svn的权限认证文件
	 /home/svn2/usvn/files/usvn.db  这是usvn的sqlite数据库db文件

- 只要我们在重新搭建usvn的时候把这些文件copy到对应位置就可以了。