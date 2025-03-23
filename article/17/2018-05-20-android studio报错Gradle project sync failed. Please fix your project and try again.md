---
layout:					post
title:					"android studio报错Gradle project sync failed. Please fix your project and try again"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---

- Android  Studio导入项目或者新建项目想运行的时候可能会报错**Gradle project sync failed. Please fix your project and try again**,原因应该是Gradle的一些东西没配好。

- 打开File - > Project Structure查看

![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/4baada2123c8f274b77175da018e5515.png)

- 这2个版本必须要保证本地有,而且一定要对得上。怎么知道本地有没有，下面2张图片展示他们各自的路径。

![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/3d1422518cc75e6b08a0b3d09ce73a33.png)
(默认路径在安装Android Studio路径下的gradle\m2repository\com\android\tools\build\gradle)


![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/c2a9612d5be736fb9737729ecd071399.png)
(windows默认路径在C:/Users/Administrator/.gradle/wrapper/dists)


- 如果dists下面的包如果下载不不来，就自己手动下载，下载路径就是当前项目下gradle\wrapper\gradle-wrapper.properties文件里面的distributionUrl属性的值。

- 最后同步一下
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/069db04b8fe34910b8c0a85d6358d65a.png)


- 现在就可以运行项目了。
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/5f47b674837a992bcb7504962cbecf04.png)
