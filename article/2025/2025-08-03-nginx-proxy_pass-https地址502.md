
@[TOC](目录)
# 背景
- 我是测试环境(是`http`地址)，如果遇到`/custom_api/`的地址代理到另一个`https`的地址。
# 遇到的问题
- 我发现用http地址ip:端口是通的，但是https地址不行报502，错误日志如下：
>*2650 SSL_do_handshake() failed (SSL: error:0A000458:SSL routines::tlsv1 unrecognized name:SSL alert number 112) while SSL handshaking to upstream

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3c4cbafb03504c669429a9be13ce7ca3.png)
# 解决方案

- 搜索后发现主要与`https`、`Host`有关，我改成如下配置代理成功。

```bash
      location /custom_api/ {
		   proxy_pass https://xxx.top;
		   resolver 8.8.8.8;
		   proxy_ssl_server_name on;
		   client_max_body_size  1024m;
		   #proxy_set_header Host $host;
		    # 这里要改Host, 与目标地址服务监听的Host有关
			proxy_set_header Host xxx.top;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header X-Forwarded-Proto $scheme;
			proxy_set_header Upgrade $http_upgrade;
			proxy_set_header Connection "upgrade";
			proxy_http_version 1.1;
			proxy_cache_bypass $http_upgrade;
    }

```
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/29eabe054e6e498aa15809008d6f694c.png)

 

# 参考
- [https://kebingzao.com/2022/08/16/nginx-502/](https://kebingzao.com/2022/08/16/nginx-502/)