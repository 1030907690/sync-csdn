---
layout:					post
title:					"把Jar包上传到GitHub仓库"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 想要把自己的Jar作为公共依赖，要使用的时候引入就可以了。但是上传到中央仓库还要先完成审核。自己又没有私服。这个时候我选择上传到GitHub仓库，先满足我基本的需求。

## 事先创建保存Jar包的仓库
- 事先创建好保存Jar包的仓库 ，如`maven-repository`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/05896cc11e03837bdf2e0e2d24118a28.png)


## 设置settings.xml文件
- 定位到`<servers>`标签下，增加如下代码。

```xml
  <server>
        <id>github</id>
          <username>GitHub帐号名</username>
          <password>GitHub token</password>
     </server>
```

- `token`在此处申请[https://github.com/settings/tokens](https://github.com/settings/tokens)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5e434a6c71c259ed99fb1de43bf5d6a4.png)
- 点击`Generate new token`，输入密码后进入。输入名称（Note），失效时间（Expiration），然后勾选`repo`和`user`，最后点击  Generate token。

- 然后就能得到`token`了， 注意保存下来，这个只显示一次。

## 修改项目的pom.xml
- 增加如下代码
> 下面代码中 `1030907690` 是我的帐户名，`maven-repository`是我事先在GitHub创建好的仓库。
```xml
 <properties>
		<java.version>1.8</java.version>
		<github.global.server>github</github.global.server>
</properties>
	
<build>

	<plugins>
		<!--该插件识别java代码 否则自己在Project Structure设置-->
		<plugin>
			<groupId>org.apache.maven.plugins</groupId>
			<artifactId>maven-compiler-plugin</artifactId>
			<version>3.7.0</version>
			<configuration>
				<source>${java.version}</source>
				<target>${java.version}</target>
				<encoding>UTF-8</encoding>
			</configuration>
		</plugin>
		<plugin>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-maven-plugin</artifactId>
		</plugin>

		<!-- 要将源码放上去，需要加入这个插件 -->
		<plugin>
			<artifactId>maven-source-plugin</artifactId>
			<version>3.0.0</version>
			<configuration>
				<attach>true</attach>
			</configuration>
			<executions>
				<execution>
					<phase>compile</phase>
					<goals>
						<goal>jar</goal>
					</goals>
				</execution>
			</executions>
		</plugin>

		<!--参考  https://www.jianshu.com/p/98a141701cc7-->
<!--Error creating blob: Git Repository is empty. (409)   仓库里随便创建下文件-->


		<plugin>
			<artifactId>maven-deploy-plugin</artifactId>
			<version>2.8.1</version>
			<configuration>
				<altDeploymentRepository>
					internal.repo::default::file://${project.build.directory}/maven-repository
				</altDeploymentRepository>
			</configuration>
		</plugin>


		<plugin>
			<groupId>com.github.github</groupId>
			<artifactId>site-maven-plugin</artifactId>
			<version>0.12</version>
			<configuration>
				<message>Maven artifacts for ${project.version}</message>
				<noJekyll>true</noJekyll>
				<outputDirectory>${project.build.directory}/maven-repository</outputDirectory><!--本地jar地址-->
				<branch>refs/heads/main</branch><!--分支-->
				<merge>true</merge>
				<includes>
					<include>**/*</include>
				</includes>
				<repositoryName>maven-repository</repositoryName><!--对应github上创建的仓库名称 name-->
				<repositoryOwner>1030907690</repositoryOwner><!--github 仓库所有者-->
			</configuration>
			<executions>
				<execution>
					<goals>
						<goal>site</goal>
					</goals>
					<phase>deploy</phase>
				</execution>
			</executions>
		</plugin>
	</plugins>
</build>
```


## 上传Jar
- 使用如下命令

```bash
 mvn clean package deploy
```
- 如果要忽略测试
```bash
 mvn clean package deploy -DskipTests
```

## 执行效果
- 上传完成后仓库里就有Jar包了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dd6bc200a53f3fdc3cefe1d274d41651.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3c27f7a2a61a418b873aed66f01a6932.png)


## 其他项目引入Jar
> 注意下`settings.xml`有没有配置`<mirrorOf>*</mirrorOf>`，如果有不会走自己的仓库，是拉不下来这种包的。

```xml
    <repositories>
        <repository>
            <id>maven-repository-main</id>
            <url>https://raw.github.com/帐户名/maven-repository/main/</url>
            <snapshots>
                <enabled>true</enabled>
                <updatePolicy>always</updatePolicy>
            </snapshots>
        </repository>

    </repositories>
   <dependencies>
      <dependency>
            <groupId>groupId</groupId>
            <artifactId>artifactId</artifactId>
            <version>版本号</version>
      </dependency>
  </dependencies>
```
## 源码和Jar包仓库地址
- 源码地址：[https://github.com/1030907690/spring-boot-kubernetes/tree/v1.0.1](https://github.com/1030907690/spring-boot-kubernetes/tree/v1.0.1)
- Jar包地址：[https://github.com/1030907690/maven-repository](https://github.com/1030907690/maven-repository)

## 遇到的问题
- Error creating blob: Git Repository is empty. (409)
> 解决方案： 在仓库里随便创建一个文件不要为空就行。
## 参考
- [https://www.jianshu.com/p/98a141701cc7](https://www.jianshu.com/p/98a141701cc7)




