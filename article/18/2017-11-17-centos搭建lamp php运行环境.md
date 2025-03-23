---
layout:					post
title:					"centos搭建lamp php运行环境"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
###lamp：Linux+Apache+MySql+PHP，是一个在Linux上执行php程序比较通用的运行环境

###一、安装前准备：
	- 1、保证电脑是联网的
	- 2、可以使用yum

###二、安装
- 我们直接使用yum很方便，它可以解决包的依赖关系，我还在后面加了postgresql数据库如果不需要的话可以去掉和postgresql的参数
	

```
yum -y install httpd mysql mysql-server php php-mysql postgresql postgresql-server php-postgresql php-pgsql php-devel
```
![这里写图片描述](https://img-blog.csdn.net/20171117213108441?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

	这个过程大概需要几分钟，等待完成。


   - 完成后，我们可以测试一下Apache和php解析模块是否安装成功了是否安装成功了；
    - 启动
     `/etc/init.d/httpd start`
 
    - 检查结果
     `ps -ef |  grep httpd `
	 ![这里写图片描述](https://img-blog.csdn.net/20171117214140151?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
	 
    - Apache其他操作命令
```
/etc/init.d/httpd stop  #关闭
/etc/init.d/httpd restart  #重启
```

- 接下来进入网站根目录(默认的路径为/var/www/html)新建一个phpinfo.php的程序，用于查看php相关配置信息。
 - 到/var/www/html 创建phpinfo.php文件
```
vi phpinfo.php
```

	  	 文件内容
```
<?php
phpinfo();
?>
```

- 保存后，记得关闭防火墙或者开发80端口，Apache默认监听的80端口,然后ip/phpinfo.php访问。

![这里写图片描述](https://img-blog.csdn.net/20171117215101381?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
   
- 出现这样的界面就是成功的了。

- 下一步就是配置mysql了。
  

```
[root@localhost html]# /etc/init.d/mysqld start #开启mysql
Starting mysqld:                                           [  OK  ]

```

```
[root@localhost html]# lsof -i:3306  #查看是否启动成功或者用 netstat -tulnp | grep :3306
COMMAND  PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
mysqld  2608 mysql   10u  IPv4  22286      0t0  TCP *:mysql (LISTEN)

```
```
[root@localhost html]#  mysqladmin -u root password 'root' #首次安装无密码，设置密码
```
- 登录进去创建一个database
`mysql> create database newTest;
Query OK, 1 row affected (0.01 sec)
`
![这里写图片描述](https://img-blog.csdn.net/20171117220054846?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

- 最后编写一个连接数据库的测试代码，写在phpinfo.php里面
  - 先往数据库添加点数据
  

```
use newTest;
create table test(name varchar(10));
insert into test values('zs');
insert into test values('ls');
```

phpinfo.php源码

```
<?php
$mysql_server_name='localhost'; //改成自己的mysql数据库服务器

$mysql_username='root'; //改成自己的mysql数据库用户名

$mysql_password='root'; //改成自己的mysql数据库密码

$mysql_database='newTest'; //改成自己的mysql数据库名

$conn = mysql_connect($mysql_server_name,$mysql_username,$mysql_password) or die("error connecting") ; //连接数据库

mysql_query("set names 'utf8'"); //数据库输出编码 应该与你的数据库编码保持一致.南昌网站建设公司百恒网络PHP工程师建议用UTF-8 国际标准编码.

mysql_select_db($mysql_database); //打开数据库
$sql ="select * from test "; //SQL语句

$result = mysql_query($sql,$conn); //查询

while($row = mysql_fetch_array($result))

{

echo "<div style=\"height:24px; line-height:24px; font-weight:bold;\">"; //排版代码

echo $row['name'] . "<br/>";

echo "</div>"; //排版代码

}

phpinfo();
?>

```

![这里写图片描述](https://img-blog.csdn.net/20171117221531301?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 - 这样整个环境就算搭建完成了。

需要特别注意的是如果你的系统是centos7.0或者Redhat7.0及以上系统，使用yum安装mysql是失败的，原因是CentOS7版本将MySQL数据库软件从默认的程序列表中移除，用mariadb代替了。有两个办法可以解决问题。

####方式一、安装mariadb
- MariaDB数据库管理系统是MySQL的一个分支，主要由开源社区在维护，采用GPL授权许可。开发这个分支的原因之一是：甲骨文公司收购了MySQL后，有将MySQL闭源的潜在风险，因此社区采用分支的方式来避开这个风险。MariaDB的目的是完全兼容MySQL，包括API和命令行，使之能轻松成为MySQL的代替品
```
yum install mariadb-server mariadb  #使用yum就可以安装了
```
  - mariadb数其他相关命令：
```
 systemctl start mariadb  #启动MariaDB

systemctl stop mariadb  #停止MariaDB

systemctl restart mariadb  #重启MariaDB

systemctl enable mariadb  #设置开机启动
```
- 启动过后，你也同样可以向之前一样mysql -u root -p登录进去操作mysql数据库

###方式二、下载官方的mysql安装包
- 下载地址https://dev.mysql.com/downloads/mysql/

![这里写图片描述](https://img-blog.csdn.net/20171117222747387?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

- 这里可以选择你想要的系统和版本。后面是一样的。