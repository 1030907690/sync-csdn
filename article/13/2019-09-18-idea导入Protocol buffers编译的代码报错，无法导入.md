---
layout:					post
title:					"idea导入Protocol buffers编译的代码报错，无法导入"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 原因是Protocol buffers协议多了以后后整个项目比较大，超过了idea的限制了，调节下配置就可以了。
- 找到idea安装目录`bin/idea.properties`文件

```
 idea.max.intellisense.filesize=92500 #默认2500
```
