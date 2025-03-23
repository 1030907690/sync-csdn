---
layout:					post
title:					"启动nginx报错/usr/local/nginx/sbin/nginx: error while loading shared libraries: libpcre.so.1: cannot ope"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
在启动nginx时报错

[zzq@weekend110 pcre-8.39]$ sudo /usr/local/nginx/sbin/nginx 
/usr/local/nginx/sbin/nginx: error while loading shared libraries: libpcre.so.1: cannot open shared object file: No such file or directory

确认已经安装了pcre和zlib:  pcre下载地址https://sourceforge.net/projects/pcre/files/pcre/ zlib下载地址https://sourceforge.net/projects/libpng/files/zlib/



执行以上步奏解决：



​