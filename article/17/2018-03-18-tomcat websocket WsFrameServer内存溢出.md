---
layout:					post
title:					"tomcat websocket WsFrameServer内存溢出"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- WebSocket连接上了300以后JVM就报内存溢出了，把JVM溢出的堆栈日志导了出来这是详情：

```
 648 instances of "org.apache.tomcat.websocket.server.WsFrameServer", loaded by "java.net.URLClassLoader @ 0x80f923a8" occupy 1,598,429,376 (96.40%) bytes. These instances are referenced from one instance of "java.util.concurrent.ConcurrentHashMap$Node[]", loaded by "<system class loader>"

Keywords
java.util.concurrent.ConcurrentHashMap$Node[]
org.apache.tomcat.websocket.server.WsFrameServer
java.net.URLClassLoader @ 0x80f923a8
```
![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318153852190%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-d930R2iD-1742104286665)

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318153902919%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-aCO4FX9q-1742104286667)

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318154006531%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-ExSZC075-1742104286667)

- 可以看到WsFrameServer里面有2个变量messageBufferText和messageBufferBinary占用内存比较大。那么来看下源码，一般项目不会导入tomcat的jar，所以如果在项目里找不到WsFrameServer就先导入tomcat的包。
![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318154552767%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-DetYFmby-1742104286667)

- WsFrameServer继承WsFrameBase ，messageBufferText和messageBufferBinary属性就在WsFrameBase里，然后我们来debug程序,看看是怎么设置的值。

- WsFrameServer里面会调用WsSession的构造方法有给messageBufferText和messageBufferBinary赋默认值2个都是8192大概是8K,然后再通过WsSession里面的get属性方法拿到这2个值。

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318155347530%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-kgHFCw6d-1742104286668)
![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318155404178%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-6HI3Ke8O-1742104286668)


- 然后走到了WsWebSocketContainer ， setDefaultMaxTextMessageBufferSize方法设置值，这里的值是819200大概是800K
![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318155651656%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-uT9MEjTo-1742104286668)

- 然后再走看是哪里调用的这个方法：
![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318155936141%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-AT4tK3W3-1742104286668)

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318155951166%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-F2rOFwQd-1742104286668)

- 设置messageBufferText和messageBufferBinary的地方就是ServletServerContainerFactoryBean,最后发现在spring的配置文件中配置了这2个值：
![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318160150486%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-2RJl9bOy-1742104286668)

- 把这个后面2个属性的值减少2个0，连接数明显增大了，也没报内存溢出了。
