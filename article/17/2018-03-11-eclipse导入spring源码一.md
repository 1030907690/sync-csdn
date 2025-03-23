---
layout:					post
title:					"eclipse导入spring源码一"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
###一、准备的软件
- 安装git或者GitHub(不是必须的可以直接在GitHub网页上选择版本下载压缩包，地址[https://github.com/spring-projects/spring-framework/](https://github.com/spring-projects/spring-framework/) ，我选择的是v3.2.18.RELEASE版本) 

- 安装gradle(把源码转成eclipse工程用的,下载地址 ： [https://gradle.org/releases/](https://gradle.org/releases/))


二、配环境和转换源码
- 下载好源码解压再配置好gradle的环境变量。

```
C:\Users\Administrator>gradle -v

------------------------------------------------------------
Gradle 3.5
------------------------------------------------------------

Build time:   2017-04-10 13:37:25 UTC
Revision:     b762622a185d59ce0cfc9cbc6ab5dd22469e18a6

Groovy:       2.4.10
Ant:          Apache Ant(TM) version 1.9.6 compiled on June 29 2015
JVM:          1.8.0_144 (Oracle Corporation 25.144-b01)
OS:           Windows 7 6.1 amd64

```

我这里专门用的是3.5的gradle，4.0及以上的版本编译spring3.2的源码会报找不到构造方法

```
* What went wrong:
Execution failed for task ':spring-orm:eclipseClasspath'.
> Could not find matching constructor for: org.gradle.plugins.ide.eclipse.model.
ProjectDependency(org.codehaus.groovy.runtime.GStringImpl, java.lang.String)
```
我个人不太熟悉gradle,所以只能暂时换了一个低版本的把这个问题给略过了。

- 解压后的spring源码
![这里写图片描述](https://img-blog.csdn.net/20180311173422467?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

就在这个目录执行

```
gradle cleanidea eclipse
```
当然也可以到每个子项目里面去执行。执行日志如下：

```
D:\360极速浏览器下载\spring\spring-framework-3.2.18.RELEASE>gradle cleanidea ecl
ipse
Starting a Gradle Daemon (subsequent builds will be faster)
:buildSrc:clean UP-TO-DATE
:buildSrc:compileJava NO-SOURCE
:buildSrc:compileGroovy
:buildSrc:processResources
:buildSrc:classes
:buildSrc:jar
:buildSrc:assemble
:buildSrc:compileTestJava NO-SOURCE
:buildSrc:compileTestGroovy NO-SOURCE
:buildSrc:processTestResources NO-SOURCE
:buildSrc:testClasses UP-TO-DATE
:buildSrc:test NO-SOURCE
:buildSrc:check UP-TO-DATE
:buildSrc:build
Cleaned up directory 'D:\360极速浏览器下载\spring\spring-framework-3.2.18.RELEAS
E\buildSrc\build\classes\main'
Cleaned up directory 'D:\360极速浏览器下载\spring\spring-framework-3.2.18.RELEAS
E\buildSrc\build\resources\main'
:cleanIdeaModule UP-TO-DATE
:cleanIdeaProject UP-TO-DATE
:cleanIdea UP-TO-DATE
:spring-aop:cleanIdeaModule UP-TO-DATE
:spring-aop:cleanIdea UP-TO-DATE
:spring-aspects:cleanIdeaModule UP-TO-DATE
......
BUILD SUCCESSFUL

Total time: 53.634 secs
```
- 随便打开一个项目,现在里边就有eclipse需要的.classpath和.project文件了
![这里写图片描述](https://img-blog.csdn.net/20180311174030647?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

- 现在用eclipse 试着导入项目，先从spring-beans开始,发现它依赖spring-core项目。
![这里写图片描述](https://img-blog.csdn.net/20180311174443889?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

再导入spring-core。
![这里写图片描述](https://img-blog.csdn.net/20180311174638392?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

我们可以看到虽然项目还有报错，但是我们已经完成一部分了。下面的请看[ eclipse导入spring源码二（丢失的spring-asm-repack和spring-cglib-repack）](http://blog.csdn.net/baidu_19473529/article/details/79518685)