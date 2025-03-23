---
layout:					post
title:					"tomcat配置https"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
一、创建生产密钥和证书

Tomcat 目前只能操作 JKS、PKCS11、PKCS12 格式的密钥存储库。JKS 是 Java 标准的“Java 密钥存储库”格式，是通过 keytool 命令行工具创建的。该工具包含在 JDK 中。PKCS12 格式一种互联网标准，可以通过 OpenSSL 和 Microsoft 的 Key-Manager 来。

   命令创建

"%JAVA_HOME%\bin\keytool" -genkey -alias tomcat -keyalg RSA
JAVA_HOME是已经配置好的Java环境变量



该命令将在用户的主目录下创建一个新文件：.keystore，如果你想要想指定一个不同的位置或文件名，可以在上述的 keytool 命令上添加 -keystore 参数，后跟到达 keystore 文件的完整路径名。

"%JAVA_HOME%\bin\keytool" -genkey -alias tomcat -keyalg RSA -keystore c:/keystore
二、修改tomcat配置

打开/conf/server.xml 文件找到这样的内容

<!--
    <Connector port="8443" protocol="org.apache.coyote.http11.Http11Protocol"
               maxThreads="150" SSLEnabled="true" scheme="https" secure="true"
               clientAuth="false" sslProtocol="TLS" />
    -->

复制一份下来，把注释去掉port默认是8443，但是对于SSL标准端口号是443，这样在访问网页的时候，直接使用https而不需要输入端口号就可以访问，如https://loalhost/web

<Connector port="80" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="443" />

把 redirectPort改为443

SSL HTTP/1.1 Connector定义的地方，也修改端口号为：443，加入了keystoreFile="${user.home}/.keystore" keystorePass="这是tomcat密钥口令"

	<Connector port="443" protocol="org.apache.coyote.http11.Http11Protocol"
               maxThreads="150" SSLEnabled="true" scheme="https" secure="true"
			   keystoreFile="${user.home}/.keystore" keystorePass="这是tomcat密钥口令"
               clientAuth="false" sslProtocol="TLS" />

还有一个

<!-- Define an AJP 1.3 Connector on port 8009 -->
    <Connector port="8009" protocol="AJP/1.3" redirectPort="443" />

然后启动tomcat，就可以用https去访问了

若想把所有 HTTP 请求都转到 HTTPS 协议上，可以修改tomcat的conf下的web.xml，在节点下方 添加如下：

<security-constraint>  
	<!-- Authorization setting for SSL --> 
	<web-resource-collection >  
		<web-resource-name >SSL</web-resource-name>  
		<url-pattern>/*</url-pattern>  
	</web-resource-collection>  
	<user-data-constraint>  
		<transport-guarantee>CONFIDENTIAL</transport-guarantee>  
	</user-data-constraint>  
</security-constraint>


​