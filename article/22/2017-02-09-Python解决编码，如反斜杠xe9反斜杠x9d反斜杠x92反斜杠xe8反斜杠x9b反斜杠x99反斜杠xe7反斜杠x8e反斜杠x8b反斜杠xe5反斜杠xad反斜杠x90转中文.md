---
layout:					post
title:					"Python解决编码，如\xe9\x9d\x92\xe8\x9b\x99\xe7\x8e\x8b\xe5\xad\x90转中文"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
利用Python解决编码问题,有些json在控制台打印也是这样的结果

    s = '\xe9\x9d\x92\xe8\x9b\x99\xe7\x8e\x8b\xe5\xad\x90'
    ss = s.encode('raw_unicode_escape')
    print(ss)  # 结果：b'\xe9\x9d\x92\xe8\x9b\x99\xe7\x8e\x8b\xe5\xad\x90'
    sss = ss.decode()
    print(sss)





​