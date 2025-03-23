---
layout:					post
title:					"Defender Antivirus占用资源怎么禁止"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
## 前言
- 有时Defender Antivirus 突然磁盘IO很高。导致机器卡得很，开发代码很不方便，本文就介绍如何禁用这个服务。

## 操作
### 下载Defender Control

- [https://www.sordum.org/9480/defender-control-v2-1/](https://www.sordum.org/9480/defender-control-v2-1/) 这是当前的最新版本。
- 下载不了就用云盘地址 ：链接: [https://pan.baidu.com/s/1RorDhm8LaZ0MsXFqNRqn0Q](https://pan.baidu.com/s/1RorDhm8LaZ0MsXFqNRqn0Q) 提取码: ar9g 。解压密码 ： sordum

### 禁用服务
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cb44c9237bc68ca254107e8eadefb1d9.png)
- 首先点击 `Defender_Settings.vbs`关闭实时防护。
- 如何打开软件`dControl.exe`，禁用。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/365afa1cc4c6cd1caa871e119278391a.png)
- 在任务里就没有了

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8847bd5fdbf04659be05b04f73e0494e.png)
