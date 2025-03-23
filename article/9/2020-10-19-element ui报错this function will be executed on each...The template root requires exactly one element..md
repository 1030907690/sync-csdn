---
layout:					post
title:					"element ui报错this function will be executed on each...The template root requires exactly one element."
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 报错信息如下所示。

```html
this function will be executed on each node when use filter method. if return 'false', tree node will be hidden.
[vue/no-multiple-template-root]
The template root requires exactly one element.
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7ac5d6869ebae38ae8476f7fbaee14e7.png#pic_center)
- 解决办法：在`<template>`标签下随便再加个标签，比如`<span>`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9af15072837dc9e867590b12f31a9a32.png#pic_center)

