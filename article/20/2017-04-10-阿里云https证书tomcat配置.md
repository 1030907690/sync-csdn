---
layout:					post
title:					"阿里云https证书tomcat配置"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
阅读本文前，请先参看前文tomcat配置https_tomcat keystorefile-CSDN博客

当我们使用Java生成的证书使用https访问时会出现未认证的问题，证书风险



现在我们就申请一个阿里云云盾的免费证书

一、登录阿里云-->安全(云盾)-->证书服务->购买证书



在配置单中选择 "免费型DV SSL"   证书提供商品牌为:“赛门铁克” 注意:免费数字证书,最多保护一个明细子域名,不支持通配符，一个阿云帐户最多签发20张免费证书最后支付。

然后再点击查看



此时还未完成，需要点击补全信息，并填写相应信息。真实填写就可以了。包括：域名、姓名、邮箱等等。因为我的域名是托管到阿里云解析服务的，所以我的认证方式DNS解析认证，并勾选了发送cname。填写完成后才是“待审核”状态，等待就可以了。



10分钟左右就会收到阿里云的邮件。邮件的内容：发送给你的 主机记录和记录值。

阿里云自动的去添加了一条cname记录



大概过半个多小时后证书状态会变成已签发



这个时候就可以点进去下载证书了。选择tomcat，支持2种方式：

Tomcat支持JKS格式证书，从Tomcat7开始也支持PFX格式证书，两种证书格式任选其一，我使用的第一种方式。

文件说明：

1. 证书文件214068026470389.pem，包含两段内容，请不要删除任何一段内容。

2. 如果是证书系统创建的CSR，还包含：证书私钥文件214068026470389.key、PFX格式证书文件214068026470389.pfx、PFX格式证书密码文件pfx-password.txt。

1、证书格式转换

在Tomcat的安装目录下创建cert目录，并且将下载的全部文件拷贝到cert目录中。如果申请证书时是自己创建的CSR文件，附件中只包含214068026470389.pem文件，还需要将私钥文件拷贝到cert目录，命名为214068026470389.key；如果是系统创建的CSR，请直接到第2步。

到cert目录下执行如下命令完成PFX格式转换命令，此处要设置PFX证书密码，请牢记：

openssl pkcs12 -export -out 214068026470389.pfx -inkey 214068026470389.key -in 214068026470389.pem
2、PFX证书安装

找到安装Tomcat目录下该文件server.xml,一般默认路径都是在 conf 文件夹中。找到 <Connection port="8443" 标签，增加如下属性：

keystoreFile="cert/214068026470389.pfx"
keystoreType="PKCS12"
#此处的证书密码，请参考附件中的密码文件或在第1步中设置的密码
keystorePass="证书密码"
                    
完整的配置如下，其中port属性根据实际情况修改：


	<Connector port="443" protocol="org.apache.coyote.http11.Http11Protocol"
               maxThreads="150" SSLEnabled="true" scheme="https" secure="true"
			   keystoreFile="cert/214068026470389.pfx"
				keystoreType="PKCS12"
				keystorePass="您的证书密码"
                clientAuth="false" sslProtocol="TLS" />
重启tomcat，用https访问成功

关于异常： Connector attribute SSLCertificateFile must be defined when using SSL with APR
Tomcat提供了两个SSL实现，一个是JSSE实现，另一个是APR实现。Tomcat将自动选择使用哪个实现，即如果安装了APR则自动选择APR，否则选择JSSE。如果不希望让Tomcat自动选择，而是我们自己指定一个实现则可
通过protocol定义，如下：APR文件名为tcnative-1.dll。6.x里没这个dll文件，而7.x里有。6.x没有，6.x默认使用JSSE实现，而7.0默认使用APR实现。弄明白缘由就好办了。由于习惯使用6.0的配置方式
（即JSEE实现），因此只要把conf\server.xml里的protocol的值修改一下就行了：
 
protocol="org.apache.coyote.http11.Http11Protocol"

 


​