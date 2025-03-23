---
layout:					post
title:					"Python爬虫(1)，Python3.x"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
直接上代码：

import urllib.request;//引入包

response = urllib.request.urlopen("http://www.baidu.com");//加载网页
html=response.read();//读取
print('loading...baidu');
print(html);//打印网页源码


​