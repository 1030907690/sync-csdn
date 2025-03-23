---
layout:					post
title:					"nginx make报错Makefile:8: recipe for target 'build' failed"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 编译安装nginx时使用`./configure --prefix=/usr/local/nginx --with-pcre=/usr/local/pcre` 没有报错,然后在`make`,发现异常,报错信息如下:
> root@iZwz91qim1yorfi3qvql46Z:~/software/nginx-1.12.2# make
	make -f objs/Makefile
	make[1]: Entering directory '/root/software/nginx-1.12.2'
	cd /usr/local/pcre \
	&& if [ -f Makefile ]; then make distclean; fi \
	&& CC="cc" CFLAGS="-O2 -fomit-frame-pointer -pipe " \
	./configure --disable-shared 
	/bin/sh: 3: ./configure: not found
	objs/Makefile:1167: recipe for target '/usr/local/pcre/Makefile' failed
	make[1]: *** [/usr/local/pcre/Makefile] Error 127
	make[1]: Leaving directory '/root/software/nginx-1.12.2'
	Makefile:8: recipe for target 'build' failed
	make: *** [build] Error 2

- 报错信息提到了进入pcre时发生的异常找不到 `./configure: not found`
>root@iZwz91qim1yorfi3qvql46Z:~/software/nginx-1.12.2# ./configure --help | grep '\--with-pcre'
  --with-pcre                        force PCRE library usage
  --with-pcre=DIR                    set path to PCRE library sources
  --with-pcre-opt=OPTIONS            set additional build options for PCRE
  --with-pcre-jit                    build PCRE with JIT compilation support

- 使用了一下help发现pcre的`路径要写源码路径而不是安装路径`, 改成源码路径就正确了`./configure --prefix=/usr/local/nginx --with-pcre=/root/software/pcre-8.35  `