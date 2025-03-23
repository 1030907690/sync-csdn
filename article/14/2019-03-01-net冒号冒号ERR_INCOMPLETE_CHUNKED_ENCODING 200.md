---
layout:					post
title:					"net::ERR_INCOMPLETE_CHUNKED_ENCODING 200"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 前端是vue写的,F12查看具体表现为发送了个 option后，不继续发post了,表面上表现是跨域问题，然后控制台报net::ERR_INCOMPLETE_CHUNKED_ENCODING,
- 网上搜索了一下有磁盘满了、chrome的自身问题、tomcat版本和配置的问题,json返回的文本太大，为了少走弯路于是自己用wireshark抓包，得到的结果是`[Malformed Packet: HTTP]`(格式错误的数据包)
- 用的spring mvc @RestController注解返回的json怎么会格式错误?有点不相信于是把数据导下来,在本地测试是完好的(只是发现json内容比较大的特点,有可能真实数据量太大无法解析)。然后继续查关于net::ERR_INCOMPLETE_CHUNKED_ENCODING json数据太大的问题，真的有人遇到过。
- 为了验证一下我把返回的数据加了个条件判断从之前返回201条数现在只返回18条了，打包发布到公网真的就不报net::ERR_INCOMPLETE_CHUNKED_ENCODING异常了，猜想这些软件应该是对返回数据大小有限制吧。
- 我把返回的数据存入到文件里居然有80多KB，确实有点大了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e013cb275bc1b7cc60eb98e4fe31be9e.png)
- 除了限制返回数据量能解决外，我在测试中发现加大Nginx的buffer可以临时解决这个问题。如以下Nginx配置:

```
http{
................................
	proxy_buffer_size 128k;
	proxy_buffers   32 128k;
	proxy_busy_buffers_size 128k;
	.............................
}

```
