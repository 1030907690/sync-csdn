---
layout:					post
title:					"el-dialog中ref无效"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/75b7043c697fe6366dbb0bfbc6ff7b52.png)
- 从图中可以看出`el-dialog`中的组件是不会提前加载的。所以使用$refs会报错。

- 解决方案
	- 使用`$nextTick`
	

```js
 this.$nextTick(() => {
      console.log("ref ",  this.$refs.tagTitleRef);
    })
```
- 这样就能获取到了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4273bc517f9981844ff68bb04bbec539.png)

