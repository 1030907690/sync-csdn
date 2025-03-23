---
layout:					post
title:					"Set iterator.remove()； 无效"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
## 问题背景
- 使用的是`HashSet`，对象用了lombok的`@Data`注解，这里面重写过`hashCode`和`equals`。
- 来看现象，首先看我这里有2条数据。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5843e3ff7f1197f23a0821f8d262099b.png)
- 然后经历删除方法。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5fbf8b13677d17ae3a39da612a0513d6.png)
- 最后结果还是有2条数据。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1bd973a817e14bf5c502d9f77bba28b8.png)
## 问题分析
- 	注意我这里有个`骚操作`，中途有修改对象的属性。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6ae6dac0777f861062a98b74d880885a.png)
- 大概跟`hashCode`和`equals`有关，`iterator.remove()`没有定位到对象。
- 我注释掉修改那2段代码，结果就可以了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7c070c3660b9e1f4ee9ea91bf56c8488.png)
- 另外测试了下同样的骚操作，用List(ArrayList)是没问题的。
