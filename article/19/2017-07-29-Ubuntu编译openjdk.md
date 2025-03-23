---
layout:					post
title:					"Ubuntu编译openjdk"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
最近看深入理解Java虚拟机：JVM高级特性与最佳实践（第2版）想自己实践下编译一个openjdk出来，但是照着操作很多次还是没成功，里面有些编译方法应该是过时了吧，于是自己查了些资料，实验了下。现在分享给大家

一、下载openjdk源码和搭建环境

1、下载openjdk源码我下载的是openjdk8的：

  

hg clone http://hg.openjdk.java.net/jdk8/jdk8 openjdk8
cd openjdk8
bash get_source.sh
我这里是直接用的Mercurial代码版本管理工具拉下了的，如果没有安装要先安装才能用hg 

2、下载一个openjdk或者是我们平时写代码用的jdk作为bootstrap JDK（注意：需要使用JDK 7及之后版本）

sudo apt install openjdk-8-jdk
sudo apt build-dep openjdk-8-jdk
安装其他依赖：

sudo apt-get install build essential gawk m4 libasound2-dev libcups2-dev libxrender-dev xorg-dev xutils-dev x11proto-print-dev binutils libmotif3 libmotif-dev ant 
二、安装

1、编写一个shell脚本在openjdk8文件夹下运行

build.sh 

# 不生成文档，节约时间。
export NO_DOCS=true
sh ./configure
make all
然后运行这个脚本，如果编译成功了可以看到如下图：



然后到/home/zzq/software/openjdk8/build/linux-x86_64-normal-server-release/images/j2sdk-image（相对路径是build/linux-x86_64-normal-server-release/images/j2sdk-image）目录试试用命令看看



已经看可以看到版本了那就成功了。

三、常见的编译 时的错误

1、This OS is not supported  不支持当前系统

    

hotspot/make/linux/Makefile文件修改第228行
vi hotspot/make/linux/Makefile
# line 228. ubuntu 16.04 using kernel 4.x.
SUPPORTED_OS_VERSION = 2.4% 2.5% 2.6% 3% 4%
修改Make参数语法。

vi hotspot/make/linux/makefiles/adjust-mflags.sh
# line 67. (新版本make语法有变动)
 s/ -\([^        I][^    ]*\)j/ -\1 -j/
2、出现undefine symbols错误

将 hotspot/src/share/vm/gc_implementation/g1/g1SATBCardTableModRefBS.cpp 中的template <class T> void write_ref_array_pre_work(T* dst, int count)方法，提升到对应的头文件g1SATBCardTableModRefBS.hpp中。
# 模板函数定义需要出现在头文件中，以便编译器为其生成特化版本。若无此修改，运行编译后的java程序，将出现undefine symbols错误
我只出现过第一个错误。



​