---
layout:					post
title:					"nginx反向代理后webSocket拿不到真实ip"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
>- 1、场景：nginx反向代理后使用 WebSocketSession 里面 webSocketSession.getRemoteAddress().getHostString()方法经过了Nginx反向代理后得到的ip地址是127.0.0.1(就是Nginx反向代理的地址)。在本地测试过直接使用Tomcat是能够拿到真实IP的。
>- 2、解决方案
Nginx配置：

```
server {  
    listen 8080;   
    server_name 192.168.0.134 ;  

     location / {  
        proxy_set_header Host $host:$server_port;    
        proxy_set_header X-Real-Ip $remote_addr;    
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  
		proxy_http_version 1.1;
		proxy_set_header Upgrade $http_upgrade;
		proxy_set_header Connection "upgrade";
        proxy_pass http://127.0.0.1:8085;
    }  

	
}
```
> proxy_http_version 1.1;
		proxy_set_header Upgrade $http_upgrade;
		proxy_set_header Connection "upgrade"; 
		是专门针对WebSocket配置的,具体可查看Nginx官方文档[Nginx关于WebSocket的配置](http://nginx.org/en/docs/http/websocket.html)

 

>- 3、重点在Tomcat的配置`server.xml` 具体可查阅[http://tomcat.apache.org/tomcat-8.0-doc/api/org/apache/catalina/valves/RemoteIpValve.html](http://tomcat.apache.org/tomcat-8.0-doc/api/org/apache/catalina/valves/RemoteIpValve.html),增加如下配置



 
 

```
Nginx增加以下配置 
proxy_set_header Host $host:$server_port; 非80端口 ，用80端口时 不需要$server_port 
proxy_set_header X-Real-IP $remote_addr; 非必须，添加此项之后可以在代码中通过request.getHeader("X-Real-IP")获取ip
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
proxy_set_header X-Forwarded-Proto $scheme; 
  
<Engine name="Catalina" defaultHost="localhost"> 
<Valve className="org.apache.catalina.valves.RemoteIpValve" 
remoteIpHeader="X-Forwarded-For" 
protocolHeader="X-Forwarded-Proto" 
protocolHeaderHttpsValue="https" httpsServerPort="443"/> 非80端口时，必须增加httpsServerPort配置，不然request.getServerPort()方法返回 443. 
```
>此时经过反向代理到Tomcat就能获取到真实IP了。
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/53acbda4063a14101f04c249e1a30aa6.png)

 

 
