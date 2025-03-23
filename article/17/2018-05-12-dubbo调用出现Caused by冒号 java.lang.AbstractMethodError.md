---
layout:					post
title:					"dubbo调用出现Caused by: java.lang.AbstractMethodError"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- dubbo消费者调用提供者出现：

```
java.lang.AbstractMethodError: com.xxx.xxx.service.impl.VersionManageServiceImpl.findVersionManageByPageCode(Ljava/lang/String;)Lcom/xxx/xxx/entity/VersionManage;
```
- 在网上搜了一大片，基本上都说是spring和mybatis插件的兼容问题，但是改了依然不见效果，于是好好的搜了一下这个异常。

```
这是调用抽象方法时抛出异常
可能这个方法(findVersionManageByPageCode)没有具体的实现
```

- 于是我查看源码和用**jd-gui**工具反编译class文件
![这是源码里的方法](https://i-blog.csdnimg.cn/blog_migrate/8d5b0cecf63bef6f10c1dd9e2cbf0031.png)
(这是源码里的方法,写在文件最后的)

![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/21f64857e7b661827062942f4be383a5.png)
(这是反编译后的源码，最后一个是findAllChannelPackage方法)

- 惊奇的发现并没有findVersionManageByPageCode方法。办法只能重新生成了class文件了。

- 我用的maven  ，我直接在项目路径下运行 **mvn clean** 清理了一下 ，重新运行就能正常调用了。
