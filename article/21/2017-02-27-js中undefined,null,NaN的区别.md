---
layout:					post
title:					"js中undefined,null,NaN的区别"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
类型分析：

js中的数据类型有undefined,boolean,number,string,object等5种，前4种为原始类型，object为引用类型。

    var a1;
    var a2 = true;
    var a3 = 1;
    var a4 = "Hello";
    var a5 = new Object();
    var a6 = null;
    var a7 = NaN;
    var a8 = undefined;
    document.write("<br />");
    document.write(typeof(a1)); //显示"undefined"
    document.write("<br />");
    document.write(typeof(a2)); //显示"boolean"
    document.write("<br />");
    document.write(typeof(a3)); //显示"number"
    document.write("<br />");
    document.write(typeof(a4)); //显示"string"
    document.write("<br />");
    document.write(typeof(a5)); //显示"object"
    document.write("<br />");
    document.write(typeof(a6)); //显示"object"
    document.write("<br />");
    document.write(typeof(a7)); //显示"number"
    document.write("<br />");
    document.write(typeof(a8)); //显示"undefined"
    document.write("<br />");
输出结果：

undefined
boolean
number
string
object
object
number
undefined
从上面的代码中可以看出未定义的值和定义未赋值的为undefined，未初始化的变量可以用typeof判断，null是一种特殊的object,NaN是一种特殊的number。

​