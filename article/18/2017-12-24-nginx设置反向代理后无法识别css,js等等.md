---
layout:					post
title:					"nginx设置反向代理后无法识别css,js等等"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
####情况如下
![这里写图片描述](https://img-blog.csdn.net/20171224165038060?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)


###目前nginx的配置：

```
server {
    listen 80;
    server_name video.xxx.cn;
    proxy_set_header Host $host:$server_port;
    proxy_set_header X-Real-Ip $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   location / {
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Real-Ip $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:8083/video;

    }


}

```

###解决办法,既然反向代理的路径下找不到文件，那么单独指定js css文件的访问路径
- 修改后的配置如下：

```
 反向代理的路径下找不到文件，需要单独指定js css文件的访问路径。
server {
    listen 80;
    server_name video.xxx.cn;
    proxy_set_header Host $host:$server_port;
    proxy_set_header X-Real-Ip $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   location / {
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Real-Ip $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:8083/video;

    }


	location ~ .*\.(js|css)$ {
             proxy_pass http://127.0.0.1:8083;
         }

}


```
