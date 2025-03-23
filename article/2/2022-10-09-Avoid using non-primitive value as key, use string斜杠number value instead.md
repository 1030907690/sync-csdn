---
layout:					post
title:					"Avoid using non-primitive value as key, use string/number value instead"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 我的代码和数据是这样的。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9210982c4c0b710a532415a9fe58541b.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/590d4f78250de0e743022bdada8ed251.png)
- 因为我的`tag是一个对象`，所以会警告。
- 包`:key的值改为数字或字符串`类型就没问题了。
