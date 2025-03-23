---
layout:					post
title:					"使用SourceForge"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[toc](目录)
### SourceForge简介
- SourceForge是一套合作式软件开发管理系统。SourceForge本身是VA Software出售的专有软件。它集成了很多开源应用程序（例如PostgreSQL和SVN、CVS），为软件开发提供了整套生命周期服务。(摘自维基百科)
- SourceForge.net，又称SF.net，是开源软件的开发者进行开发管理的集中式场所，也是全球最大开源软件开发平台和仓库。SourceForge.net由VA Software提供主机，并运行SourceForge软件。大量开源项目在此落户（2005年6月已经达到125,090个项目及1,352,225位注册用户），包括维基百科使用的MediaWiki，但也包含很多停止开发和一人开发的项目。(摘自维基百科)
- 就我目前体验到的，简而言之SourceForge和github差不多也是个存储仓库，不过SourceForge是完全免费的，而且没有空间的限制。
### 用SourceForge可以做什么?
- 我只说说我目前用过的，SourceForge肯定不止这点功能
	- 文件存储
	- 构建网站

### 文件存储
- 注册一个帐号，点击右上角的`Create`创建一个仓库。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ea9a5ad59eeec10b1edb2acdd59d1321.png)
- 点击`Create Your Project Now`，`Import from GitHub` 我还没试过先不说。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/003169fdea53cebc978fd9ab497d0592.png)
- 名字自己定义，只要能过验证就行了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d8f1fe2838456715a3c5a57bab03f449.png)
- 然后就是选择接受协议，点击`Create`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/97840a024c72826fa4763ec6388dcc07.png)
- 加入这就是我刚刚创建好的仓库，现在就该上传文件试试了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8774a7c51ee060b2bffc87539bc337fd.png)
- SourceForge提供了很多中上传文件的方式(上传文件的文档 [https://sourceforge.net/p/forge/documentation/Release%20Files%20for%20Download/#scp](https://sourceforge.net/p/forge/documentation/Release%20Files%20for%20Download/#scp))
  - 网页上传
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fd00ecd068f0e13fb401535a70116f83.png)
 	- FTP
 	- scp
	 - rsync

 - 还可以用其他的工具，比如WinScp之类的。
 - 还有个要注意的是上传路径, `zhouzhongqing@frs.sourceforge.net:/home/frs/project/generic-software/`，`zhouzhongqing`是我的帐号名称`@frs.sourceforge.net:/home/frs/project/`是固定的，后面是自己仓库的名称。`/home/frs/project/generic-software/`这样表示直接上传到`generic-software/`存储库根目录下。

```bash
scp file.zip zhouzhongqing@frs.sourceforge.net:/home/frs/project/generic-software/
```

### 构建网站
- 文档 [https://sourceforge.net/p/forge/documentation/Project%20Web%20Services/](https://sourceforge.net/p/forge/documentation/Project%20Web%20Services/)
- 构建网站与什么的有一点不一样，我在创建仓库时是把全部都勾上的，有备无患。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7e382eb8202ad021c484df41a1fda0be.png)
- 先来看看SourceForge部署环境  [https://sourceforge.net/p/forge/documentation/Project%20Web%20Services/](https://sourceforge.net/p/forge/documentation/Project%20Web%20Services/)
- 现在的环境应该是Apache2.4.x和php7.1
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/53a309c923aaa76be27c328362704ff3.png)
- 这环境对一般的php程序运行是没问题的，比如建个博客网站`wordpress`之类的；但是要做一些骚气的操作就难了，比如采集数据，因为我发现它无法访问外网。
- 下面就说下建站比较重要的数据库
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/93ba692a86a39e2871e79d216dc33efa.png)
- 下面就是设置密码；有3个账号，不同的权限  管理数据库的url	https://mysql-w.sourceforge.net
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d9e9bf8fef1980f8cd4f7aabc4a911d6.png)
- 管理数据库的界面
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6473b2d9ae7e5394447155992f282dfe.png)
- 项目配置
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ce0c830d151844a01f2b6877c0557d3d.png)
- 记住这个`Homepage`的值，这就是SourceForge分配给我们的域名
- 上传源代码,我依然用scp上传演示，我以建好的`wparticle`项目为例；把我的代码放在`/home/project-web/wparticle/htdocs/`目录下。

```bash
scp -r   xxxx   zhouzhongqing@web.sourceforge.net/home/project-web/wparticle/htdocs/
```
- 初始化的时候数据库host填`mysql-w`就可以了，有可能你的不一样，具体看SourceForge的管理界面。
- 还记得上面的域名吗？使用上面的域名访问试试。
- 要搭建网站又不得不说权限这个问题，有的网站要目录的全部权限;用用chmod之类的命令；所以这又不得不插播一下SourceForge的`Shell Service`
	- 文档 [https://sourceforge.net/p/forge/documentation/Shell%20Service/](https://sourceforge.net/p/forge/documentation/Shell%20Service/)
	- 命令`ssh -t  zhouzhongqing@shell.sourceforge.net create`    ；`zhouzhongqing`是我的用户名
	![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b65a0ebdf2b4e1437af297d346f6f99c.png)
- 一通配置之后基本上就可以用了，我在SourceForge上建了个博客
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/47a9f0df111221e9b284400e1aca65fe.png)

### SourceForge目录总结
- `/home/pfs/project/xxxx` 这是项目文件存储目录(一般大文件放这儿)比如我的`generic-software`是`/home/pfs/project/generic-software`
- `/home/project-web/xxxx/htdocs/` 这是项目存放网站的地方，比如我的`wparticle`项目 ；路径为`/home/project-web/wparticle/htdocs/`
- 本文简单的讲述了下SourceForge的使用，"白嫖真香警告";感谢您的观看，如果文字有描述不当之处，欢迎您批评指出。