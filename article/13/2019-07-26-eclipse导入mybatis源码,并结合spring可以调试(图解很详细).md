---
layout:					post
title:					"eclipse导入mybatis源码,并结合spring可以调试(图解很详细)"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
##### 一、用自己原来引入过mybatis的项目，主要下载这2个源码
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b75aa44184718883cec154c36c08ee50.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f9b22afb32543ae1caebba19c4fc7997.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/71644285b25146bd56f6fdb984b07d07.png)
- 在github下载对应的版本
Mybatis-spring下载地址: https://github.com/mybatis/spring (因为我这里用了spring所以要下mybatis对应spring的适配)
Mybatis源码下载地址:  https://github.com/mybatis/mybatis-3
注意:mybatis源码的版本和mybatis-spring里的mybatis版本对应
##### 二、下载之后两个都解压，导入eclipse(注意用maven方式导入)
- 导入后这2个项目要maven刷新下依赖，目录结构就会变成maven了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d7f39a264f9a95ac9e58283279587f15.png)
- 目录结构变成了maven
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/93237639321dfe7fe656d4a3bcde6486.png)
- 此时点击我项目的2个依赖会进入我本地源码的pom.xml，基本上就成功一半了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3c325fdec0693676e62674307bef8f5f.png)
##### 三、此时要注意的就是添加依赖
- 这2个依赖要有
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e10b3c78b746feb7e5b4412cdccc234e.png)
- 还有pom.xml必须要有ognl和javassist ，这里版本看你们自己选用了；缺少javassist 会报 Cannot enable lazy loading because Javassist is not available. Add Javassist to your classpath；缺少ognl会报找不到class
 

```
  		<!-- mybatis需要的 -->
      <dependency>
            <groupId>ognl</groupId>
            <artifactId>ognl</artifactId>
            <version>${ognl.version}</version>
        </dependency>
   		<!-- Cannot enable lazy loading because Javassist is not available. Add Javassist to your classpath. -->
        <dependency>
            <groupId>org.javassist</groupId>
            <artifactId>javassist</artifactId>
            <version>${javassist.version}</version>
        </dependency>
```

- 有时Deployment Assembly不会自动添加依赖需要我们自己Add：
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f8c211818a505c1970d7a73acb33b2c8.png)
后面的spring那些包，因为我是导入的源码才有;不是导入spring源码运行的不用管。

- 有时候maven刷新后，会变成低版本一些语法糖要报错，还需要改下编译的jdk版本:
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ec57c4170dbf5aa26432e86e0ab65b87.png)
还可以在pom.xml设置编译jdk版本，就不会出现这种问题了。

```
  <build>
        <plugins>
             <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>${maven-compiler-plugin.version}</version>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                    <encoding>UTF-8</encoding>       
                </configuration>
            </plugin>  
</plugins>
</build>
```
##### 四、最后一步就是检测是否生效，看一下是否走我们的源码了。查看下我们的配置文件找入口，然后我们debug一下就可以验证了。
- 这里有2个入口可以debug，SqlSessionFactoryBean是根据配置文件构建SqlSessionFactory的；MapperScannerConfigurer是扫描Mapper接口注入到spring容器的。
- MapperScannerConfigurer是实现BeanDefinitionRegistryPostProcessor接口所以这个初始化比SqlSessionFactoryBean要早一些。SqlSessionFactoryBean是在被初始化的时候调用afterPropertiesSet方法区构建SqlSessionFactory的。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/909bd02258029b106f3d759d8c463e50.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0ad1d5c490d58c54a6d3fc80db5c094e.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cb66964a76bf4215ad7ccd8f9c285605.png)

- 启动完成后做一下简单查询debug一下也是可以的。
- 查询单条数据调用mapper的时候一路会经过一个jdk动态代理判断执行的动作(增、删、改、查),然后给封装的SqlSessionTemplate,最后还是到DefaultSqlSession的selectOne方法。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9b91c2d253914a7a40a4ed8f03f6d531.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/eb33d3ac0d81d46d9fa414fb756f3786.png)
- 至此已经完成了，导入源码还是比较好debug一些,看源码效率相对高一些。如果本文章有误，请批评指正，感谢您的观看!

