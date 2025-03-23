---
layout:					post
title:					"eclipse git报错git The current branch is not configured for pull No value for key branch.master.merge"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- **eclipse中使用git提交或者pull报错：**

```
git  The current branch is not configured for pull No value for key branch.master.merge found in configur
```

- **解决办法：**
修改你本地仓库的配置文件.git/config文件内容
```
[core]
	repositoryformatversion = 0
	filemode = false
	logallrefupdates = true
[branch "master"] 
	remote = origin 
	merge = refs/heads/master 
[remote "origin"] 
	url = https://gitee.com/apple_1030907690/CeShi2.git
	fetch = +refs/heads/*:refs/remotes/origin/*
```

这里的**url = https://gitee.com/apple_1030907690/CeShi2.git地址是你的仓库地址**。