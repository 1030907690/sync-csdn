---
layout:					post
title:					"PHP中Notice: unserialize(): Error at offset 109 of 615 bytes in on line 的解决方法"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
今天在集成UCenter通信时偶然遇到unserialize(): Error at offset 109 of 615 bytes，查找资料得到结果

使用unserialize函数将数据储存到数据库的时候遇到了这个报错，后来发现是将gb2312转换成utf-8格式之后，每个中文的字节数从2个增加到3个之后导致了反序列化的时候判断字符长度出现了问题，所以需要使用正则表达式将序列化的数组中的表示字符长度的值重新计算一遍
于是我使用了preg_replace方法，果然就成功了

 $out = preg_replace('!s:(\d+):"(.*?)";!se', "'s:'.strlen('$2').':\"$2\";'", $GLOBALS['_CFG']['integrate_config'] );
    $cfg = unserialize($out);


​