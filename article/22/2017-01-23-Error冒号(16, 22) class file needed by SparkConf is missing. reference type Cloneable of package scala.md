---
layout:					post
title:					"Error:(16, 22) class file needed by SparkConf is missing. reference type Cloneable of package scala"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
编写spark程序报错

Error:(16, 22) class file needed by SparkConf is missing.
reference type Cloneable of package scala refers to nonexisting symbol.
      val conf = new SparkConf().setAppName("wordCount").setMaster("local[2]");

我的pom.xml

    <!-- https://mvnrepository.com/artifact/org.apache.spark/spark-core_2.10 -->
    <dependency>
      <groupId>org.apache.spark</groupId>
      <artifactId>spark-core_2.10</artifactId>
      <version>1.6.3</version>
    </dependency>

原因竟然是我的Scala版本太低了，要2.10的版本，换成2.10的版本好了。

​