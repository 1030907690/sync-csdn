---
layout:					post
title:					"spring boot maven 多环境打包切换"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
#### 一、背景
- 在实际开发中一般都有多套环境,比如本地开发环境、测试环境、正式环境等等。他们有可能就是数据库连接地址，帐号，密码这些配置不同，所以打包到正式服的时候就要去改文件,这就很麻烦,有的时候可能忘记改,就打包到正式服引起一些程序异常。下面就来了解一些spring boot加maven 多环境打包,解决这个问题。

#### 二、配置
- pom文件

```
 <profiles>
        <!-- 本地开发环境 -->
        <profile>
            <id>dev</id>
            <properties>
                <spring.profiles.active>dev</spring.profiles.active>
            </properties>
            <activation>
            <!--默认-->
                <activeByDefault>true</activeByDefault>
            </activation>
        </profile>
        <!-- 生产环境 -->
        <profile>
            <id>prod</id>
            <properties>
                <spring.profiles.active>prod</spring.profiles.active>
            </properties>
        </profile>
    
    </profiles>

<build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>


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
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>${maven-surefire-plugin.version}</version>
                <configuration>
		<!--跳过测试-->
                    <skip>true</skip>
                </configuration>
            </plugin>
 		 <!-- 解决资源文件的编码问题 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-resources-plugin</artifactId>
                <version>${maven-resources-plugin.version}</version>
                <configuration>
                    <encoding>UTF-8</encoding>
                </configuration>
            </plugin>


</plugins>


   <!-- 2023年7月13日 更新 增加  打包过滤 就不会报@spring.profiles.active@问题了 -->
        <resources>
            <resource>
                <directory>src/main/resources</directory>
                <filtering>true</filtering>
                <!-- 这是排除文件-->
                <excludes>
                    <exclude>rebel.xml</exclude>
                    <exclude>assembly.xml</exclude>
                    <exclude>generatorConfig.xml</exclude>
                </excludes>
            </resource>
        </resources>


</build>
```

- application.yml文件

```
spring:
  profiles:
    active: @spring.profiles.active@
```
- `@spring.profiles.active@`使用的正式`<profiles>`的配置，我这里本地开发环境和正式环境是2个yml文件拆分出来的,命令打包`mvn clean package -Pprod`则会使用`application-prod.yml`文件,`active: @spring.profiles.active@`的值也就是`active: prod`。基本上到这步已经可以满足需求了。当然你也可以就一个`application.yml`所有可能会根据环境改变的参数配置在`pom.xml`里然后`application.yml`就写pom里的配置`@xxx@`。
- 后续功能:这里的`active: @spring.profiles.active@`,`@`占位符也可以通过配置`pom`自定义的,增加配置如下:

```
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-resources-plugin</artifactId>
    <version>${maven-resources-plugin.version}</version>
    <executions>
        <execution>
            <id>default-resources</id>
            <phase>validate</phase>
            <goals>
                <goal>copy-resources</goal>
            </goals>
            <configuration>
                <outputDirectory>target/classes</outputDirectory>
                <useDefaultDelimiters>false</useDefaultDelimiters>
                <delimiters>
                    <delimiter>#</delimiter>
                </delimiters>
                <resources>
                    <resource>
                        <directory>src/main/resources/</directory>
                        <filtering>true</filtering>
                    </resource>
                </resources>
            </configuration>
        </execution>
    </executions>
</plugin>
 
```
- 这里`<delimiter>#</delimiter>`用来增加一个占位符，Maven本身有占位符`${xxx}`，但这个占位符被SpringBoot占用了，所以我们就再定义一个。`<filtering>true</filtering>`表示打开过滤器开关，这样`application.yml`文件中的`#spring.profiles.active#`部分就会替换为`pom.xml`里`profiles`中定义的 `spring.profiles.active`变量值。
