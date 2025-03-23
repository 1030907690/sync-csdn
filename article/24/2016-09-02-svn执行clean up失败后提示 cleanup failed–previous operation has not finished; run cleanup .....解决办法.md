---
layout:					post
title:					"svn执行clean up失败后提示 cleanup failed–previous operation has not finished; run cleanup .....解决办法"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
大多原因是由于没有先去更新多次操作文件引起的。

解决方案找到你.svn目录下的wc.db文件

下载<a target="blank" href="http://download.csdn.net/detail/baidu_19473529/9620489">sqlite3.exe</a>这个工具

为了方便可以放在.svn目录下：



然后运行cmd：

启动cmd执行sqlite3 wc.db "select * from work_queue"

看到有记录，下一步执行sqlite3 wc.db "delete from work_queue" 删除



好，我们在执行SVN的clean up就可以成功了。

 另外svn cleanup 报lock的问题:

        需要运行 ： sqlite3 wc.db "delete from wc_lock"; 

​