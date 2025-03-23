---
layout:					post
title:					"使用certbot生成https证书"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
 ## 背景
 - 本篇是继[使用Let's Encrypt免费SSL证书](https://blog.csdn.net/baidu_19473529/article/details/80868632)之后的文章，因为我发现使用原来GitHub项目方式在大部分服务器会报：

```
Skipping bootstrap because certbot-auto is deprecated on this system.
Your system is not supported by certbot-auto anymore.
Certbot cannot be installed.
Please visit https://certbot.eff.org/ to check for other alternatives.

```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c98f730904c93836d911826a640245ff.png)
- 然后就没有然后了。
- 在`GitHub issues`搜索一波后，发现说`certbot-auto已被弃用`，如下图所示（原文链接:[https://github.com/certbot/certbot/issues/8535](https://github.com/certbot/certbot/issues/8535)）：
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8368f205b621a59c39561547a1f6da79.png)
- 最上面的提问这里说snap的certbot版本可以正常工作。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b78d2007c652292fe5ae15fd5acf6515.png)

- 通过`GitHub issues`我们知道需要使用`snap`或许能解决问题，命令打印提示到[https://certbot.eff.org/](https://certbot.eff.org/)寻找替代方案。
- 几经波折，经过一番摸索后，我终于从入门到会用，整理了下分享给大家。
## 全部操作步骤概览
### 1、打开https://certbot.eff.org
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/99a151fd225f4ec9bc3910dada1ea695.png)
### 2、选择自己用的什么软件并且是什么操作系统
- 我的是Centos7 Nginx所以选择的是这样的组合。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1caf93e4ea354a6eabcc2243be560c19.png)
### 3、查看操作步骤
- 下面就是具体的操作
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f703bde98775c913b3498784dbb63e4f.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6458cb186124618f1fbf9e68cd4a52f9.png)
> 下面的实战细节主要针对在Centos系统 + Nginx/Openresty软件上，之所以有前面的`全部操作步骤概览`，就为了遇到其他系统或软件举一反三，然后参考下面的实战操作。应该是大同小异。
## 实战细节
### 安装snap
- 官方文档：[https://snapcraft.io/docs/installing-snapd](https://snapcraft.io/docs/installing-snapd)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b087e2d52b97503a559880c44fa4acaa.png)
- 因为我是`Centos`，所以点击`CentOS`。进入 [https://snapcraft.io/docs/installing-snap-on-centos](https://snapcraft.io/docs/installing-snap-on-centos)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b553c5b491b2647c253b0bc8eb0f6626.png)

> 注意下自己系统的版本。
- 我的是centos7运行以下命令安装`snap`。

```
# 将EPEL添加到CentOS 7
yum install epel-release   
#安装snapd
yum install snapd
#安装后，需要启用用于管理主快照通信套接字
systemctl enable --now snapd.socket
# 启用快照支持
ln -s /var/lib/snapd/snap /snap
```
>我是root用户运行，所以没有加sudo
- 确保安装的snap是最新的。

```
 snap install core
 snap refresh core
```
> 这2条命令估计要多尝试几次，第1次有可能失败，我的失败了2次

### 安装Certbot
- 使用snap命令安装：

```
 snap install --classic certbot
```
- 增加软链接

```
ln -s /snap/bin/certbot /usr/bin/certbot
```

### 生成证书
- 生成证书前的准备
	- 1、域名解析到当前操作的服务器。
	- 2、制作nginx的软链接。
	> 因为我安装的是openresty，默认是不能不加路径就直接nginx命令的，所以我使用命令，ln -s /usr/local/openresty/nginx/sbin/nginx /usr/bin/nginx 制作软链接。
	- 3、安装`python-certbot-nginx`，这是nginx插件。
	> Centos使用`yum install python-certbot-nginx`命令，Ubuntu使用`apt install python-certbot-nginx`命令。

- 生成证书有2条命令`certbot --nginx`（获取证书，并让Certbot自动编辑Nginx配置以为其提供服务）和`certbot certonly --nginx`（只生成证书，手动更改Nginx配置）
- 我比较保守，所以使用的是只生成证书的命令。

```
certbot certonly --nginx
```
- 还有个问题，运行这个命令，它会去`/etc/nginx`目录去找配置文件，而我是手动安装的`openresty`，配置文件并不在/etc/nginx下，所以要指定配置文件目录，最终命令如下所示。

```
certbot certonly --nginx --nginx-server-root=/usr/local/openresty/nginx/conf
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bfee15fb0549d1b220f9d1a8022b2c83.png)
- 运行命令后，它会把所有配置的域名列出来，然后选择编号就可以了，最下面就是我们生成的证书路径了。
- 手动改下配置文件。内容如下所示。

```
server {
    listen       443 ssl;
    server_name  xxx.xxx.com;
    ssl_certificate /etc/letsencrypt/live/xxx.xxx.com-0001/fullchain.pem;
    ssl_certificate_key  /etc/letsencrypt/live/xxx.xxx.com-0001/privkey.pem;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
    ssl_prefer_server_ciphers on;
    ...省略...
}
```

- 重启`nginx/openresty`就可以了，一气呵成，收工。
### 续期
- 证书会过期，续期的基础命令如下所示。
```
certbot renew --dry-run
```
> 这个命令我暂时没用，等我用的时候再更新下本文，预计又会有配置文件路径问题。


> 该命令已测试，没有配置文件路径问题，直接运行即可，更新于2021年6月29日13:36:30。
## 常见问题整理
### Could not choose appropriate plugin: The nginx plugin is not working; there may be problems with your existing configuration

```
Could not choose appropriate plugin: The nginx plugin is not working; there may be problems with your existing configuration.
The error was: NoInstallationError("Could not find a usable 'nginx' binary. Ensure nginx exists, the binary is executable, and your PATH is set correctly.")
```
- 两步解决
	- 1、安装nginx插件，Centos使用`yum install python-certbot-nginx`命令，Ubuntu使用`apt install python-certbot-nginx`命令，原文链接[https://github.com/certbot/certbot/issues/1736](https://github.com/certbot/certbot/issues/1736)。
	- 2、制作nginx软链接：如下命令：
	```
	ln -s /usr/local/openresty/nginx/sbin/nginx /usr/bin/nginx
	```
