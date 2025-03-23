---
layout:					post
title:					"the volume for a file has been externally altered so that the opened file is no longer valid"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 今天我在把python程序打包成exe的时候出现了这个问题。
```
the volume for a file has been externally altered so that the opened file is no longer valid
```
- 开始我以为是`pyinstaller`的问题。关于这个错误网上的解决方案很杂，后面发现右下角的提示。
- 所以出现这个问题极有可能`被安全软件阻止`了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ac36a6b8cc65d78e32b11777917be949.png)
- 加入`信任`后就能打开了，如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a7359364de34b9e7add6ddce4741748e.png)
