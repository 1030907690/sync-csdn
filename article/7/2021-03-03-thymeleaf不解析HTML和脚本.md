---
layout:					post
title:					"thymeleaf不解析HTML和脚本"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 问题背景：后端返回了脚本，正常来说应该跳转到百度的，但是页面上只是当成字符串打印出来了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/69fdf39739446fde52b3e350ff1fb774.png)
- 解决方案：以前用的是`th:text`,现在使用`th:utext`属性，代码如下所示。

```
<span th:utext="${redirectObject.action}"></span>
```
