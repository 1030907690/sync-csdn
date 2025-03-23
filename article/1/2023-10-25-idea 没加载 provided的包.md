---
layout:					post
title:					"idea 没加载 provided的包"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 我的版本是IntelliJ IDEA 2022.1.4 (Community Edition)，本地调试不知道为什么不加载provided的包。后来找到这篇文章[https://youtrack.jetbrains.com/issue/IDEA-107048](https://youtrack.jetbrains.com/issue/IDEA-107048)才知道这是个bug。不知道其他版本会不会出现这种问题。



## 解决方案
- 我利用的是`profiles`标签，例如我对`ffmpeg`的配置。本地是windows，线上是linux。

```xml
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

            <dependencies>
                <dependency>
                    <groupId>org.bytedeco.javacpp-presets</groupId>
                    <artifactId>ffmpeg</artifactId>
                    <version>${ffmpeg-platform}</version>
                    <classifier>windows-x86_64</classifier>
                </dependency>
            </dependencies>
        </profile>

        <!-- 生产环境 -->
        <profile>
            <id>prod</id>
            <properties>
                <spring.profiles.active>prod</spring.profiles.active>
            </properties>

            <dependencies>
                <dependency>
                    <groupId>org.bytedeco.javacpp-presets</groupId>
                    <artifactId>ffmpeg</artifactId>
                    <version>${ffmpeg-platform}</version>
                    <classifier>linux-x86_64</classifier>
                </dependency>
            </dependencies>
        </profile>

    </profiles>
```

- 根据环境区分，要哪些包。