---
layout:					post
title:					"whistle ERR_CERT_AUTHORITY_INVALID"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 我是做企业微信侧边栏，因为要改bug，方便调试，所以想把请求导到我本地来。
- 事先设置了代理，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4fbf48ec9653e48ed6b4d944a1270c48.png)

- 使用了`whistle` 。`ctrl+shift+alt+d`打开debug后，查看到发起请求被中断了，console报了`ERR_CERT_AUTHORITY_INVALID`。

- 中间还有个小插曲，我电脑还有`mitmproxy`,使用它却没有问题，能看到请求。
- 推断就是证书问题。
## 解决方案
- 安装证书时不要用自动那个选项。
- 选择`Trusted Root Certificate Authorities`(受信任的根证书颁发机构)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/da888b55644f8cfa7b6b1cc154731d00.png)
- 使用命令`certmgr.msc`查看证书
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a1f1bd4174a22b2f01c153c2daa07d3e.png)
- 请求效果,如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e289b80a4dbb3a4c0835ef21fc60b93b.png)
- 请求已经到本地了（现在配置了`Rules`），如下图所示
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/874c8ba2eb3af2c3b47135c777c5a839.png)

## 后续对比思考
- 我对比了下证书，`whistle`自动安装在`Intermediate Certificate`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1b23464b41c3cdd599847d42ad47ec5c.png)
- `mitmproxy`自动安装在`Trusted Root Certificate Authorities`(受信任的根证书颁发机构)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0d440137a7d0e9415461a602ac5702d4.png)
- 大概是`Intermediate Certificate`级别不够吧，所以会被中断。



## 参考
- [https://github.com/avwo/whistle/issues/52](https://github.com/avwo/whistle/issues/52)
- [https://wproxy.org/whistle/webui/https.html](https://wproxy.org/whistle/webui/https.html)
