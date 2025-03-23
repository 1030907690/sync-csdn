---
layout:					post
title:					"linux和windows安装openOffice将excel、doc文件转成pdf或html"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
一、准备工作（下载软件等等）

1、openoffice官网下载地址 Apache OpenOffice - 下载    下载你需要的版本，windows或者linux等等



2、除了openoffice以外我们还需要用到pdf2htmlEX这个软件；下载地址https://github.com/coolwanglu/pdf2htmlEX/;https://github.com/coolwanglu/pdf2htmlEX/wiki/Building 这里有具体的安装步骤说明，作者是以Fedora为示例，CentOS也类似，其中大部分依赖项可以通过yum安装，不必一一用源码安装      ；pdf2htmlEX需要依赖2.0。通过pdf2htmlEX作者放出的分支，下载fontforge：GitHub - coolwanglu/fontforge at pdf2htmlEX，查看INSTALL-Git.md文件，其中的fontforge需要手动单独安装，因为目前的yum源中的fontforge版本是低于2.0的，按照说明依次执行：(windows的可以忽略此步骤,直接去下载一个windows版本的,我分享的下载链接里也会有pdf2htmlEX windows版本的)

二、安装

  1、安装openoffice

将下载好的tar包解压出来，进入到RPMS目录，然后会看到很多rpm的包，直接全部安装



	rpm -ivh *.rpm
rpm -ivh *.rpm
安装完成后会生成一个desktop-integration文件夹，进入desktop-integration文件夹

[zzq@weekend110 RPMS]$ cd desktop-integration/
查看有以下几个版本
[zzq@weekend110 desktop-integration]$ ll
总用量 2004
-rw-rw-r--. 1 zzq zzq 469674 9月  26 2016 openoffice4.1.3-freedesktop-menus-4.1.3-9783.noarch.rpm
-rw-rw-r--. 1 zzq zzq 490143 9月  26 2016 openoffice4.1.3-mandriva-menus-4.1.3-9783.noarch.rpm
-rw-rw-r--. 1 zzq zzq 541506 9月  26 2016 openoffice4.1.3-redhat-menus-4.1.3-9783.noarch.rpm
-rw-rw-r--. 1 zzq zzq 544148 9月  26 2016 openoffice4.1.3-suse-menus-4.1.3-9783.noarch.rpm
我的是centos接近于Redhat所以我安装的是Redhat版本

[zzq@weekend110 desktop-integration]$ sudo rpm -ivh openoffice4.1.3-redhat-menus-4.1.3-9783.noarch.rpm 
[sudo] password for zzq: 
准备中...                          ################################# [100%]
	file /usr/bin/soffice from install of openoffice4.1.3-redhat-menus-4.1.3-9783.noarch conflicts with file from package libreoffice-core-1:5.0.6.2-3.el7.x86_64
下面就是启动openOffice
 

[zzq@weekend110 desktop-integration]$ soffice -headless -accept="socket,host=127.0.0.1,port=8100;urp;" -nofirststartwizard &
[1] 23269
[zzq@weekend110 desktop-integration]$ Warning: -headless is deprecated.  Use --headless instead.
Warning: -accept=socket,host=127.0.0.1,port=8100;urp; is deprecated.  Use --accept=socket,host=127.0.0.1,port=8100;urp; instead.
Warning: -nofirststartwizard is deprecated.  Use --nofirststartwizard instead.
查看进程
[zzq@weekend110 desktop-integration]$ 
[zzq@weekend110 ~]$ ps -ef | grep 8100
zzq       23286      1  0 11:22 ?        00:00:00 /usr/lib64/libreoffice/program/soffice.bin -headless -accept=socket,host=127.0.0.1,port=8100;urp; -nofirststartwizard
zzq       27004  25312  0 11:31 pts/2    00:00:00 grep --color=auto 8100

有进程则表示openoffice已经启动成功了（windows上检测端口的命令为netstat -ano | findstr "8100"）。

2、安装pdf2htmlEX

从githut下载压缩包解压，必须要先安装fontforge-pdf2htmlEX

[zzq@weekend110 software]$ unzip -o -d ~/app/  pdf2htmlEX-master.zip
[zzq@weekend110 software]$ unzip -o -d ~/app/ fontforge-pdf2htmlEX.zip 
[zzq@weekend110 software]$ cd ~/app
[zzq@weekend110 app]$ ll
总用量 12
drwxr-xr-x. 11 zzq zzq  204 4月  13 14:53 apache-activemq-5.11.1
drwxr-xr-x.  9 zzq zzq  160 3月   9 13:50 apache-tomcat-7.0.76
drwxr-xr-x. 10 zzq zzq  258 4月  13 16:57 FastDFS
drwxrwxr-x. 33 zzq zzq 4096 3月  22 2014 fontforge-pdf2htmlEX
drwxr-xr-x.  8 zzq zzq  233 4月  11 2015 jdk1.7.0_80
drwxr-xr-x. 10 zzq zzq  187 4月  12 01:19 jprofiler10.0.1
drwxrwxr-x.  4 zzq zzq  124 2月  27 2015 libfastcommon-master
drwxr-xr-x.  8 zzq zzq  113 7月  10 2015 nexus-2.11.4-01
drwxrwxr-x.  8 zzq zzq 4096 7月  18 11:54 pdf2htmlEX-master
-rwxrw-r--.  1 zzq zzq   90 4月   9 18:24 run.sh
drwxr-xr-x.  3 zzq zzq   37 7月  10 2015 sonatype-work
drwxrwxr-x.  5 zzq zzq   49 9月  26 2016 zh-CN
进入到fontforge-pdf2htmlEX依次执行

./autogen.sh  
./configure
make
make install
注意安装fontforge相关依赖

sudo yum install libtool* -y
 不安装就会报错Preparing build ... ERROR: libtoolize failed
安装 fontforge-pdf2htmlEX
[zzq@weekend110 fontforge-pdf2htmlEX]$ sudo ./autogen.sh 
Preparing the fontforge build system...please wait

Found GNU Autoconf version 2.69
Found GNU Automake version 1.13.4
Found GNU Libtool version 2.4.2

Automatically preparing build ... done

The fontforge build system is now prepared.  To build here, run:
  ./configure
  make
[zzq@weekend110 fontforge-pdf2htmlEX]$ ./configure
checking build system type... x86_64-unknown-linux-gnu
checking host system type... x86_64-unknown-linux-gnu
checking for a BSD-compatible install... /usr/bin/install -c
checking whether build environment is sane... yes
checking for a thread-safe mkdir -p... /usr/bin/mkdir -p
checking for gawk... gawk
checking whether make sets $(MAKE)... yes
checking whether make supports nested variables... yes
checking how to create a pax tar archive... gnutar
checking whether to enable maintainer-specific portions of Makefiles... yes
checking for style of include used by make... GNU
checking for gcc... gcc
checking whether the C compiler works... yes
checking for C compiler default output file name... a.out
checking for suffix of executables... 
checking whether we are cross compiling... no
checking for suffix of object files... o
checking whether we are using the GNU C compiler... yes
checking whether gcc accepts -g... yes
checking for gcc option to accept ISO C89... none needed
checking dependency style of gcc... gcc3
checking how to run the C preprocessor... gcc -E
看到有报错，因为还缺少一些东西 glib和gio 安装他们 再执行上一步
configure: error: Package requirements (glib-2.0 >= 2.6 gio-2.0) were not met:

No package 'glib-2.0' found
No package 'gio-2.0' found

Consider adjusting the PKG_CONFIG_PATH environment variable if you
installed software in a non-standard prefix.

Alternatively, you may set the environment variables GLIB_CFLAGS
and GLIB_LIBS to avoid the need to call pkg-config.
See the pkg-config man page for more details.
[zzq@weekend110 fontforge-pdf2htmlEX]$ make 
make: *** 没有指明目标并且找不到 makefile。 停止。
[zzq@weekend110 fontforge-pdf2htmlEX]$ sudo yum install glib* gio* freetype*  pango* -y


[zzq@weekend110 fontforge-pdf2htmlEX]$make && make install
执行到这里fontforge-pdf2htmlEX就安装成功了

2、安装pdf2htmlEX

[zzq@weekend110 pdf2htmlEX-master]$ cmake .
-- checking for module 'poppler>=0.25.0'
--   package 'poppler>=0.25.0' not found
CMake Error at /usr/share/cmake/Modules/FindPkgConfig.cmake:279 (message):
  A required package was not found
Call Stack (most recent call first):
  /usr/share/cmake/Modules/FindPkgConfig.cmake:333 (_pkg_check_modules_internal)
  CMakeLists.txt:22 (pkg_check_modules)


-- checking for module 'cairo>=1.10.0'
--   package 'cairo>=1.10.0' not found
CMake Error at /usr/share/cmake/Modules/FindPkgConfig.cmake:279 (message):
  A required package was not found
Call Stack (most recent call first):
  /usr/share/cmake/Modules/FindPkgConfig.cmake:333 (_pkg_check_modules_internal)
  CMakeLists.txt:28 (pkg_check_modules)


Trying to locate cairo-svg...
CMake Error at CMakeLists.txt:47 (message):
  Error: no SVG support found in Cairo


-- Configuring incomplete, errors occurred!
See also "/home/zzq/app/pdf2htmlEX-master/CMakeFiles/CMakeOutput.log".
[zzq@weekend110 pdf2htmlEX-master]$ 


此处报错，需要导入环境再执行
[root@weekend110 pdf2htmlEX-master]# yum install poppler* -y 
[root@weekend110 pdf2htmlEX-master]#  export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig 
再次执行cmake . 最后一步

[root@weekend110 pdf2htmlEX-master]# make && make install
安装完毕然后我们用命令查看一下版本

[root@weekend110 pdf2htmlEX-master]# pdf2htmlEX -v
pdf2htmlEX: error while loading shared libraries: libfontforge.so.2: cannot open shared object file: No such file or directory
查看pdf2htmlEX版本。但执行转换操作时还会报错：因此，需要导入lib库路径，很简单，vi /etc/profile，在最后加上
[root@weekend110 pdf2htmlEX-master]# export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
[root@weekend110 pdf2htmlEX-master]# pdf2htmlEX -v
pdf2htmlEX version 0.14.6
Copyright 2012-2015 Lu Wang <coolwanglu@gmail.com> and other contributors
Libraries: 
  poppler 0.26.5
  libfontforge 20170718
  cairo 1.14.2
Default data-dir: /usr/local/share/pdf2htmlEX
Supported image format: png jpg svg
安装成功后打个jar的运行结果



这是我在windows上的运行结果：



这是主函数：Test.java

package util;

import java.io.File;

public class Test {
	public static void main(String[] args){
		//String a[] = {"C:\\Users\\sevnce\\Desktop\\exceljs\\test.xlsx","e:\\office\\1.pdf","pdfhtm.html"};
		System.out.println("args length : "+args.length);
		//3个参数 第一个是需要转换的excel文件  第二个是转换的pdf路径和名称 第三个是转换的html文件名称
		office2pdf2html(args);
		//office2html();
	}
	
	public static void office2pdf2html(String [] args) {
		String sourceFile = args[0];//"C:\\Users\\sevnce\\Desktop\\exceljs\\test.xlsx";
		String destFile = args[1];//"e:\\office\\1.pdf";
		String htmlFile = args[2];//"pdfhtmlc.html";
		// office文件转pdf
		int result = Office2PDFUtil.office2PDF(sourceFile, destFile);
		if(result == 0) {
			System.out.println("office转PDF成功");
			// pdf转html
			if(Pdf2htmlEXUtil.pdf2html(destFile, htmlFile)) {
				System.out.println("pdf转html成功");
			}
			else 
				System.out.println("pdf转html失败");
			
		} else if(result == -1) {
			System.out.println("找不到源文件, 或url.properties配置错误");
		} else {
			System.out.println("office转PDF失败");
		}
		//System.out.println(ClearHtml2Div.clearFormat(htmlStr, docImgPath));
	}
	
	public static void office2html() {
		System.out.println(Doc2HtmlUtil.office2HtmlString(new File("C:\\Users\\sevnce\\Desktop\\exceljs\\test.xlsx"), "e:/office/test"));
	}
}
分享下资料和代码的下载地址：http://download.csdn.net/detail/baidu_19473529/9903553



fontforge-pdf2htmlEX.zip是linux安装pdf2htmlEX的依赖；jodconverter-2.2.2.zip是所需lib包；pdf2htmlEX-master.zip是Linux的pdf2htmlEX；pdf2htmlEX-win32-0.14.6-upx-with-poppler-data.zip是windows的pdf2htmlEX程序；previewOnline.zip是源代码里面都封装好了excel、doc等office文档转pdf和html的方法。

/**********************************安装时遇到的一些问题************************************/

1、/opt/openoffice4/program/soffice.bin: error while loading shared libraries: libXext.so.6: cannot open shared object file: No such file or directory


找不到libXext.so.6文件，去系统里面的/usr/lib64　或者　/usr/lib　查看有没有这个文件，如果有就copy到/opt/openoffice4/program/目录里面，


赋予chmod 777 　libXext.so.6　。如果没有那么要安装该包。


由于我的系统是64位，那么输入yum install libXext.x86_64　，如果是32位系统输入：yum install libXext.i686  。安装完成后去那两个目录找libXext.so.6复制到


/opt/openoffice4/program/目录里面，赋予chmod 777 　libXext.so.6　。






2、 /opt/openoffice4/program/soffice.bin: error while loading shared libraries: libfreetype.so.6: cannot open shared object file: No such file or directory


找不到libfreetype.so.6文件，同上输入：yum install libfreetype.i686，安装完之后去那两个目录找libXext.so.6复制到/opt/openoffice4/program/目录里面，赋予权限。






3、报问题：no suitable windowing system found, exiting. (安装了图形化界面不会出现这个问题)
输入安装:yum groupinstall "X Window System"　，一路安装完之后重启系统，在启动openoffice服务看看。

最后总结下Linux安装pdf2htmlEX的坑比较多总是缺少一些依赖，不过仔细观察错误提示还是能很快解决的。希望能帮助大家上手openoffice



​