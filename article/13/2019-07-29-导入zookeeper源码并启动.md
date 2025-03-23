---
layout:					post
title:					"导入zookeeper源码并启动"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 为了更好的阅读源码,所以还是导入源码去debug比较方便；高版本的代码没什么好说的，是maven项目导入还是很方便的;我这里用的是低版本zookeeper3.4.5。我这里把它改成了maven项目。
##### 一、导入源码
- 低版本的源码本身不是maven项目,不过可以自己改。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cba2576d8e0d63296cd8ce6ad5f2ac4c.png)
- 先建一个空的maven项目,然后拷贝源码和依赖的lib
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/96e28e6ceb6a00b8f005dd687e4c09b5.png)
- 然后就是pom.xml添加依赖

```
<dependencies>
      

        <dependency>
            <groupId>io.netty</groupId>
            <artifactId>netty-all</artifactId>
            <version>3.2.2.Final</version>
            <scope>system</scope>
            <systemPath>${basedir}/dependencies/netty-3.2.2.Final.jar</systemPath>
        </dependency>

        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.8.1</version>
            <scope>system</scope>
            <systemPath>${basedir}/dependencies/junit-4.8.1.jar</systemPath>
        </dependency>


        <dependency>
            <groupId>com.puppycrawl.tools</groupId>
            <artifactId>checkstyle</artifactId>
            <version>5.0</version>
            <scope>system</scope>
            <systemPath>${basedir}/dependencies/checkstyle-5.0.jar</systemPath>
        </dependency>

        <dependency>
            <groupId>jline</groupId>
            <artifactId>jline</artifactId>
            <version>0.9.94</version>
            <scope>system</scope>
            <systemPath>${basedir}/dependencies/jline-0.9.94.jar</systemPath>
        </dependency>

        <dependency>
            <groupId>log4j</groupId>
            <artifactId>log4j</artifactId>
            <version>1.2.15</version>
            <scope>system</scope>
            <systemPath>${basedir}/dependencies/log4j-1.2.15.jar</systemPath>
        </dependency>

        <dependency>
            <groupId>org.mockito</groupId>
            <artifactId>mockito-all</artifactId>
            <version>1.8.2</version>
            <scope>system</scope>
            <systemPath>${basedir}/dependencies/mockito-all-1.8.2.jar</systemPath>
        </dependency>

        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>1.6.1</version>
            <scope>system</scope>
            <systemPath>${basedir}/dependencies/slf4j-api-1.6.1.jar</systemPath>
        </dependency>

        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-log4j12</artifactId>
            <version>1.6.1</version>
            <scope>system</scope>
            <systemPath>${basedir}/dependencies/slf4j-log4j12-1.6.1.jar</systemPath>
        </dependency>

</dependencies>
```

- 点击重新导入maven依赖
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ccfd5e2a4814bd6696a183e478ff7cdc.png)

##### 二、运行源码
- 增加配置文件zoo.cfg,这个复制下zoo_sample.cfg文件，增加dataDir配置即可。
- 启动类是QuorumPeerMain.java,如果此时直接运行main方法会运行失败找不到配置。

```
 log4j:WARN No appenders could be found for logger (org.apache.zookeeper.server.DatadirCleanupManager).
log4j:WARN Please initialize the log4j system properly.
Usage: ZooKeeperServerMain configfile | port datadir [ticktime] [maxcnxns]
```
所以我在代码里加了zoo.cfg和log4j.properties的位置:

```
//为了方便debug 增加cfg路径 2019年5月6日11:47:08
if (args.length < 1) {

    String configPathPrefix = QuorumPeerMain.class.getResource("/").getPath().replace("/target/classes/","/conf/");

    args = new String[1];
    args[0] = configPathPrefix + "zoo.cfg";

    //自定义log4j.properties的加载位置 2019年5月6日11:58:07
    PropertyConfigurator.configure(configPathPrefix + "log4j.properties");

}
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0408b69cb911199581157b7101a5107c.png)

- 现在是启动成功的了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/53d3703962000e134e82bc4f28570c41.png) 