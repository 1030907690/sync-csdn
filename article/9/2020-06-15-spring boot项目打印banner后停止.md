---
layout:					post
title:					"spring boot项目打印banner后停止"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 刚拿到的公司项目，运行之后打印了`Banner`之后阻塞一段时间后，就程序退出了。

```java
 .......省略...........

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::        (v2.0.2.RELEASE)

Disconnected from the target VM, address: '127.0.0.1:64550', transport: 'socket'

Process finished with exit code 0
```

- 解决过程：
- 我在`spring boot`整个启动过程的方法debug，在`SpringApplication#run`方法，`F8`断点调试
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/05e7b5de66e72be1593aadad7af88ac1.png)
- 然后我发现是卡在`refreshContext(context);`这段，最后发现进入了异常
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/117e911a7cc01339b3de24d2a905b55a.png)
- 现在异常找到了就好对症下药了，由于篇幅可能太长，我把`Unable to start embedded Tomcat`异常解决方案具体步骤单独写了篇文章:[遇到Unable to start embedded Tomcat或者自动停止如何查看具体报错信息](https://sample.blog.csdn.net/article/details/106764592)
- 如果还有问题,依然是自动停止的情况，建议在`AbstractApplicationContext#refresh`打断点，看具体是什么异常；
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f9e828e76db6dd3fea427cf6c35b25a7.png)
