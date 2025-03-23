---
layout:					post
title:					"新建的分支 has no tracked branch"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 新创建的分支出现x.x.x has no tracked branch，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1965d92e4bf347fd69db1c3b6ab9f4b1.png)
- 解决方案：设置追踪分支。
- 输入如下命令（`v1.0.3是我自己的分支，按自己的情况替换下`）

```
git branch --set-upstream-to origin/v1.0.3
或者
git branch --set-upstream-to=origin/v1.0.3
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4b5aeb78f4630e59f3686c88f154d3fa.png)
- 设置完成后，更新成功，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cf9229874d69519272680024645cac3a.png)
