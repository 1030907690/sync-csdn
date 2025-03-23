---
layout:					post
title:					"FreeMarker日期打印不出来"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
###使用freeMarker${userInfo.createTime}直接打印一个用户的时间会报错,空白页面,原因是因为需要转换一次

```
${userInfo.createTime?date}                                           //标准日期转日期字符串

${userInfo.createTime?datetime}　　　　　　　　　　　　　 //标准日期转日期+时间 字符串

${userInfo.createTime?string("yyyy-MM-dd HH:mm:ss")}   //标准日期转自定格式 字符串
```