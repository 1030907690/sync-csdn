---
layout:					post
title:					"nginx使用include实现多域名访问"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
在nginx.conf中加入

http的括号里面

include  host/*.conf;

路径是在conf文件下新增host文件里面存放多个域名的配置：如下shop.conf

 server {
	listen 80; 
	server_name shop.xxx.com;
	 proxy_set_header Host $host:$server_port;  
	proxy_set_header X-Real-Ip $remote_addr;  
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
 
	location / {
		proxy_set_header Host $host:$server_port;  
		proxy_set_header X-Real-Ip $remote_addr;  
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_pass http://101.xxx.182.5:8084;
		 
		
	}
	
}


​