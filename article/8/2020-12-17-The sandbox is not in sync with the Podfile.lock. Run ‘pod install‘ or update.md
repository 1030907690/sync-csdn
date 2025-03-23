---
layout:					post
title:					"The sandbox is not in sync with the Podfile.lock. Run ‘pod install‘ or update"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- xcode编译运行时报错`The sandbox is not in sync with the Podfile.lock. Run 'pod install' or update`，这是依赖的问题。
## 解决方案
### 安装CocoaPods
- OS X 10.11以前，在终端输入以下命令：
```bash
 sudo gem install cocoapods
```
OS X 10.11以后，在终端输入以下命令：

```bash
sudo gem install -n /usr/local/bin cocoapods
```
- 设置置pod仓库

```bash
pod setup
```
- 在项目根目录运行安装命令。

```bash
pod install
```
执行完成后，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a392b7a3f81f23de4857927ed106eb6d.png)
