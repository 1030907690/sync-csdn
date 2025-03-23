---
layout:					post
title:					"eclipse中git pull拉取报错Checkout conflict with files"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
### 今天在eclipse pull同步代码时git报错大致是Checkout conflict with files

### 解决办法也很简单，<font color="red">强烈建议先将自己的代码备份一下再操作，以免自己未提交的代码被覆盖</font>(感谢[DJ_coder](https://me.csdn.net/DJ_coder)的评论)  ：
	Checkout conflict with files:后面会提示你哪些文件冲突解决办法就是找到冲突的文件, 右击 team -> advanced -> assume unchanged问题解决 再去 team -> Pull 

![图片](https://i-blog.csdnimg.cn/blog_migrate/5722fd4847b2298bd0f9c3d66366d837.png)