---
layout:					post
title:					"Python和django环境配置(windows版本)"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
需要2个包

1、Python下载地址Download Python | Python.org

2、Django下载地址Download Django | Django

Python可下载可执行的exe文件安装或者是压缩文件安装，使用源文件安装要配置环境变量。安装后测试下

在cmd输入

python

出现这样的效果就是安装成功了：



接下来就是解压下载好的django压缩文件如下：



在使用cmd命令cd 到django目录 执行python setup.py install ：

出现这样的结果就成功了：

执行

import django
django.get_version()
检测是否安装成功



接下来就创建django项目了：

首先配置下django的环境变量





这个时候就可以用

django-admin.py startproject HelloWorld
创建项目了



目录结果：



开启web项目：

python manage.py runserver 0.0.0.0:8000                          #<span style="color: rgb(51, 51, 51); font-family: 'Microsoft Yahei', 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 24px;">0.0.0.0让其它电脑可连接到开发服务器，8000为端口号。如果不说明，那么端口号默认为8000。</span>


访问结果：



好，到此环境已经配好了。

​