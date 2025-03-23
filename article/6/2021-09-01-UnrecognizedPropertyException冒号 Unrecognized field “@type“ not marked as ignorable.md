---
layout:					post
title:					"UnrecognizedPropertyException: Unrecognized field “@type“ not marked as ignorable"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 问题背景：Redis里的数据取出来反序列成对象，报错 `com.fasterxml.jackson.databind.exc.UnrecognizedPropertyException: Unrecognized field "@type" (class com.xx.common.xx.xxx.xxx.LoginUser)`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/006d22248de1c768148313b8597e61cb.png)
- 有可能的原因
- 1、`@type`类型与本地对象类型不同，比如：`字符串 @type是com.xx.common.xx.xxx.xxx.LoginUser，但你本地对象是com.yy.common.xx.xxx.xxx.LoginUser`。
- 2、数据字段和本地对象对应相差太大。

- 解决方案，代码如下所示

```c
        String str = "{\"os\":\"Windows 10 or Windows Server 2016\",\"@type\":\"com.xx.common.xx.xx.xx.LoginUser\",..........}";
        ObjectMapper objectMapper = new ObjectMapper();
         //这句代码
        objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        LoginUser loginUser = objectMapper.readValue(str, LoginUser.class);
        System.out.println(loginUser);
```
