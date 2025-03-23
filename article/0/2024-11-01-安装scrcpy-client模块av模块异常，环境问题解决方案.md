---
layout:					post
title:					"安装scrcpy-client模块av模块异常，环境问题解决方案"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
## 背景
- 使用 `pip install scrcpy-client`命令出现以下报错
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/59be31a7449f45dcaf1efbb6e7ba58cc.png)

```
 performance hint: av\logging.pyx:232:5: Exception check on 'log_callback' will always require the GIL to be acquired.
Possible solutions:
1. Declare 'log_callback' as 'noexcept' if you control the definition and you're sure you don't want the function to raise exceptions.
2. Use an 'int' return type on 'log_callback' to allow an error code to be returned.
```
- 搜索时发现是环境问题，我的是最新python 3.12 还没有对应的av支持模块，得使用低版本python才行。原文地址 [https://stackoverflow.com/questions/77410272/problems-installing-python-av-in-windows-11](https://stackoverflow.com/questions/77410272/problems-installing-python-av-in-windows-11)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c59bcff0838c4372ab6df4ce53a6824b.png)
- 我并不想卸载当前的3.12版本，于是想到了`conda`。

## 解决方案

- conda下载地址 [https://www.anaconda.com/download/success](https://www.anaconda.com/download/success)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/4f103edc1d6e4dbbb351af610f355c66.png)
- 安装好后使用如下cmd命令
```shell
#创建python 3.10.13的环境  gamed 名称可自定义
conda create -n gamed python=3.10.13
# 激活 gamed 虚拟环境后，你的命令行前面会多出虚拟环境的名称 
conda activate gamed
```
- 在python 3.10.13环境中执行`pip  install scrcpy-client`终于成功了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/bfb56845519c4c38a8012c93396e14e4.png)
- 为了方便开发中使用，所以在pycharm中配置上conda创建的环境。
	- 第一步
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/79e535381e0849a4a41e305f05c07e68.png)
	-  第二步
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/73d208ace7b0412693884238902462e2.png)
- 现在就有python 3.10.13的环境了













