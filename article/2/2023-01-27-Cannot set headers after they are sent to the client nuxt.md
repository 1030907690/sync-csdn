---
layout:					post
title:					"Cannot set headers after they are sent to the client nuxt"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 使用axios在created时请求2个接口，代码如下。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9245afc142e413b0691bd70abf674669.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/086fc44239aeeaa647afc7cbf1a94c61.png)

- 然后报错如下：
```js

 ERROR  Cannot set headers after they are sent to the client                                                                                                                                                                       14:54:29  

  at new NodeError (node:internal/errors:372:5)
  at ServerResponse.setHeader (node:_http_outgoing:576:11)
  at Storage.setCookie (server.js:3323:20)
  at Storage.setUniversal (server.js:3175:10)
  at Storage.syncUniversal (server.js:3202:12)
  at Token._syncToken (server.js:4046:26)
  at Token.sync (server.js:3998:24)
  at LocalScheme.check (server.js:4175:30)
  at server.js:3934:87
  at runMicrotasks (<anonymous>)
  at processTicksAndRejections (node:internal/process/task_queues:96:5)
```

## 解决方案
- 我查找资料说是发送了多次请求的问题。
- 然后我在created代码块测试。
```js
  created() {
    // this.initDate();
    let random = Math.floor(Math.random()*10+1)
    console.log("调用了created ",random);
  },
```
- 果然调用了2次。有一次是nuxt调用的。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3c16ffe547b31536fa785b63f0520ff2.png)

### 方案一
- 后面我改在`mounted`执行了。	

```bash
  mounted() {
    console.log("调用了mounted");
    this.initDate();
    
  },
```


### 方案二
- 判断是否在客户端

```js
created() {

    if (process.client) {
      let random = Math.floor(Math.random()*10+1)
      console.log("调用了created ",random);
      // handle client side
      this.initDate();
    }
  },
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f75ff4b3c516faba06ecd198b2108273.png)


