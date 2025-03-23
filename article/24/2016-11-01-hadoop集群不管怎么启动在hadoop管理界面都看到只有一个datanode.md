---
layout:					post
title:					"hadoop集群不管怎么启动在hadoop管理界面都看到只有一个datanode"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
这是因为我以前单台机子使用过，在配置hadoop集群时，由于大多都是复制到每个节点上的，这就导致了datanode的VERSION里面有2个id是一模一样不能共存。datanodeUuid和storageID



只需要稍微修改下这2个id的值重新启动就可以了。



就这样就行了。

​