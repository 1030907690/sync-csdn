@[TOC](目录)
# 前言
- mkcert 是一个用于生成本地自签名 SSL 证书的开源工具。

# 准备工作
- 官方文档： [https://github.com/FiloSottile/mkcert](https://github.com/FiloSottile/mkcert)
- 下载地址： [https://github.com/FiloSottile/mkcert/releases](https://github.com/FiloSottile/mkcert/releases)
- 支持多种操作系统。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/27813c997f274910abcc26c82046f78e.png)
- 我下载了适应Linux系统的文件，并增加执行权限。
```bash
chmod +x mkcert-v1.4.4-linux-amd64
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/1cd7a40a4fe44e94a0c60f5beffeacb6.png)


# 生成证书文件

```shell
# 最后面是地址（域名、IP），换成自己的
/home/zzq/mkcert-v1.4.4-linux-amd64   -key-file key.pem -cert-file cert.pem 192.168.117.129
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/1b38158671ab48e7b4a85b4ab661700e.png)

# openresty配置
```bash
  server {
        listen       9527 ssl;  # 端口换成自己的
        server_name  192.168.117.129; # 换成自己的
        ssl_certificate /usr/local/openresty/nginx/cert/cert.pem;
        ssl_certificate_key /usr/local/openresty/nginx/cert/key.pem;

        location / {
            root   html;
            index  index.html index.htm;
        }
}
```

```bash
openresty -s reload
```
# 安装证书
- 此时访问会报不安全。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/249bc3f8235d44248c9fc503a7a598d5.png)
- 先安装证书，查看证书位置

```bash
  /home/zzq/mkcert-v1.4.4-linux-amd64 -install
  /home/zzq/mkcert-v1.4.4-linux-amd64  -CAROOT
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3c2a32ffa6274c35b30d80004d45831c.png)
- 下载`rootCA.pem`文件，改名为`rootCA.crt`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9adb59597d0f4573b1d126c046294dc0.png)
- 双击开始安装
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/40d311ce03a349b180fb168cead443ef.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/03c9b4c5754c4ca9926baa100b09fba2.png)

# 验证
- 清除缓存后，再次访问，连接安全。如下图所示表示成功。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e9631c7de2664f0e9cde662e57b2c6b5.png)

# 参考

- [https://www.cnblogs.com/xjzyy/p/17553820.html](https://www.cnblogs.com/xjzyy/p/17553820.html)
- [https://cloud.tencent.com/developer/article/2191830](https://cloud.tencent.com/developer/article/2191830)