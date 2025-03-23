---
layout:					post
title:					"nginx代理无法携带Cookie，导致session丢失引发的“惨案”"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 项目是前后端分离，前端用的react打包后的nginx配置如下：

```
        location /xxx{
            gzip off;
            try_files $uri /xxx/index.html;
        }
```
- 代理到server端nginx配置如下：

```
       location /xxx/service/ {
			gzip off;
			proxy_set_header Host $http_host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		    proxy_pass http://127.0.0.1:8083/service/;  
			expires -1;
			proxy_redirect http:// https://;
        }
```
- 登录成功了请求一直不带cookie,后端就一直判断是没登录
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7974d715e21a384840fde197959acb60.png)
- 解决办法：加上`proxy_cookie_path /service/ /;` 如下配置：

```
     location /xxx/service/ {
			gzip off;
			proxy_set_header Host $http_host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		    proxy_pass http://127.0.0.1:8083/service/;   #可能是 /itrip/service/ /service/路径不一致，以前直接ip+端口是不会有这种问题的
			expires -1;
			proxy_redirect http:// https://;
			proxy_cookie_path /service/ /; #这段设置cookie路径，/service/与proxy_pass后缀对应，后面的我直接设置成根路径/
        }
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/baf13032f1ebcda0473df14946bcd319.png)
- 参考 [https://www.jb51.net/article/185661.htm](https://www.jb51.net/article/185661.htm)