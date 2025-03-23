---
layout:					post
title:					"mysql create database xx-xxx异常You have an error in your SQL syntax"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 语句`create database test-admin;`报具体异常就是说语法不正确:

```
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '-admin' at line 1
```
- 明显的-(横杠)前面的没有了，应该是被认为是什么特殊字符了。
- 解决办法：
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f9b72135bdff02bcd5a96b13e31ccdf3.png)
- 主要database名称两边有`,就是按esc下面那个键。
