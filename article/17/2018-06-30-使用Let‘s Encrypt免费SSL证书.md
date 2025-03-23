---
layout:					post
title:					"使用Let‘s Encrypt免费SSL证书"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
### 一、获取https证书的途径
>- 1、服务提供方(如国内的阿里云、腾讯云等等都可以申请免费或者收费的https证书)
- 2、Let's Encrypt证书
- 3、还有其他的...（目前我不知道了）

### 二、Let's Encrypt
 >- Let's Encrypt作为一个公共且免费SSL的项目逐渐被广大用户传播和使用，是由Mozilla、Cisco、Akamai、IdenTrust、EFF等组织人员发起，主要的目的也是为了推进网站从HTTP向HTTPS过度的进程，目前已经有越来越多的商家加入和赞助支持。
 >- 详情可去Let's Encrypt官网介绍[Let's Encrypt官网介绍](https://letsencrypt.org/about/)

### 三、使用Let's Encrypt生成https证书
>- 1、使用git下载项目，运行生产证书

 

```bash
 git clone https://github.com/certbot/certbot
cd certbot
./certbot-auto certonly --standalone --email xxx@qq.com -d www.abc.com -d mall.abc.com
 
```

> - 2、certbot-auto命令介绍生成证书的命令,--email是你的域名联系人邮箱地址,-d是你要生的哪个域名地址的证书，可同时生成多个域名证书,就是多个-d；生成过程有提示的话agree和yes即可。
>- 3、此步生成证书可能的异常

```
Plugins selected: Authenticator standalone, Installer None
	Obtaining a new certificate
	Performing the following challenges:
	http-01 challenge for xxxx.xxxx.com
	Cleaning up challenges
	Problem binding to port 80: Could not bind to IPv4 or IPv6.
```
>- 4、这个异常报的就是80端口被占用,因为我是开着Nginx的，Nginx端口就是80,我关了之后就好了(如果被占用,是生成不了证书文件的)。
>- 5、查看生成的文件,生成的证书位于/etc/letsencrypt/下；live文件夹里面有证书文件
>`cert.pem - Apache服务器端证书
chain.pem - Apache根证书和中继证书
fullchain.pem - Nginx所需要ssl_certificate文件
privkey.pem - 安全证书KEY文件`
>- 6、配置Nginx使https生效,配置在server下面。

```
server
	{
	    listen 443 ssl;
	    server_name abc.com;
	    ssl_certificate      /etc/letsencrypt/live/abc.com/fullchain.pem;
	    ssl_certificate_key  /etc/letsencrypt/live/abc.com/privkey.pem;
	    location / {
```
>- 7、重启Nginx就可以用https访问了。
>- 8、续期问题：Let's Encrypt证书是有效期90天的，需要我们自己手工更新续期才可以。
>命令例子:

```
./letsencrypt-auto certonly --renew-by-default --email xxx@qq.com -d abc.com -d mall.abc.com
```
>这样又可以继续使用90天。


### 四、其他
- 报错 Client with the currently selected authenticator does not support any combination of challenges that will satisfy the CA. You may need to use an authenticator plugin that can do challenges over DNS.
- 我在生成泛域名的时候遇到这个错，命令格式应该是:
> - ./certbot-auto certonly --email 1057421xx@qq.com -d *.xxx.com --preferred-challenges dns --manual
> - 或者 ./certbot-auto  certonly --preferred-challenges dns --manual  -d *.xxx.com --server https://acme-v02.api.letsencrypt.org/directory
 
- 途中会出现txt值
```bash
Are you OK with your IP being logged?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: Y

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please deploy a DNS TXT record under the name
_acme-challenge.xxx.com with the following value:

xxxxjQYXG3lDlg

Before continuing, verify the record is deployed.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

```

> 注意要dns验证加入txt值
### 该方法可能对某些机器上已失效，如果失效请移步下篇 [使用certbot生成https证书](https://sample.blog.csdn.net/article/details/114277125) 更新于2021年6月29日09:42:56