---
layout:					post
title:					"ArrayList和LinkedList原理"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
ArrayList：

ArrayList 使用默认无参数构造函数，底层的Object数组长度默认为10，当长度不够用自动增长0.5倍

源代码：

默认长度10

    /**
     * Default initial capacity.
     */
    private static final int DEFAULT_CAPACITY = 10;
如果数组长度不够增长0.5倍grow方法

       int newCapacity = oldCapacity + (oldCapacity >> 1);
ArrayList为什么查询快，增删慢？

查询快：



因为数组的内存地址排列是连续的，可以很快找到比如 list.get(100); 第一个元素内存地址是0x98，那么内存地址加100就找到了。

增删慢：

增：



我们假设这个数组长度容量为7，现在要再添加一个元素它会怎么做呢？

增加元素时，先检测数组长度是否够用，如果底层Object数组长度不够，增加0.5倍的长度，形成一个新的Object数组，并将之前的数组元素copy到新的数组里面。

删：



删除慢：当删除里面的其中一个数据时，后面的数据要全部移动一个位置。

LinkedList：



使用链表数据结构实现，特点，增删快，查询慢。

查询慢：元素之前内存地址不连续，只能挨个挨个遍历查找

增加：



插入数据时，只需要改变内存地址的指向；



将和它有关系的内存地址指向删除掉，没人指向它，它就成为了垃圾对象。



​