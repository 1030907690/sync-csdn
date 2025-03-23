---
layout:					post
title:					"npm EACCES: permission denied"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 背景:在linux上安装好nodejs后,使用`npm install`命令安装项目相关依赖一直都报permission denied权限未定义的问题，我本身就是root用户了。

- 解决办法 ,需要这个命令。

```
npm install --unsafe-perm=true --allow-root
```