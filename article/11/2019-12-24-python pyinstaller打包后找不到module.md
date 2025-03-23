---
layout:					post
title:					"python pyinstaller打包后找不到module"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- python pyinstaller打包后找不到module,情况如下:
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4fb3b54a59ba868ced93075dd53640ac.png)
- 解决办法:
	- 可能是环境因素，找不到module，打包加上`-p`指定依赖路径就可以了：
 

	```bash
	 /usr/local/python3.5/bin/pyinstaller -F  ssr_update.py  -p /usr/local/python3.5/site-packages
	```

	- 执行成功
	![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4b2c61fd1d6f015dbe4909df6bd98edc.png)
