---
layout:					post
title:					"mysql cluster集群搭建"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
mysql cluster集群概述
MySQL Cluster 是MySQL 适合于分布式计算环境的高实用、可拓展、高性能、高冗余版本，其研发设计的初衷就是要满足许多行业里的最严酷应用要求，这些应用中经常要求数据库运行的可靠性要达到99.999%。MySQL Cluster允许在无共享的系统中部署“内存中”数据库集群，通过无共享体系结构，系统能够使用廉价的硬件，而且对软硬件无特殊要求。此外，由于每个组件有自己的内存和磁盘，不存在单点故障。
实际上，MySQL集群是把一个叫做NDB的内存集群存储引擎集成与标准的MySQL服务器集成。它包含一组计算机，每个都跑一个或者多个进程，这可能包括一个MySQL服务器，一个数据节点，一个管理服务器和一个专有的一个数据访问程序。

MySQL Cluster能够使用多种故障切换和负载平衡选项配置NDB存储引擎，但在Cluster 级别上的存储引擎上做这个最简单。以下为MySQL集群结构关系图



MySQL从结构看，由3类节点(计算机或进程)组成，分别是：
管理节点:用于给整个集群其他节点提供配置、管理、仲裁等功能。理论上通过一台服务器提供服务就可以了。
数据节点:MySQL Cluster的核心，存储数据、日志，提供数据的各种管理服务。2个以上 时就能实现集群的高可用保证，DB节点增加时，集群的处理速度会变慢。
SQL节点(API):用于访问MySQL Cluster数据，提供对外应用服务。增加 API 节点会提高整个集群的并发访问速度和整体的吞吐量，该节点 可以部署在Web应用服务器上，也可以部署在专用的服务器上，也开以和DB部署在 同一台服务器上。

NDB引擎

MySQL Cluster 使用了一个专用的基于内存的存储引擎——NDB引擎，这样做的好处是速度快， 没有磁盘I/O的瓶颈，但是由于是基于内存的，所以数据库的规模受系统总内存的限制， 如果运行NDB的MySQL服务器一定要内存够大，比如4G, 8G, 甚至16G。NDB引擎是分布式的，它可以配置在多台服务器上来实现数据的可靠性和扩展性，理论上 通过配置2台NDB的存储节点就能实现整个数据库集群的冗余性和解决单点故障问题。
缺陷

基于内存，数据库的规模受集群总内存的大小限制
基于内存，断电后数据可能会有数据丢失，这点还需要通过测试验证。
多个节点通过网络实现通讯和数据同步、查询等操作，因此整体性受网络速度影响，因此速度也比较慢

优点

多个节点之间可以分布在不同的地理位置，因此也是一个实现分布式数据库的方案。
扩展性很好，增加节点即可实现数据库集群的扩展。
冗余性很好，多个节点上都有完整的数据库数据，因此任何一个节点宕机都不会造成服务中断。
实现高可用性的成本比较低，不象传统的高可用方案一样需要共享的存储设备和专用的软件才能实现，NDB 只要有足够的内存就能实现

环境准备：

数据节点：192.168.16.135 192.168.16.136
SQL节点：192.168.16.137 192.168.16.138
管理节点：192.168.16.130
(如果你不是root用户运行，下面命令就加下sudo)

一、下载、安装
官网的下载地址 https://dev.mysql.com/downloads/cluster/  官网要登陆，我在其他网站下载的
其他网站下载地址 http://mirror.cogentco.com/pub/mysql/
http://mirror.cogentco.com/pub/mysql/MySQL-Cluster-7.3/mysql-cluster-gpl-7.3.8-linux-glibc2.5-i686.tar.gz
解压：
tar -zxvf mysql-cluster-gpl-7.3.8-linux-glibc2.5-i686.tar.gz
 

二、配置
1、管理节点配置


将MySQL集群软件拷贝到管理节点的/usr/local目录下并解压为mysql，MySQLCluster管理节点默认是要安装在/usr/local下的，否则启动会报错

[zzq@weekend110 local]$ mv mysql-cluster-gpl-7.3.8-linux-glibc2.5-i686/ mysql
关闭安全策略

关闭iptables防火墙(或者打开防火墙的1186、3306端口)，在Shell中运行以下命令：

    

chkconfig --level 35 iptables off 
关闭SELinux，在Shell中运行以下命令：
将config文件中的SELINUX项改为disabled，修改后的config文件的内容如下：

vi /etc/selinux/config 
         # This file controls the state of SELinux on the system. 
 
	# SELINUX= can take one of these three values: 
	 
	# enforcing - SELinux security policy is enforced. 
	 
	# permissive - SELinux prints warnings instead of enforcing. 
	 
	# disabled - No SELinux policy is loaded. 
	 
	SELINUX=disabled 
	 
	# SELINUXTYPE= can take one of these two values: 
	 
	# targeted - Targeted processes are protected, 
	 
	# mls - Multi Level Security protection. 
	 
	SELINUXTYPE=targeted 
最后重启系统

配置config.ini配置文件

	[zzq@weekend110 local]$ sudo mkdir /var/lib/mysql-cluster 
	[zzq@weekend110 local]$ cd /var/lib/mysql-cluster 
	[zzq@weekend110 mysql-cluster]$ vi config.ini
配置文件config.ini内容如下：

	[ndbd default] 

	NoOfReplicas=2  #定义在Cluster环境中复制份数
	 
	DataMemory=80M #分配的数据内存大小，根据本机服务器内存适量来分配，实际运用中需要分配很大
	 
	IndexMemory=18M #设定用于存放索引（非主键）数据的内存段大小
	 
	[ndb_mgmd]  
	 
	NodeId=1 #管理节点
	 
	hostname=192.168.16.130 
	 
	datadir=/var/lib/mysql-cluster #确定该目录存在
	 
	[ndbd] 
	 
	NodeId=2 #数据节点 1
	 
	hostname=192.168.16.135 
	 
	datadir=/usr/local/mysql/data #确定该目录存在
	 
	[ndbd] 
	 
	NodeId=3 #数据节点 2
	 
	hostname=192.168.16.136 
	 
	datadir=/usr/local/mysql/data #确定该目录存在
	 
	[mysqld] 
	 
	NodeId=4 #sql节点 1
	 
	hostname=192.168.16.137 
	 
	[mysqld] 
	 
	NodeId=5 #sql节点 2
	 
	hostname=192.168.16.138
安装管理节点，不需要mysqld二进制文件，只需要MySQL Cluster服务端程序(ndb_mgmd)和监听客户端程序(ndb_mgm)。在shell中运行以下命令：
 

	cp /usr/local/mysql/bin/ndb_mgm* /usr/local/bin 
	cd /usr/local/bin 
	chmod +x ndb_mgm* 

将mysql远程拷贝到其他节点

2、配置数据结点(192.168.16.135、192.168.16.136)

	groupadd mysql 
	useradd -g mysql mysql

配置my.cnf配置文件

	vi /etc/my.cnf
	
	[mysqld] 
	 
	basedir=/usr/local/mysql 
	 
	datadir=/usr/local/mysql/data 
	 
	socket=/usr/local/mysql/sock/mysql.sock 
	 
	user=mysql 
	 
	# Disabling symbolic-links is recommended to prevent assorted security risks 
	 
	symbolic-links=0 
	 
	[mysqld_safe] 
	 
	log-error=/var/log/mysqld.log 
	 
	pid-file=/var/run/mysqld/mysqld.pid 
	 
	[mysql_cluster] 
	 
	ndb-connectstring=192.168.16.130
创建系统数据库

	cd /usr/local/mysql 
 
	mkdir sock 
	 
	scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data 



设置数据目录

	
	chown -R root . 
 
	chown -R mysql.mysql /usr/local/mysql/data 
	 
	chown -R mysql.mysql /usr/local/mysql/sock 
	 
	chgrp -R mysql .
配置MySQL服务

	cp support-files/mysql.server /etc/rc.d/init.d/ 
 
	chmod +x /etc/rc.d/init.d/mysql.server 
	 
	chkconfig --add mysql.server 
3、配置SQL结点(192.168.16.137、192.168.16.138)

添加mysql组和用户

	groupadd mysql 
	useradd -g mysql mysql
配置my.cnf配置文件

vi /etc/my.cnf
配置文件my.cnf的内容如下：

	[client] 
	 
	socket=/usr/local/mysql/sock/mysql.sock 
	 
	[mysqld] 
	 
	ndbcluster 
	 
	datadir=/usr/local/mysql/data 
	 
	socket=/usr/local/mysql/sock/mysql.sock 
	 
	ndb-connectstring=192.168.16.130 
	 
	[mysql_cluster] 
	 
	ndb-connectstring=192.168.16.130

创建系统数据库

	cd /usr/local/mysql 
 
	mkdir sock 
	 
	scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data 
设置数据目录

	chown -R root . 
 
	chown -R mysql.mysql /usr/local/mysql/data 
	 
	chown -R mysql.mysql /usr/local/mysql/sock 
	 
	chgrp -R mysql . 
配置MySQL服务

	cp support-files/mysql.server /etc/rc.d/init.d/ 
 
	chmod +x /etc/rc.d/init.d/mysql.server 
	 
	chkconfig --add mysql.server 

三、启动

启动管理结点

	ndb_mgmd -f /var/lib/mysql-cluster/config.ini 

启动数据结点
首次启动，则需要添加--initial参数，以便进行NDB节点的初始化工作。在以后的启动过程中，则是不能添加该参数的，否则ndbd程序会清除在之前建立的所有用于恢复的数据文件和日志文件。

	/usr/local/mysql/bin/ndbd --initial 
如果不是首次启动，则执行下面的命令。

	/usr/local/mysql/bin/ndbd 
如果出现
 

	[zzq@weekend112 mysql]$ /usr/local/mysql/bin/ndbd --initial 
	2017-02-13 09:03:02 [ndbd] INFO     -- Angel connected to '192.168.16.130:1186'
	2017-02-13 09:03:02 [ndbd] INFO     -- Angel allocated nodeid: 3
	2017-02-13 09:03:02 [ndbd] ERROR    -- Couldn't start as daemon, error: 'Failed to open logfile '/usr/local/mysql/data/ndb_3_out.log' for write, errno: 13'
这样的异常给当前用户增加权限

	sudo chmod -R 777 /usr/local/mysql/
启动SQL结点

若MySQL服务没有运行，则在shell中运行以下命令：

	/usr/local/mysql/bin/mysqld_safe --user=mysql & 
启动测试
查看管理节点，启动成功
 

四、集群测试

1. 测试一

现在我们在其中一个SQL结点上进行相关数据库的创建,然后到另外一个SQL结点上看看数据是否同步。

在SQL结点1(192.168.16.137)上执行：

	[zzq@weekend113 ~]$ /usr/local/mysql/bin/mysql -u root -p 
	Enter password: 
	Welcome to the MySQL monitor.  Commands end with ; or \g.
	Your MySQL connection id is 3
	Server version: 5.6.22-ndb-7.3.8-cluster-gpl MySQL Cluster Community Server (GPL)

	Copyright (c) 2000, 2015, Oracle and/or its affiliates. All rights reserved.

	Oracle is a registered trademark of Oracle Corporation and/or its
	affiliates. Other names may be trademarks of their respective
	owners.

	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

	mysql> show database;
	ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'database' at line 1
	mysql> show databases;
	+--------------------+
	| Database           |
	+--------------------+
	| information_schema |
	| mysql              |
	| ndbinfo            |
	| performance_schema |
	| test               |
	+--------------------+
	5 rows in set (0.03 sec)

	mysql> create database ecshop;
	Query OK, 1 row affected (0.17 sec)

	mysql> use ecshop
	Database changed
	mysql> CREATE TABLE ctest2 (i INT) ENGINE=NDB; //这里必须指定数据库表的引擎为NDB,否则同步失败 
	Query OK, 0 rows affected (0.26 sec)

	mysql> INSERT INTO ctest2 () VALUES (1); 
	Query OK, 1 row affected (0.00 sec)

	mysql>  SELECT * FROM ctest2;
	+------+
	| i    |
	+------+
	|    1 |
	+------+
	1 row in set (0.02 sec)

	mysql> 
然后在SQL结点2上看数据是否同步过来了


经过测试，在非master上创建数据，可以同步到master上


查看表的引擎是不是NDB，>show create table 表名;

验证

	[zzq@weekend114 ~]$ /usr/local/mysql/bin/mysql -u root -p 
	Enter password: 
	Welcome to the MySQL monitor.  Commands end with ; or \g.
	Your MySQL connection id is 2
	Server version: 5.6.22-ndb-7.3.8-cluster-gpl MySQL Cluster Community Server (GPL)

	Copyright (c) 2000, 2015, Oracle and/or its affiliates. All rights reserved.

	Oracle is a registered trademark of Oracle Corporation and/or its
	affiliates. Other names may be trademarks of their respective
	owners.

	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

	mysql> show databases;
	+--------------------+
	| Database           |
	+--------------------+
	| information_schema |
	| ecshop             |
	| mysql              |
	| ndbinfo            |
	| performance_schema |
	| test               |
	+--------------------+
	6 rows in set (0.02 sec)

	mysql> use ecshop
	Reading table information for completion of table and column names
	You can turn off this feature to get a quicker startup with -A

	Database changed
	mysql> show tables;
	+------------------+
	| Tables_in_ecshop |
	+------------------+
	| ctest2           |
	+------------------+
	1 row in set (0.00 sec)

	mysql>  SELECT * FROM ctest2;
	+------+
	| i    |
	+------+
	|    1 |
	+------+
	1 row in set (0.01 sec)

	mysql> 

结果是正确的。

2. 测试二

关闭一个数据节点 ，在另外一个节点写输入，开启关闭的节点，等会儿再关闭最开始未关闭的那个节点，看数据是否同步过来。
首先把数据结点1关闭，然后在结点2上添加数据
在SQL结点2(192.168.16.138)上操作如下：

	mysql> INSERT INTO ctest2 () VALUES (3333); 
	再启动节点1，再关闭节点2，再去查询
	 mysql>  SELECT * FROM ctest2;
	+------+
	| i    |
	+------+
	| 3333 |
	|    1 |
	+------+
	2 rows in set (0.00 sec)

可以看到数据已经同步过来了，说明数据可以双向同步了。



​