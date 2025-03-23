---
layout:					post
title:					"django Django解决中文显示\u5...."
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
### 解决方案
- 解决中文乱码，代码如下所示。
```java
return JsonResponse(data=res, json_dumps_params={'ensure_ascii': False}) 
```
