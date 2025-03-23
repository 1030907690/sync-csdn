---
layout:					post
title:					"spring boot mybatis增加sql日志"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 没有sql日志，不好找问题，增加打印sql日志的yml配置如下：
	- com.xxx.wx.dao是自己的包路径。也就是mapper、xml的路径。

```
logging:
  level:
    com:
      xxx:
        wx:
          dao: debug
```
- 如果是properties文件则是：

```
logging.level.com.xxx.wx.dao=debug
```

- 配置后效果如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3b797d5d3d786aa41e49a9fda138308b.png)


- 并且路径可以配置多个，例如。
```
logging:
  level:
    com:
      xxx:
        wx:
          dao: debug
          daob: debug
```

