---
layout:					post
title:					"eclipse和idea导入tomcat源码"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
### 下载源码
- 不管是用什么工具导入源码，这第一步肯定是去下载源码了。下载地址[https://archive.apache.org/dist/tomcat/](https://archive.apache.org/dist/tomcat/)，因为工作中用的是tomcat8.5.20我就下他了[https://archive.apache.org/dist/tomcat/tomcat-8/v8.5.20/src/apache-tomcat-8.5.20-src.zip](https://archive.apache.org/dist/tomcat/tomcat-8/v8.5.20/src/apache-tomcat-8.5.20-src.zip)

###  eclipse导入并运行
####  建立一个空的maven项目
#### 复制源码到项目
- 到这个把源码复制到项目里
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f0bee378eb3d66aba3c1e312bd925331.png)
- 把conf复制到resources下
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2156236a64d5517c38eef9158c22c147.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9babe57458ead27086b3fef0ee580cb3.png)
- 可能需要的依赖

 

```java
<!-- https://mvnrepository.com/artifact/org.apache.ant/ant -->
<dependency>
    <groupId>org.apache.ant</groupId>
    <artifactId>ant</artifactId>
    <version>1.8.2</version>
</dependency>
 <!-- https://mvnrepository.com/artifact/org.eclipse.jdt/org.eclipse.jdt.core -->
  <dependency>
    <groupId>org.eclipse.jdt</groupId>
    <artifactId>org.eclipse.jdt.core</artifactId>
    <version>3.13.102</version>
</dependency> 
 
 <!-- https://mvnrepository.com/artifact/javax.xml.rpc/javax.xml.rpc-api -->
<dependency>
    <groupId>javax.xml.rpc</groupId>
    <artifactId>javax.xml.rpc-api</artifactId>
    <version>1.1.2</version>
</dependency>
 
<!-- https://mvnrepository.com/artifact/org.eclipse.birt.runtime.3_7_1/javax.wsdl -->
<dependency>
    <groupId>org.eclipse.birt.runtime.3_7_1</groupId>
    <artifactId>javax.wsdl</artifactId>
    <version>1.5.1</version>
</dependency>
```

#### 运行测试

- 可以运行一个项目试试看，在webapps放一个项目就好
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c83c871728e1be5c2fd31e641ac7ba1f.png)
- 找到Bootstrap运行
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6adcd26086e08b7c98a6e7bdd4d63bf2.png)
- 启动成功，测试一波
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ceadcf69d8378febf3d5499c77008e6f.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/44bb45c812426a5f317d1f1b34c10864.png)
- 运行成功,eclipse导入源码算是完成了。

### idea导入源码并运行
#### 建立一个空maven项目

#### 复制代码到项目里
- 依旧是把代码还有配置文件以及拿个测试项目复制到里面
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/18504898be32738dd29ae81540c084bb.png)
- 可能需要的依赖

```java
     <!-- https://mvnrepository.com/artifact/org.apache.ant/ant -->
        <dependency>
            <groupId>org.apache.ant</groupId>
            <artifactId>ant</artifactId>
            <version>1.8.2</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/org.eclipse.jdt/org.eclipse.jdt.core -->
        <dependency>
            <groupId>org.eclipse.jdt</groupId>
            <artifactId>org.eclipse.jdt.core</artifactId>
            <version>3.13.102</version>
        </dependency>

        <!-- https://mvnrepository.com/artifact/javax.xml.rpc/javax.xml.rpc-api -->
        <dependency>
            <groupId>javax.xml.rpc</groupId>
            <artifactId>javax.xml.rpc-api</artifactId>
            <version>1.1.2</version>
        </dependency>

        <!-- https://mvnrepository.com/artifact/org.eclipse.birt.runtime.3_7_1/javax.wsdl -->
        <dependency>
            <groupId>org.eclipse.birt.runtime.3_7_1</groupId>
            <artifactId>javax.wsdl</artifactId>
            <version>1.5.1</version>
        </dependency>
```
- 这里有个坑,必须的build配置(不然不会编译到classes )

```java
 <build>
          ......... 省略.............
        <resources>
 

            <!-- 因为src/main/java里的xml，properties,dtd没编译到classes 所以这样配置 -->
            <resource>
                <directory>src/main/java</directory>
                <includes>
                    <include>**/*.xml</include>
                    <include>**/*.properties</include>
                    <include>**/*.dtd</include>
                </includes>
            </resource>
        </resources>
    ......... 省略.............
    </build>
```
#### 运行测试 
- 依旧运行Bootstrap启动
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fde5c7c52db17f648f64467312412da8.png)
- 然后访问项目
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/822f495610f7aafd68351d88e6292bcc.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f125857d11b5a75a372cf66640e6a829.png)
- 测试成功，idea导入源码就完了


### 已经调试过的源码
- 我把idea导入过的tomcat8.5.20的源码分享给大家,写了一些源码注释 [https://github.com/1030907690/apache-tomcat-8.5.20-src](https://github.com/1030907690/apache-tomcat-8.5.20-src),如果要运行可以把那个测试项目换成自己的，因为那个测试项目启动要查询数据库;没有那条数据要报错的。
- 最后如果文章有问题的地方还希望大家留言斧正。
