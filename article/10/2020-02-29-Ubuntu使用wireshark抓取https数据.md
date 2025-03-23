---
layout:					post
title:					"Ubuntu使用wireshark抓取https数据"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[toc](目录)
### 简介
- 一般来说这些抓包工具是无法直接看到https的真实数据；但也是有办法的。
- 解决办法大概有以下几种
	-  中间人攻击(这一类工具有：Fiddler、Charles 和 whistle);
	- 设置web服务器使用RSA作为交换密钥算法;
	- 如果是用chrome,firefox，可以设置导出pre-master-secret log，然后wireshark设置pre-master-secret log路径，这样就可以解密了。

- 本文会介绍使用第三种办法

### 安装wireshark
- 直接使用命令
```shell
 sudo apt install wireshark
```
- 默认情况下，`tcpdump`的权限是`root:root`，普通用户运行wireshark无法调用`tcpdump`，会报没有权限，导致无法抓包。为了让普通用户也可以使用wireshark

 
```bash
sudo chmod +x /usr/sbin/tcpdump
```
### 配置环境变量抓取所有https网站
-  首先编辑`~/.profile`文件，为什么编辑它而不是`~/.bashrc`？因为`~/.profile`中的变量可以用于所有软件，而`~/.bashrc`里的变量只能用在`Terminal`中，即`Ctrl + Alt + T`打开的终端。而通常我们打开`Chrome`浏览器是直接点击图标，而不是在`Terminal`运行`google-chrome`命令。
- `vim ~/.profile`加入

```bash
export SSLKEYLOGFILE=/home/zzq/temp/sslkey.log
```
- 这个`sslkey.log`文件会在`chrome`运行时自己创建和写入，所以自己可以不创建它。

- 注销当前用户，打开`wireshark`和`chrome`，wireshark选择哪个网卡就不说了，看自己的电脑环境。
- 进入后把视图->解析名称 里面全部勾上；这样信息方便观察；菜单栏`Edit`——`Preferences`——`Protocols`——`SSL`（注意，不论是SSL还是TLS这里都是SSL，没有单独的TLS选项），在`(Pre)-Master-Secretlog filename`中选择刚才设置的变量值。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d901392ac3989de92e52a3e50394fdfb.png)
- 网站的话，我就以我的csdn主页为例；`https://blog.csdn.net/baidu_19473529`
- 首先简单的设置下过滤规则`ssl and ip.addr==47.95.47.253`后面的ip地址是我`ping   blog.csdn.net`出来的，csdn这种大网站肯定不是单服务，每个人每个地区可能ip都不一样。
- 这样设置过后会软件显示都不一样了，有些会出现`Decrypted  SSL`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1397362fd84359a757f4027111d5ed30.png)
- 我请求`https://blog.csdn.net/baidu_19473529`后得到这些信息； 这里有个请求`/api/ArticleHighWords/list`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/37464336dffd50f7cf961117b2879840.png)
- 验证下请求和返回数据对不对
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a576442eb2c1d510974f8a9339f55137.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/387b8234165c38d2936dde3eec7b60c6.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1ba59ff4e1e912e6f54804f46640aec4.png)

- 结果是一致的，成功了。

### 手机https抓包
- 如果是手机https抓包的话，可以使用Fiddler、Charles 和 whistle这类的根据做代理；也就是前面说的第一种方法。后面我实际操作后有时间再把详细步骤写下了。
### 其他工具

- 抓https包还可参考本人以下拙作，手机的话一般设置代理，安装好证书就行。（更新于2022年8月13日09:10:07）
	- [绕过反调试fuck-debugger](https://blog.csdn.net/baidu_19473529/article/details/122768471)（使用whistle）
	- [mitmproxy篡改返回数据实战](https://blog.csdn.net/baidu_19473529/article/details/125362907)

