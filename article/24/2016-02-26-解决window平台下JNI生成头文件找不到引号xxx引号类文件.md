---
layout:					post
title:					"解决window平台下JNI生成头文件找不到"xxx"类文件"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
想写一个java调用C的小程序。

java代码：

package edu.netcom.jni;

public class WinMsgDll {
    static{
        System.loadLibrary("WinMsgDll"); // (1)第一步，加载动态库
    }
    public native void showMsgBox(String str);// (2)第二步，声明这个方法
   
    
}



然后我用javac 生成了WinMsgDll.class文件

 用命令javah -jni edu.netcom.jni.WinMsgBox



然后去查了命令有问题 ，应该是这样的



javah -classpath . -jni 类路径.JNI类





生成了edu_netcom_jni_WinMsgDll.h头文件。