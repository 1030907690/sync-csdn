---
layout:					post
title:					"elk采集java程序的日志(logback)-分割message字段"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)

### 接上篇[elk采集java程序的日志(logback)](https://blog.csdn.net/baidu_19473529/article/details/103028769)
- 在上篇中我的message字段是:`message:2019-11-12 15:21:22#-#111111#-#hello`;现在我想要的是做一个更详细的分类,根据#-#,把这个message字段拆分成更多的字段。
### logstash配置
-  vim logstash-tomcat-access-log.conf

 

```bash
input {
	tcp{
		port => 9601
		mode => "server"
		codec => json_lines
	}
}




filter {
	mutate { #使用mutate插件
	split => ["message","#-#"]
	add_field =>   {
		"temp1" => "%{[message][0]}"
	}
	add_field =>   {
		"temp2" => "%{[message][1]}"
	}
	add_field =>   {
		"temp3" => "%{[message][2]}"
	}

}
}
output {
	elasticsearch {
		hosts => ["192.168.137.137:9200"]
		index => "logstash-tomcat-log"
	}
	stdout{
		codec => rubydebug
	}
}

```
- 然后启动logstash
### 验证效果
- 访问接口
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2b432dd393936956f0a21cb4ddf0aa90.png)
- logstash日志
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c5b4d701d425fd85e917ee2e785cad84.png)
- kibana展示
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/27ebfe01bd6f9204c554a08bb114cc27.png)
- 还有个问题，就是现在temp1、temp2、temp3没有索引的是?问号不能用于visualize和discover的搜索。要到这里(Management -> Index Patterns -> 点击你的某个索引)点击刷新下才能出来temp1、temp2、temp3的索引。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/495203757c61b221404eb6dae794c0bd.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e2ec617c0a8c12e055f6fd8731618286.png)
- 测试到分割是成功的；如果文章有错误的地方，希望批评指出，感谢您的观看。