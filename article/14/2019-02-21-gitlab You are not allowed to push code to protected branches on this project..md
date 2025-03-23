---
layout:					post
title:					"gitlab You are not allowed to push code to protected branches on this project."
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- gitlab You are not allowed to push code to protected branches on this project.提交是报这个是因为没有权限。
- 解决方案一：把帐号设置为admin管理员。
- 解决方法二: 到目标仓库 Settings -> Repository -> 展开Protected Branches ,**修改Allowed to merge   Allowed to push这两栏权限**(之前默认只有维护人员有权限，而我刚好赋予的是开发人员，所有没权限)，见下面图片。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4451660615ebaf1fd61f2aee2aff13e8.png)