---
layout:					post
title:					"绕过反调试fuck-debugger"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 遇到个网站感觉还不错，想用`F12`,看看地址，没想到有反调试，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b5763b413533b1e5bd741fa00d52948d.png)
- 就卡在了`fuck-debugger.js`。

- 下面我们来突破它。

## 所需工具
- `whistle`  (需要先安装nodejs，正向代理时使用)。
- `nginx` （替换文件时使用）
- `SwitchyOmega`(一个浏览器插件),如果没有这个可以设置全局代理，下面会说到Windows 10的设置方法。


## 安装whistle
- 要先安装nodejs。
- 安装whistle命令

```powershell
  npm install -g whistle
```
- 启动

```powershell
w2 start
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5c50cda22cd98990d31bb0799d5f75bd.png)

## 配置SwitchyOmega
### SwitchyOmega
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3e2ab4370cd7774374077ab3e6e4ec9c.png)
- 当前页面切换到w2配置。

### 没有SwitchyOmega
- 如果没有SwitchyOmega这个插件，可以设置全局代理，以`Windows 10`为例，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c527384323f77a19ced37989ea4ee13b.png)
- 然后点保存。



## 保存和修改fuck-debugger.js
- 开启`nginx`，然后把文件下载下来，按自己需求修改一点。
- 我注释了`3`处代码，本地服务如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c129eefc3d3013113686bb5328bb4bcf.png)
- 下面我们来配置`whistle`
## 配置whistle
- 打开`http://localhost:8899/`

```powershell
https://xxxx.com/xxx/statics/js/fuck-debugger.js http://127.0.0.1/fuck-debugger.js
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1186e0e4c76d03099995f49d7a2c257b.png)
- 记得保存哦

- 因为是https的所有要下载安装证书,勾选Capture TUNNEL CONNECTs


![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c84f64e62e46b81ead0bd11e5c3616fd.png)
- 下载完成后点击安装
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3eff89ec0768641d8dfefec834a17517.png)
- 重启浏览器

- 现在打开F12,就没有烦人的debug了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/97f577b0c3310603ece0bfca6012074a.png)
