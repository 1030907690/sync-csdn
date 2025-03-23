---
layout:					post
title:					"Oracle VM VirtualBox NAT网络ping不通"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 为了换了网络`IP`地址也一样，所以用了`NAT`网络，但`Oracle VM VirtualBox`的`NAT`似乎与`VMware`的`NAT`模式不一样，无法连上，也`ping不通`。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/19f9d2aeaa9ee4d913f8336dd8968104.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/71d50843783ebea254d19240c476b638.png)

## 解决方案
### 设置端口转发
- 解决方案就是设置`端口转发`。下面开始设置。
- 在`Oracle VM VirtualBox`主界面点击`设置`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a7c86c5851d0257faf5459ed1e3ffac4.png)
- 选择`网络`，点击`高级`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/447193dbab71a365234f1063a46ccb2b.png)
- 进入`端口转发`,设置端口转发规则。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/01f958e2454e39d09633280510e51bfb.png)
> 该配置表示本机222端口映射到虚拟机22端口。映射其他端口也是同样的道理。
### 测试
- 下面我使用`127.0.0.1 222`开始连接Linux虚拟机。使用命令如下。
```bash
ssh root@127.0.0.1  -p 222
```
- 连接成功，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/177cd136d31567704b877c3fae04eea6.png)
## 其他问题（更新于2022年5月16日17:50:17）
### 端口转发后登录慢
- 登录简直是龟速
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/319947b217144423dcbf62165ad6223a.png)

- 解决办法不要dns解析。

```bash
vim /etc/ssh/sshd_config
```
放开注释的`UseDNS`并修改为`no`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/da62b6e8afdaa5af36d78f7d46d934aa.png)
- 重启ssh服务

```bash
systemctl restart sshd.service
```

- 效果登录很快了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/86b70b2c8c0a4340623b4ee8895aac77.gif)



## 参考
- [http://ask.apelearn.com/question/9986](http://ask.apelearn.com/question/9986)

 
