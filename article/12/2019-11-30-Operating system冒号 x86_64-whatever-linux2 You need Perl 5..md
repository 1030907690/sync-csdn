---
layout:					post
title:					"Operating system: x86_64-whatever-linux2 You need Perl 5."
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 解决办法,安装perl，网址[https://www.cpan.org/src/README.html](https://www.cpan.org/src/README.html):

```
     wget https://www.cpan.org/src/5.0/perl-5.30.1.tar.gz
     tar -xzf perl-5.30.1.tar.gz
     cd perl-5.30.1
     ./Configure -des -Dprefix=$HOME/localperl
     make
     make test
     make install
```
