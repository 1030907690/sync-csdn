---
layout:					post
title:					"nuxt-link跳转到当前页面，不同query参数值不加载"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 例如地址是这样的`http://localhost:81/xxx`，现在加上参数`http://localhost:81/?act=0`。默认情况下是不会加载的。
## 解决方案
- 使用`watchQuery`。文档地址：[https://nuxtjs.org/docs/components-glossary/watchquery](https://nuxtjs.org/docs/components-glossary/watchquery)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/45979b7c95e97390dc84f1aaa36be88f.png)
- 修改后代码如下：

```js
 ... 省略...
 watchQuery: ["act"],
async asyncData({ $axios, query }) {
    let act = query.act 
    console.log("act ",act);
    return {selectedIndex:act ? act : 0}
  },
  ... 省略...
```

- 这样每次切换就有效果了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dab4a132f2d126da31947b623658f663.png)

## 参考
- [https://blog.51cto.com/u_15351691/3732466](https://blog.51cto.com/u_15351691/3732466)