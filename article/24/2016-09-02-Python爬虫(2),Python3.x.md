---
layout:					post
title:					"Python爬虫(2),Python3.x"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#中文注释
import urllib.request;


url = "http://www.baidu.com";
#头信息
user_agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;";
headers ={'User-Agent':user_agent};
req = urllib.request.Request(url,headers=headers);
response = urllib.request.urlopen(req)
html = response.read()
print('loading...baidu');
print(html);
​