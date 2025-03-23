---
layout:					post
title:					"deploy发布的jar包中文乱码"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
### 背景
- 使用`mvn clean package deploy -DskipTests`发布的jar包。
- 源码显示正常
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/db03e6cdc0f42a8d435800d07ac6d300.png)
- 打包时出现Using platform encoding (GBK actually) to copy filtered resources, i.e. build is platform dependent!
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/301c3a4451a14f088aaaef2abbf3797d.png)
 - HTTP调用返回异常
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/11f4e08537de2f64e2bb78088e226b8a.png)
### 解决方案
- pom.xml加入`<encoding>utf-8</encoding>` 

```
  <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.0</version>
                <configuration>
                    <encoding>utf-8</encoding> 
                    <source>1.8</source>
                    <target>1.8</target>
                </configuration>
            </plugin>
```

- 重新发布调用返回正常，如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/04b0670b78dbde6c8c2a1df0f9d4706d.png)
