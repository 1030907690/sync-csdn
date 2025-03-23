---
layout:					post
title:					"java导出excel中文不显示"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 文件名只有数字和字母等，中文不见了。
- 解决方案，编码。

```
response.setHeader("Content-disposition", "attachment; filename=" + URLEncoder.encode(fileName, "UTF-8"));
```
