---
layout:					post
title:					"ubuntu wine"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
### 安装wine（推荐）
- 首先确定自己32位还是64位系统 `lscpu`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c7bd0ca96d2a91b494bf22d9c7b25185.png)
- 32位

```
 sudo apt install wine32
```
- 64位

```
 sudo apt install wine64
```
- 检测是否安装完成

```
 wine --version
```
### 替代方案 WineHQ
- 在安装64位版本的Wine之前，在终端中运行以下命令以添加i386体系结构

```
sudo dpkg --add-architecture i386 
```
- 下载并添加存储库密钥
```
wget -nc https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key
```
- 添加仓库(我自己安装的时候发现了用`Ubuntu 16.04 Linux Mint 18.x`这个版本的命令才能安装上，我的是ubuntu 18.04，不知道是不是和我安装系统时选择最小安装有关)

|版本 | 使用命令|
|--- |--- |
|Ubuntu 19.10 |sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ eoan main' |
| Ubuntu 18.04 Linux Mint 19.x | sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ bionic main' |
|Ubuntu 16.04 Linux Mint 18.x|sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ xenial main'|

- 更新包

```
sudo apt update
```
- 安装包(任选一个)
- 稳定版本  `sudo apt install --install-recommends winehq-stable`
- 开发版本 `sudo apt install --install-recommends winehq-devel`
- Staging `sudo apt install --install-recommends winehq-staging`
