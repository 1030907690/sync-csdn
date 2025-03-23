---
layout:					post
title:					"小心pointer-events: none；"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
 
- 我发现点击事件不生效。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/423d566990bbd9bd9fa7db78ec583345.png)
一开始我以为是swiper的问题，后面发现是css属性`pointer-events: none;`阻止了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/805a1c809bbd8e1089e54e96a9a9c2a9.png)

- 去掉后就可以点击了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a73b336bdc3401b6c429616dcf5241bd.png)
