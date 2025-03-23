---
layout:					post
title:					"RestTemplate乱码和No HttpMessageConverter for java.util.HashMap and content type “application/json"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 乱码问题如下所示
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3333c687b3f05b3e6c9d2580342824ad.png)
- 解决方案，设置转换器
```c
private StringHttpMessageConverter m = new StringHttpMessageConverter(Charset.forName("UTF-8"));
private RestTemplate restTemplate = new RestTemplateBuilder().additionalMessageConverters(m).build();
```

- 如果要传递`json`数据可能遇到`No HttpMessageConverter for java.util.HashMap and content type "application/json`
- 需要再改下`RestTemplate`对象。

```c
    private StringHttpMessageConverter m = new StringHttpMessageConverter(Charset.forName("UTF-8"));
    private RestTemplate restTemplate = new RestTemplateBuilder().additionalMessageConverters(m).additionalMessageConverters(new MappingJackson2HttpMessageConverter()).build();
```
- 修改后成功，如下图所示
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a036f04083d3175772fbcb0fd0c61979.png)
