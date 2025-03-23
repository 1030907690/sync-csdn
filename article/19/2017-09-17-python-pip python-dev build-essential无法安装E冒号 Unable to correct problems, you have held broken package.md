---
layout:					post
title:					"python-pip python-dev build-essential无法安装E: Unable to correct problems, you have held broken package"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
用apt-get安装python-dev老是报错，缺少依赖包，报错信息：

The following packages have unmet dependencies:
 build-essential : Depends: dpkg-dev (>= 1.13.5) but it is not going to be installed
 python-dev : Depends: python (= 2.7.9-1) but 2.7.11-1 is to be installed
              Depends: libpython-dev (= 2.7.9-1) but it is not going to be installed
              Depends: python2.7-dev (>= 2.7.9-1~) but it is not going to be installed
 python-pip : Depends: python-setuptools (>= 0.6c1) but it is not going to be installed
              Recommends: python-dev-all (>= 2.6) but it is not installable
E: Unable to correct problems, you have held broken packages.
第一种方法：

将破损的包删除掉，再执行安装

sudo apt-get remove  dpkg-dev python libpython-dev python2.7-dev python-setuptools python-dev-all
第二种解决办法：

我使用了一下aptitude去安装

aptitude与 apt-get 一样，是 Debian 及其衍生系统中功能极其强大的包管理工具。与 apt-get 不同的是，aptitude在处理依赖问题上更佳一些。举例来说，aptitude在删除一个包时，会同时删除本身所依赖的包。这样，系统中不会残留无用的包，整个系统更为干净
首先先安装aptitude

sudo apt-get install aptitude 
然后安装你要的东西

sudo aptitude install xxxx


​