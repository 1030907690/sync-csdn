---
layout:					post
title:					"Ignoring ensurepip failure: pip 8.1.1 requires SSL/TLS"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 我的是Ubuntu18.04安装Python3.5.2执行 sudo make install最后提示`Ignoring ensurepip failure: pip 8.1.1 requires SSL/TLS`，pip没安好。
- 解决方案，安装ssl相关的:

```bash
apt-get install libssl-dev
apt-get install make build-essential libssl-dev zlib1g-dev libbz2-dev libsqlite3-dev
sudo apt-get install libssl1.0
```
- 如果是centos用:

```bash
yum install openssl-devel
```

- 最终能看到pip是安装好了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/59dcc7ba4577c6438100527857bb531e.png)
