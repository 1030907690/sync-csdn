---
layout:					post
title:					"Linux安装下载神器axel"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[toc](目录)
## Ubuntu安装
- Ubuntu安装比较简单
```
apt install axel
```

## centos安装
- 我们可以先用yum install axel尝试下看能不能安装上，如果不能再尝试下面的方案。
- 到这个网站[https://pkgs.org/](https://pkgs.org/)搜索`axel`
- 可能搜索后还要输入验证码，之后到达这个页面
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/93c3e229c1cb30ba8f16500659db476d.png)
- 选择自己需要的版本点击进去
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9423469d1c53d52db226dbff0cd60f7d.png)
- 一般选择官方的
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5175867d00d1760c22fb3d3ae983c4ea.png)
- 下载下来用`rpm -ivh` 安装就可以了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0d228bc93f1bc1e4870ac937282a61ee.png)

## 其他安装方式（通用）
- 到网站下载release包，地址[https://github.com/axel-download-accelerator/axel](https://github.com/axel-download-accelerator/axel)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/77d1979d402c335c034d9198ecb9e731.png)
- 然后解压，到解压目录里，执行以下命令。

```
./configure && make && make install
```
- 执行完成后的结果
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/be98ed01b5c35163e6cc037216f8507a.png)
