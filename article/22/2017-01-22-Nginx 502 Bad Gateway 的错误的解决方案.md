---
layout:					post
title:					"Nginx 502 Bad Gateway 的错误的解决方案"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
我用的是nginx反向代理Apache，直接用Apache不会有任何问题，加上nginx就会有部分ajax请求502的错误，下面是我收集到的解决方案。

一、fastcgi缓冲区设置过小

出现错误，首先要查找nginx的日志文件，目录为/var/log/nginx，在日志中发现了如下错误

2013/01/17 13:33:47 [error] 15421#0: *16 upstream sent too big header while reading response header from upstream
大意是nginx缓冲区有一个bug造成的,我们网站的页面消耗占用缓冲区可能过大。网上查找了一下解决方法，在国外网站看到了一个增加缓冲区的方法，彻底解决了Nginx 502 Bad

Gateway的问题。方法如下：

http {
    ...
    fastcgi_buffers 8 16k;
    fastcgi_buffer_size 32k;
    ...
}
可根据服务器已经网站的情况自行增大上述两个配置项。

二、代理缓冲区设置过小

如果你使用的是nginx反向代理，如果header过大，超出了默认的1k，就会引发上述的upstream sent too big header （说白了就是nginx把外部请求给后端处理，后端返回的header太大，nginx处理不过来就会导致502。
(我自己的就是这个问题)

server {  
    listen 80;   
    server_name shop.xxx.com;  
     proxy_set_header Host $host:$server_port;    
    proxy_set_header X-Real-Ip $remote_addr;    
    proxy_set_header X-Forwarded-For $remote_addr;   
   
    location / {  
	#这三行 start
	proxy_buffer_size 64k;
	proxy_buffers   32 32k;
	proxy_busy_buffers_size 128k;
	#这三行 end
        proxy_set_header Host $host:$server_port;    
        proxy_set_header X-Real-Ip $remote_addr;    
        proxy_set_header X-Forwarded-For $remote_addr;   
        proxy_pass http://127.0.0.1:82;  
          
    }  
      
}  

三、默认php-cgi的进程数设置过少

在安装好使用过程中出现502问题，一般是因为默认php-cgi进程是5个，可能因为phpcgi进程不够用而造成502，需要修改/usr/local/php/etc/php-fpm.conf 将其中的max_children值适当增加。也有可能是max_requests值不够用。需要说明的是这连个配置项占用内存很大，请根据服务器配置进行设置。否则可能起到反效果。

四、php执行超时

php执行超时，修改/usr/local/php/etc/php.ini 将max_execution_time 改为300（这种概率很小）

五、nginx等待时间超时

部分PHP程序的执行时间超过了Nginx的等待时间，可以适当增加nginx.conf配置文件中FastCGI的timeout时间

http  {
  fastcgi_connect_timeout 300;
  fastcgi_send_timeout 300;
  fastcgi_read_timeout 300;
  ......
  }
六、被代理的服务无法响应或者已停止

如下配置,如果http://192.168.16.129:80服务无法响应或者已停止也会报502








希望我收集的能给大家一些帮助

​