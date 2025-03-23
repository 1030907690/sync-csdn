---
layout:					post
title:					"nuxt创建项目失败，Error: Failed to download template from registry: Failed to download https://raw.githubus"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
## 报错详情
>Error: Failed to download template from registry: Failed to download https://raw.githubusercontent.com/nuxt/starter/templates/templates/v3.json: TypeError: fetch failed


![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/547f5247c444b4c87899cf31f4a883a3.png)


## 解决方案

- 去这个网站 [https://www.ipaddress.com/ip-lookup](https://www.ipaddress.com/ip-lookup) 查询ip

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/47a928ecb87d4b32d075302141faab73.png)
- 然后根据结果改hosts（路径是 C:\Windows\System32\drivers\etc\hosts）
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6f419069ee3f48315bb5f32246bc7d9f.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/52c29e34021051d7f5dc7f8645bb25d2.png)
- 重新打开cmd窗口就能通过了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7ab76700cb9f7306ddc147ab180f9e5c.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3e1a015b688eee5f48a59dc1bd7f276c.png)
