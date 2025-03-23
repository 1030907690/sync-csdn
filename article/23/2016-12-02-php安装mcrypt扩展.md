---
layout:					post
title:					"php安装mcrypt扩展"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
查了一下资料使用 yum install php-mcrypt 安装mcrypt扩展时会提示没有安装包

Setting up Install Process
No package php-mcrypt available.
Error: Nothing to do

mcrypt 是加密扩展库，加载了它可以用他里面自带的22种加密解密算法

CentOS6 默认安装的是php5.3.2

默认的 redhat repos php中是没有 mcrypt 扩展的
根据红帽的官方消息（https://bugzilla.redhat.com/show_bug.cgi?id=621268）RHEL 不打算添加PHP的mcrypt 的支持
Joe Orton 2010-08-05 04:47:17 EDT

Thanks for the report.

We are not planning to ship mcrypt support for PHP.

解决方案：

从php 官网下载新的php 5.3 源码包后http://www.php.net/releases/，解压到本地目录
进入解压目录下的 ext 目录后会发现有 mcrypt ，
进入 mcrypt 目录

[root@weekend109 php-5.5.36]# cd ext/mcrypt
[root@weekend109 mcrypt]# phpize
Configuring for:
PHP Api Version:         20090626
Zend Module Api No:      20090626
Zend Extension Api No:   220090626
注意：如果报 -bash:phpize not Found  那么 yum install php-devel 就可以使phpize进行动态编译安装扩展

[root@weekend109 mcrypt]# ./configure  -with-php-config=/usr/bin/php-config
checking for grep that handles long lines and -e... /bin/grep
checking for egrep... /bin/grep -E
checking for a sed that does not truncate output... /bin/sed
checking for cc... cc
checking for C compiler default output file name... a.out
checking whether the C compiler works... yes
checking whether we are cross compiling... no
checking for suffix of executables... 
checking for suffix of object files... o
checking whether we are using the GNU C compiler... yes
checking whether cc accepts -g... yes
checking for cc option to accept ISO C89... none needed
checking how to run the C preprocessor... cc -E
checking for icc... no
checking for suncc... no
checking whether cc understands -c and -o together... yes
checking for system library directory... lib
checking if compiler supports -R... no
checking if compiler supports -Wl,-rpath,... yes
checking build system type... i686-pc-linux-gnu
checking host system type... i686-pc-linux-gnu
checking target system type... i686-pc-linux-gnu
checking for PHP prefix... /usr
checking for PHP includes... -I/usr/include/php -I/usr/include/php/main -I/usr/include/php/TSRM -I/usr/include/php/Zend -I/usr/include/php/ext -I/usr/include/php/ext/date/lib
checking for PHP extension directory... /usr/lib/php/modules
checking for PHP installed headers prefix... /usr/include/php
checking if debug is enabled... no
checking if zts is enabled... no
checking for re2c... no
configure: WARNING: You will need re2c 0.13.4 or later if you want to regenerate PHP parsers.
checking for gawk... gawk
checking for mcrypt support... yes, shared
checking for libmcrypt version... >= 2.5.6
checking for mcrypt_module_open in -lmcrypt... no
checking for mcrypt_module_open in -lmcrypt... yes
checking for a sed that does not truncate output... (cached) /bin/sed
checking for fgrep... /bin/grep -F
checking for ld used by cc... /usr/bin/ld
checking if the linker (/usr/bin/ld) is GNU ld... yes
checking for BSD- or MS-compatible name lister (nm)... /usr/bin/nm -B
checking the name lister (/usr/bin/nm -B) interface... BSD nm
checking whether ln -s works... yes
checking the maximum length of command line arguments... 1966080
checking whether the shell understands some XSI constructs... yes
checking whether the shell understands "+="... yes
checking for /usr/bin/ld option to reload object files... -r
checking for objdump... objdump
checking how to recognize dependent libraries... pass_all
checking for ar... ar
checking for strip... strip
checking for ranlib... ranlib
checking command to parse /usr/bin/nm -B output from cc object... ok
checking for ANSI C header files... yes
checking for sys/types.h... yes
checking for sys/stat.h... yes
checking for stdlib.h... yes
checking for string.h... yes
checking for memory.h... yes
checking for strings.h... yes
checking for inttypes.h... yes
checking for stdint.h... yes
checking for unistd.h... yes
checking for dlfcn.h... yes
checking for objdir... .libs
checking if cc supports -fno-rtti -fno-exceptions... no
checking for cc option to produce PIC... -fPIC -DPIC
checking if cc PIC flag -fPIC -DPIC works... yes
checking if cc static flag -static works... no
checking if cc supports -c -o file.o... yes
checking if cc supports -c -o file.o... (cached) yes
checking whether the cc linker (/usr/bin/ld) supports shared libraries... yes
checking whether -lc should be explicitly linked in... no
checking dynamic linker characteristics... GNU/Linux ld.so
checking how to hardcode library paths into programs... immediate
checking whether stripping libraries is possible... yes
checking if libtool supports shared libraries... yes
checking whether to build shared libraries... yes
checking whether to build static libraries... no
configure: creating ./config.status
config.status: creating config.h
config.status: executing libtool commands
[root@weekend109 mcrypt]# make && make install
/bin/sh /home/zzq/software/php-5.5.36/ext/mcrypt/libtool --mode=compile cc  -I. -I/home/zzq/software/php-5.5.36/ext/mcrypt -DPHP_ATOM_INC -I/home/zzq/software/php-5.5.36/ext/mcrypt/include -I/home/zzq/software/php-5.5.36/ext/mcrypt/main -I/home/zzq/software/php-5.5.36/ext/mcrypt -I/usr/include/php -I/usr/include/php/main -I/usr/include/php/TSRM -I/usr/include/php/Zend -I/usr/include/php/ext -I/usr/include/php/ext/date/lib -I/usr/local/include  -DHAVE_CONFIG_H  -g -O2   -c /home/zzq/software/php-5.5.36/ext/mcrypt/mcrypt.c -o mcrypt.lo 
libtool: compile:  cc -I. -I/home/zzq/software/php-5.5.36/ext/mcrypt -DPHP_ATOM_INC -I/home/zzq/software/php-5.5.36/ext/mcrypt/include -I/home/zzq/software/php-5.5.36/ext/mcrypt/main -I/home/zzq/software/php-5.5.36/ext/mcrypt -I/usr/include/php -I/usr/include/php/main -I/usr/include/php/TSRM -I/usr/include/php/Zend -I/usr/include/php/ext -I/usr/include/php/ext/date/lib -I/usr/local/include -DHAVE_CONFIG_H -g -O2 -c /home/zzq/software/php-5.5.36/ext/mcrypt/mcrypt.c  -fPIC -DPIC -o .libs/mcrypt.o
/bin/sh /home/zzq/software/php-5.5.36/ext/mcrypt/libtool --mode=compile cc  -I. -I/home/zzq/software/php-5.5.36/ext/mcrypt -DPHP_ATOM_INC -I/home/zzq/software/php-5.5.36/ext/mcrypt/include -I/home/zzq/software/php-5.5.36/ext/mcrypt/main -I/home/zzq/software/php-5.5.36/ext/mcrypt -I/usr/include/php -I/usr/include/php/main -I/usr/include/php/TSRM -I/usr/include/php/Zend -I/usr/include/php/ext -I/usr/include/php/ext/date/lib -I/usr/local/include  -DHAVE_CONFIG_H  -g -O2   -c /home/zzq/software/php-5.5.36/ext/mcrypt/mcrypt_filter.c -o mcrypt_filter.lo 
libtool: compile:  cc -I. -I/home/zzq/software/php-5.5.36/ext/mcrypt -DPHP_ATOM_INC -I/home/zzq/software/php-5.5.36/ext/mcrypt/include -I/home/zzq/software/php-5.5.36/ext/mcrypt/main -I/home/zzq/software/php-5.5.36/ext/mcrypt -I/usr/include/php -I/usr/include/php/main -I/usr/include/php/TSRM -I/usr/include/php/Zend -I/usr/include/php/ext -I/usr/include/php/ext/date/lib -I/usr/local/include -DHAVE_CONFIG_H -g -O2 -c /home/zzq/software/php-5.5.36/ext/mcrypt/mcrypt_filter.c  -fPIC -DPIC -o .libs/mcrypt_filter.o
/home/zzq/software/php-5.5.36/ext/mcrypt/mcrypt_filter.c: In function ‘php_mcrypt_filter_create’:
/home/zzq/software/php-5.5.36/ext/mcrypt/mcrypt_filter.c:210: warning: passing argument 1 of ‘mcrypt_module_open’ discards qualifiers from pointer target type
/usr/local/include/mutils/mcrypt.h:38: note: expected ‘char *’ but argument is of type ‘const char *’
/bin/sh /home/zzq/software/php-5.5.36/ext/mcrypt/libtool --mode=link cc -DPHP_ATOM_INC -I/home/zzq/software/php-5.5.36/ext/mcrypt/include -I/home/zzq/software/php-5.5.36/ext/mcrypt/main -I/home/zzq/software/php-5.5.36/ext/mcrypt -I/usr/include/php -I/usr/include/php/main -I/usr/include/php/TSRM -I/usr/include/php/Zend -I/usr/include/php/ext -I/usr/include/php/ext/date/lib -I/usr/local/include  -DHAVE_CONFIG_H  -g -O2   -o mcrypt.la -export-dynamic -avoid-version -prefer-pic -module -rpath /home/zzq/software/php-5.5.36/ext/mcrypt/modules  mcrypt.lo mcrypt_filter.lo -Wl,-rpath,/usr/local/lib -L/usr/local/lib -lmcrypt
libtool: link: cc -shared  .libs/mcrypt.o .libs/mcrypt_filter.o   -L/usr/local/lib /usr/local/lib/libmcrypt.so  -Wl,-rpath -Wl,/usr/local/lib   -Wl,-soname -Wl,mcrypt.so -o .libs/mcrypt.so
libtool: link: ( cd ".libs" && rm -f "mcrypt.la" && ln -s "../mcrypt.la" "mcrypt.la" )
/bin/sh /home/zzq/software/php-5.5.36/ext/mcrypt/libtool --mode=install cp ./mcrypt.la /home/zzq/software/php-5.5.36/ext/mcrypt/modules
libtool: install: cp ./.libs/mcrypt.so /home/zzq/software/php-5.5.36/ext/mcrypt/modules/mcrypt.so
libtool: install: cp ./.libs/mcrypt.lai /home/zzq/software/php-5.5.36/ext/mcrypt/modules/mcrypt.la
libtool: finish: PATH="/usr/local/jdk1.7.0_79/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/home/zzq/app/hadoop-2.4.1/bin:/home/zzq/app/hadoop-2.4.1/sbin:/home/zzq/bin:/sbin" ldconfig -n /home/zzq/software/php-5.5.36/ext/mcrypt/modules
----------------------------------------------------------------------
Libraries have been installed in:
   /home/zzq/software/php-5.5.36/ext/mcrypt/modules

If you ever happen to want to link against installed libraries
in a given directory, LIBDIR, you must either use libtool, and
specify the full pathname of the library, or use the `-LLIBDIR'
flag during linking and do at least one of the following:
   - add LIBDIR to the `LD_LIBRARY_PATH' environment variable
     during execution
   - add LIBDIR to the `LD_RUN_PATH' environment variable
     during linking
   - use the `-Wl,-rpath -Wl,LIBDIR' linker flag
   - have your system administrator add LIBDIR to `/etc/ld.so.conf'

See any operating system documentation about shared libraries for
more information, such as the ld(1) and ld.so(8) manual pages.
----------------------------------------------------------------------

Build complete.
Don't forget to run 'make test'.

Installing shared extensions:     /usr/lib/php/modules/
如果make && make install报错/home/zzq/software/php-5.5.36/ext/mcrypt/mcrypt.c:283: error: ‘PHP_FE_END’ undeclared here (not in a function)
make: *** [mcrypt.lo] Error 1

源码有错执行这个：

[root@weekend109 mcrypt]# sed -i 's|PHP_FE_END|{NULL,NULL,NULL}|' ./*.c
[root@weekend109 mcrypt]# sed -i 's|ZEND_MOD_END|{NULL,NULL,NULL}|' ./*.c
编辑php.ini

[root@weekend109 mcrypt]# vim /etc/php.ini
加入mcrypt.so，      mcrypt.so默认在/usr/lib/php/modules/里面

extension_dir = "/usr/lib/php/modules/"
extension = "mcrypt.so"




用

php -m
能查看到mcrypt就成功了

网页上也能看到





​