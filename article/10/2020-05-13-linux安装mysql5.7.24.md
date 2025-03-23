---
layout:					post
title:					"linux安装mysql5.7.24"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
### 下载和解压mysql
- 下载地址[https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/) ；存档下载地址： [https://downloads.mysql.com/archives/community/](https://downloads.mysql.com/archives/community/)

```bash
wget https://cdn.mysql.com/archives/mysql-5.7/mysql-5.7.24-linux-glibc2.12-x86_64.tar.gz
```
或者

```java
wget -O mysql-5.7.24-linux-glibc2.12-x86_64.tar.gz https://sourceforge.net/projects/generic-software/files/mysql/mysql-5.7.24-linux-glibc2.12-x86_64.tar.gz/download
```


```bash
tar -zxvf mysql-5.7.24-linux-glibc2.12-x86_64.tar.gz
```

```bash
 mv mysql-5.7.24-linux-glibc2.12-x86_64 /usr/local/mysql
```
### 初始化
- 在mysql下添加data目录

```bash
 mkdir /usr/local/mysql/data
```
- 创建用户和用户组；更改mysql目录下所有的目录及文件夹所属组和用户

```bash
groupadd mysql
useradd -r -g mysql mysql
cd /usr/local
 chown -R mysql:mysql mysql/
 chmod -R 755 mysql/
```
- 编译安装并初始化mysql，<font color="red">记住命令行末尾的密码</font>

```bash
/usr/local/mysql/bin/mysqld --initialize --user=mysql --datadir=/usr/local/mysql/data --basedir=/usr/local/mysql
```

>2020-05-13T14:04:08.052652Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2020-05-13T14:04:09.009944Z 0 [Warning] InnoDB: New log files created, LSN=45790
2020-05-13T14:04:09.129179Z 0 [Warning] InnoDB: Creating foreign key constraint system tables.
2020-05-13T14:04:09.190602Z 0 [Warning] No existing UUID has been found, so we assume that this is the first time that this server has been started. Generating a new UUID: 9d7da7a0-9522-11ea-b338-00163e154252.
2020-05-13T14:04:09.192264Z 0 [Warning] Gtid table is not ready to be used. Table 'mysql.gtid_executed' cannot be opened.
2020-05-13T14:04:09.192633Z 1 [Note] A temporary password is generated for root@localhost: drFol7fayg-6


![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6ad04df320f478a9451d21183de29549.png)

### 启动

```bash
/usr/local/mysql/support-files/mysql.server start
```
- 启动可能报错`Starting MySQL.The server quit without updating PID file (/[FAILED]mysql/test.pid)` ;一定要把`/etc/my.cnf`改个名字或者删除掉；报这个错也可能是权限问题。

- 还可以添加到服务，设置开机自启动

```bash
cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql
chmod +x /etc/init.d/mysql 
#把mysql注册为开机启动的服务
chkconfig --add mysql  

#查看是否添加成功
chkconfig --list mysql  


```
- 其他命令

```bash
#其他命令
#启动mysql
service mysql start
#停止mysql
service mysql stop
#重启mysql
service mysql restart
```

### 使用mysql
- 登录进去，要使用开始生成的密码，比如我这里是`drFol7fayg-6`

```bash
cd /usr/local/mysql
./bin/mysql -u root -p
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8f6c65732ef8267eb3d34c083d42f9c4.png)
- 登录进去一般就是修改密码

```bash
#修改为root
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
Query OK, 0 rows affected (0.00 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)

```
- 无需重启，用新密码再次登录就可以了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1f7b8f61e612494fccbb16ec27ee4e7b.png)
- 开启mysql远程访问

```bash
use mysql;
grant all privileges on *.* to 'root'@'%' identified by 'root' with grant option;
FLUSH PRIVILEGES;
```

### 增加配置文件my.cnf
- vim /usr/local/mysql/my.cnf
```bash
[mysqld]
port = 3306
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
#这个配置只能本机连接   如果要开启外部访问可以写)0.0.0.0
bind-address = 127.0.0.1
#设置东八区时区  MySQL默认的时区是UTC时区  否则代码连接可能报 Could not create connection to database server. Attempted reconnect 3 times. (url拼接serverTimezone=UTC参数也能解决这个报错)
default-time-zone='+08:00'
... 后面的参数省略，如果只是测试运行，就这4行也行 ...
```
- 配置完成后重启即可
