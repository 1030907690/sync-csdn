# 背景
- 使用WxJava开发包上传企微的临时素材库，传入一个url地址，这个url的https证书是使用Let's Encrypt申请，在`conn.getInputStream()`报错。
# 异常详情
- 代码和报错
```
        String url = "https://xxx/public/product/2025/05/08/21ca6b1e55d543b09974040f133ab978qlg2hm3ndb.png";
        HttpURLConnection conn = null;
        InputStream inputStream = null;
        try {
            URL remote = new URL(url);
            conn = (HttpURLConnection) remote.openConnection();
            //设置超时间为3秒
            conn.setConnectTimeout(60 * 1000);
            //防止屏蔽程序抓取而返回403错误
            conn.setRequestProperty("User-Agent", "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT; DigExt)");
            inputStream = conn.getInputStream();
        } catch (Exception e) {
            e.printStackTrace();
        }
```

```
javax.net.ssl.SSLHandshakeException: sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
	at sun.security.ssl.Alerts.getSSLException(Alerts.java:192)
	at sun.security.ssl.SSLSocketImpl.fatal(SSLSocketImpl.java:1946)
	at sun.security.ssl.Handshaker.fatalSE(Handshaker.java:316)
	...省略...

```


![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/eb920c976b9549738e26927625e2f257.png)


# 解决方案
## 方案一
- 先导出，一般是`crt`或`pem`文件
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b29267446b024314ae34cae4a19d6d0a.png)

```
keytool -import -keystore  d:/b.jks -storepass 123456 -alias alias_for_certificate -file D:\Download\_.xxxx.crt
```

- `D:\Download\_.xxxx.crt` 是导出的证书路径，`123456` 是密码，`d:/b.jks` 是希望生成的信任库文件。
- 执行命令后输入`y`
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/495af94880de42bd91d3971e34fb0fe4.png)
- 加入以下代码
```
        // 代码放到这里 可以使用相对路径
        System.setProperty("javax.net.ssl.trustStore", "d:/b.jks");
        System.setProperty("javax.net.ssl.trustStorePassword", "123456");
```
- 运行效果
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b840a12bad9642e2a2eeacb70bbbc805.png)

## 方案二
- 换一种方式下载文件，刚好项目里引入了`hutool`，换成`hutool`的`HttpUtil`工具类去下载
```
HttpUtil.downloadFile(url,"D:/");
```
- 下载成功
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/86c5ba07035742b38b97b2103a10771d.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/12f750e9a58e4618a8a762eb7f3388fe.png)

# 参考

- [https://blog.csdn.net/xuzhongyi103/article/details/131515281](https://blog.csdn.net/xuzhongyi103/article/details/131515281)