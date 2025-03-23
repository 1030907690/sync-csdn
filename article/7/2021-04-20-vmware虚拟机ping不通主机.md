---
layout:					post
title:					"vmware虚拟机ping不通主机"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
### 现象
- vmware虚拟机ping不通主机，宿主机也ping不同虚拟机，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b3b5c92b89d59a327b8c36f1ce26af1a.png)
- 确认网络适配器都是正常的，我用的是`NET`模式，如下图所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e08bc1821c10ca07a06c9d6205470f7b.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9cfb7e4e9a951e59a56f5f5200beb9a6.png)

### 解决方案
- 使用关闭防火墙的方式（比较粗暴，临时解决问题吧），问题解决，如下图所示。
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a468cc475ee27d8d9f01f1cc233766c9.gif)

