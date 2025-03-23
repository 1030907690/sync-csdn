---
layout:					post
title:					"Linux下python安装pip"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
pip是一个安装和管理 Python 包的工具,用它我们可以方便的拉一些依赖的库下来

首先下载并安装setuptools


wget --no-check-certificate https://bootstrap.pypa.io/ez_setup.py
sudo python ez_setup.py --insecure

再到python  https://pypi.python.org/pypi/pip官网下载pip安装包，解压到某个位置



然后执行（我这儿是9.0.1版本的）：

tar -zxxf pip-9.0.1.tar.gz
[root@localhost software]# cd pip-9.0.1/
[root@localhost pip-9.0.1]# python setup.py install

然后就可以用pip命令了



​