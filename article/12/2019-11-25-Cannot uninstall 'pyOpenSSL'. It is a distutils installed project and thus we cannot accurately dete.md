---
layout:					post
title:					"Cannot uninstall 'pyOpenSSL'. It is a distutils installed project and thus we cannot accurately dete"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- linux python2.7安装scrapy报错 ERROR: Cannot uninstall 'pyOpenSSL'. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall.
- 应该就是这个six导致的(真是666)，忽略它 ；解决办法：
	- 原来的命令(我是本地文件安装的)
	```bash
	pip2.7 install Scrapy-1.8.0-py2.py3-none-any.whl 
	```
	- 改成 
	```bash
	
	pip2.7 install Scrapy-1.8.0-py2.py3-none-any.whl   --upgrade --ignore-installed six 
	```
