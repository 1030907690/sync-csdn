---
layout:					post
title:					"found for response type [class [B] and content type [image/jpeg]"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- RestTemplate报错`found for response type [class [B] and content type [image/jpeg]`。
- 解决方案：增加消息转换器。

```c
// 常用的2个StringHttpMessageConverter、MappingJackson2HttpMessageConverter
StringHttpMessageConverter m = new StringHttpMessageConverter(Charset.forName("UTF-8"));
RestTemplate restTemplate = new RestTemplateBuilder().additionalMessageConverters(m).additionalMessageConverters(new MappingJackson2HttpMessageConverter()).build();
// 重点是要增加这个
restTemplate.getMessageConverters().add(new ByteArrayHttpMessageConverter());
```
