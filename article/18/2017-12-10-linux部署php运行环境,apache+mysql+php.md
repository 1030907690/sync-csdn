---
layout:					post
title:					"linux部署php运行环境,apache+mysql+php"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- linux(我用的是centos7)上非集成环境的部署php运行环境坑比较多,现在我把我安装的步骤整理一下。

###一、安装前的准备
- 需要的一些软件包：
	- apache 下载地址	http://httpd.apache.org/download.cgi#apache24 
	- apr  (apache需要的依赖)	下载地址	http://apr.apache.org/download.cgi
	- apr-util (apache需要的依赖) 下载地址 http://apr.apache.org/download.cgi
	- pcre	(apache需要的依赖)  下载地址 https://sourceforge.net/projects/pcre/files/pcre/
	- php			下载地址	http://www.php.net/downloads.php
	- libxml2 (php需要的依赖) 	http://xmlsoft.org/sources/(这个也可以直接yum安装的)
	- mysql的安装包 https://dev.mysql.com/downloads/mysql/


###二、安装Apache模块
- 先卸载系统自带的apr 不然会报这种奇怪的错误/usr/local/apr/lib/libaprutil-1.so: undefined reference to `XML_GetErrorCode'
	rpm -qa | grep apr
	apr-1.2.7-11
	apr-util-1.2.7-6
	

```
	rpm -e --allmatches --nodeps apr-util-1.2.7-6
```

- 安装apr和apr-util
	

```
[root@VM_0_6_centos software]# tar -zxvf apr-1.6.3.tar.gz 
[root@VM_0_6_centos apr-1.6.3]# ./configure --prefix=/usr/local/apr

```
可能会报错：

```
rm: cannot remove 'libtoolT': No such file or directory
config.status: executing default commands

```
解决方案：将configure文件中的$RM   "$cfgfile "这行代码注释掉就可以了
```
    #$RM "$cfgfile"
```
重新./configure --prefix=/usr/local/apr,然后

```
make && make install
```
现在开始安装apr-util:

```
[root@VM_0_6_centos software]# tar -zxvf apr-util-1.6.1.tar.gz
[root@VM_0_6_centos apr-util-1.6.1]# ./configure --prefix=/usr/local/apr-util -with-apr=/usr/local/apr #这里注意要指定刚才apr的安装路径否则报错configure: error: APR could not be located. Please use the --with-apr option.
[root@VM_0_6_centos apr-util-1.6.1]# make && make install 
```

如果apr apr-util 执行make命令时报错：
```
pr_xml.lo -c xml/apr_xml.c && touch xml/apr_xml.lo
xml/apr_xml.c:35:19: fatal error: expat.h: No such file or directory
 #include <expat.h>
                   ^
compilation terminated.
make[1]: *** [xml/apr_xml.lo] Error 1

centos或者redhat yum install expat-devel
Ubuntu ：apt-get install libexpat1-dev
```
- 安装pcre，基本步骤差不多,这里就不赘述了。

- 现在可以安装Apache模块了
 

```
[root@VM_0_6_centos software]# tar -zxvf httpd-2.4.29.tar.gz
[root@VM_0_6_centos httpd-2.4.29]# cd httpd-2.4.29/
[root@VM_0_6_centos httpd-2.4.29]# ./configure --prefix=/usr/local/apache2/  --with-apr=/usr/local/apr/ --with-apr-util=/usr/local/apr-util
[root@VM_0_6_centos httpd-2.4.29]# make && make install
```

这里的话会编译的比较久,还有可能会在编译的时候内存不足(我的虚拟主机配置比较低),如果不好升级内存，那就创建临时交换区来解决。

```
sudo dd if=/dev/zero of=/swapfile bs=64M count=16
sudo mkswap /swapfile
sudo swapon /swapfile

#编译完成后你也可以移除掉：
sudo swapoff /swapfile
sudo rm /swapfile
```

编译完后可以测试一下，默认是80端口，由于我的80端口已用我得改下配置文件

```
[root@VM_0_6_centos apache2]# vi conf/httpd.conf 
```

```
Listen 8081
```

```
#开启命令
[root@VM_0_6_centos apache2]# ./bin/apachectl
```
![这里写图片描述](https://img-blog.csdn.net/20171210160500898?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
Apache就搭建成功了
其他命令：

```
#关闭服务
[root@VM_0_6_centos apache2]# ./bin/apachectl -k  stop
```

###三、安装mysql
	
```

[root@VM_0_6_centos software]# tar -zxvf mysql-5.7.20-linux-glibc2.12-x86_64.tar.gz #解压
[root@VM_0_6_centos software]# mv mysql-5.7.20-linux-glibc2.12-x86_64 /usr/local/
[root@VM_0_6_centos local]# mv mysql-5.7.20-linux-glibc2.12-x86_64/ mysql #改名
[root@VM_0_6_centos local]# cd mysql
[root@VM_0_6_centos mysql]# mkdir data  #创建mysql数据存储目录
```

```
#建立用户mysql，组mysql。后面mysql就使用这个用户来运行（注意这也是mysql启动脚本中默认的用户，因此最好不要改名）。
groupadd mysql
useradd -r -g mysql mysql

#将mysql及其下所有的目录所有者和组均设为mysql:
[root@VM_0_6_centos mysql]# chown mysql:mysql -R .
```
 - 初始化
	 

```
#添加参数–no-defaults，进行初始化。并且，切记要放在参数的首位,否则初始化失败,不会有任何日志输出
[root@VM_0_6_centos mysql]# ./bin/mysqld --no-defaults --initialize --user=mysql --datadir=/usr/local/mysql/data --basedir=/usr/local/mysql
2017-12-10T08:50:50.917167Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2017-12-10T08:50:52.989343Z 0 [Warning] InnoDB: New log files created, LSN=45790
2017-12-10T08:50:53.291912Z 0 [Warning] InnoDB: Creating foreign key constraint system tables.
2017-12-10T08:50:53.454159Z 0 [Warning] No existing UUID has been found, so we assume that this is the first time that this server has been started. Generating a new UUID: 3ac7209f-dd87-11e7-a56c-525400a9e99c.
2017-12-10T08:50:53.472391Z 0 [Warning] Gtid table is not ready to be used. Table 'mysql.gtid_executed' cannot be opened.
2017-12-10T08:50:53.473113Z 1 [Note] A temporary password is generated for root@localhost: IX0yp5lR5U).

 #注意mysql5.7的命令不同，mysql_install_db is deprecated
```

```
[root@VM_0_6_centos mysql]# ./bin/mysqld_safe &#执行这步的是为了生成pid，当你看到以.pid ended结尾，就可以ctrl+c,而且这一步mysql已经启动了，你需要执行ps -ef|grep mysqld，然后将mysql进程kill掉，然后在进行一下命令
```


配置my.conf文件,我的mysql5.7.18 support-files下没有my-default.cnf文件，这里我找到一个模板可以改改路径就可以用

```
[client]
port = 3306
socket = /tmp/mysql.sock

[mysqld]

###############################基础设置#####################################

#Mysql服务的唯一编号 每个mysql服务Id需唯一
server-id = 1

#服务端口号 默认3306
port = 3306

#mysql安装根目录
basedir = /usr/local/mysql

#mysql数据文件所在位置
datadir = /usr/local/mysql/data

#临时目录 比如load data infile会用到
tmpdir  = /tmp

#设置socke文件所在目录
socket  = /tmp/mysql.sock

#主要用于MyISAM存储引擎,如果多台服务器连接一个数据库则建议注释下面内容
skip-external-locking

#只能用IP地址检查客户端的登录，不用主机名
skip_name_resolve = 1

#事务隔离级别，默认为可重复读，mysql默认可重复读级别（此级别下可能参数很多间隙锁，影响性能）
transaction_isolation = READ-COMMITTED

#数据库默认字符集,主流字符集支持一些特殊表情符号（特殊表情符占用4个字节）
character-set-server = utf8mb4

#数据库字符集对应一些排序等规则，注意要和character-set-server对应
collation-server = utf8mb4_general_ci

#设置client连接mysql时的字符集,防止乱码
init_connect=‘SET NAMES utf8mb4‘

#是否对sql语句大小写敏感，1表示不敏感
lower_case_table_names = 1

#最大连接数
max_connections = 400

#最大错误连接数
max_connect_errors = 1000

#TIMESTAMP如果没有显示声明NOT NULL，允许NULL值
explicit_defaults_for_timestamp = true

#SQL数据包发送的大小，如果有BLOB对象建议修改成1G
max_allowed_packet = 128M

#MySQL连接闲置超过一定时间后(单位：秒)将会被强行关闭
#MySQL默认的wait_timeout  值为8个小时, interactive_timeout参数需要同时配置才能生效
interactive_timeout = 1800
wait_timeout = 1800

#内部内存临时表的最大值 ，设置成128M。
#比如大数据量的group by ,order by时可能用到临时表，
#超过了这个值将写入磁盘，系统IO压力增大
tmp_table_size = 134217728
max_heap_table_size = 134217728

#禁用mysql的缓存查询结果集功能
#后期根据业务情况测试决定是否开启
#大部分情况下关闭下面两项
query_cache_size = 0
query_cache_type = 0

#####################用户进程分配到的内存设置BEGIN#############################

##每个session将会分配参数设置的内存大小
#用于表的顺序扫描，读出的数据暂存于read_buffer_size中，当buff满时或读完，将数据返回上层调用者
#一般在128kb ~ 256kb,用于MyISAM
#read_buffer_size = 131072
#用于表的随机读取，当按照一个非索引字段排序读取时会用到，
#一般在128kb ~ 256kb,用于MyISAM
#read_rnd_buffer_size = 262144
#order by或group by时用到

#建议先调整为2M，后期观察调整
sort_buffer_size = 2097152

#一般数据库中没什么大的事务，设成1~2M，默认32kb
binlog_cache_size = 524288

########################用户进程分配到的内存设置END############################

#在MySQL暂时停止响应新请求之前的短时间内多少个请求可以被存在堆栈中
#官方建议back_log = 50 + (max_connections / 5),封顶数为900
back_log = 130

############################日志设置##########################################

#数据库错误日志文件
log_error = error.log

#慢查询sql日志设置
slow_query_log = 1
slow_query_log_file = slow.log

#检查未使用到索引的sql
log_queries_not_using_indexes = 1

#针对log_queries_not_using_indexes开启后，记录慢sql的频次、每分钟记录的条数
log_throttle_queries_not_using_indexes = 5

#作为从库时生效,从库复制中如何有慢sql也将被记录
log_slow_slave_statements = 1

#慢查询执行的秒数，必须达到此值可被记录
long_query_time = 8

#检索的行数必须达到此值才可被记为慢查询
min_examined_row_limit = 100

#mysql binlog日志文件保存的过期时间，过期后自动删除
expire_logs_days = 5

############################主从复制设置#####################################

#开启mysql binlog功能
log-bin=mysql-bin

#binlog记录内容的方式，记录被操作的每一行
binlog_format = ROW

#对于binlog_format = ROW模式时，减少记录日志的内容，只记录受影响的列
binlog_row_image = minimal

#master status and connection information输出到表mysql.slave_master_info中
master_info_repository = TABLE

#the slave‘s position in the relay logs输出到表mysql.slave_relay_log_info中
relay_log_info_repository = TABLE

#作为从库时生效,想进行级联复制，则需要此参数
log_slave_updates

#作为从库时生效,中继日志relay-log可以自我修复
relay_log_recovery = 1

#作为从库时生效,主从复制时忽略的错误
slave_skip_errors = ddl_exist_errors

#####################redo log和binlog的关系设置BEGIN#########################

#(步骤1) prepare dml相关的SQL操作，然后将redo log buff中的缓存持久化到磁盘
#(步骤2)如果前面prepare成功，那么再继续将事务日志持久化到binlog
#(步骤3)如果前面成功，那么在redo log里面写上一个commit记录
#当innodb_flush_log_at_trx_commit和sync_binlog都为1时是最安全的，
#在mysqld服务崩溃或者服务器主机crash的情况下，binary log只有可能丢失最多一个语句或者一个事务。
#但是都设置为1时会导致频繁的io操作，因此该模式也是最慢的一种方式。
#当innodb_flush_log_at_trx_commit设置为0，mysqld进程的崩溃会导致上一秒钟所有事务数据的丢失。
#当innodb_flush_log_at_trx_commit设置为2，只有在操作系统崩溃或者系统掉电的情况下，上一秒钟所有事务数据才可能丢失。

#commit事务时,控制redo log buff持久化磁盘的模式 默认为1
innodb_flush_log_at_trx_commit = 2

#commit事务时,控制写入mysql binlog日志的模式 默认为0
#innodb_flush_log_at_trx_commit和sync_binlog都为1时，mysql最为安全但性能上压力也是最大
sync_binlog = 1

####################redo log和binlog的关系设置END############################

############################Innodb设置#####################################

#数据块的单位8k，默认是16k，16kCPU压力稍小，8k对select的吞吐量大
#innodb_page_size的参数值也影响最大索引长度，8k比16k的最大索引长度小
#innodb_page_size = 8192

#一般设置物理存储的60% ~ 70%
innodb_buffer_pool_size = 1G

#5.7.6之后默认16M
#innodb_log_buffer_size = 16777216

#该参数针对unix、linux，window上直接注释该参数.默认值为NULL
#O_DIRECT减少操作系统级别VFS的缓存和Innodb本身的buffer缓存之间的冲突
innodb_flush_method = O_DIRECT

#此格式支持压缩, 5.7.7之后为默认值
innodb_file_format = Barracuda

#CPU多核处理能力设置，假设CPU是2颗4核的，设置如下
#读多，写少可以设成2:6的比例
innodb_write_io_threads = 4
innodb_read_io_threads = 4

#提高刷新脏页数量和合并插入数量，改善磁盘I/O处理能力
#默认值200（单位：页）
#可根据磁盘近期的IOPS确定该值
innodb_io_capacity = 500

#为了获取被锁定的资源最大等待时间，默认50秒，超过该时间会报如下错误:
# ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
innodb_lock_wait_timeout = 30

#调整buffer pool中最近使用的页读取并dump的百分比,通过设置该参数可以减少转储的page数
innodb_buffer_pool_dump_pct = 40

#设置redoLog文件所在目录, redoLog记录事务具体操作内容
innodb_log_group_home_dir = /usr/local/mysql/redolog/

#设置undoLog文件所在目录, undoLog用于事务回滚操作
innodb_undo_directory = /usr/local/mysql/undolog/

#在innodb_log_group_home_dir中的redoLog文件数, redoLog文件内容是循环覆盖写入。
innodb_log_files_in_group = 3

#MySql5.7官方建议尽量设置的大些，可以接近innodb_buffer_pool_size的大小
#之前设置该值较大时可能导致mysql宕机恢复时间过长，现在恢复已经加快很多了
#该值减少脏数据刷新到磁盘的频次
#最大值innodb_log_file_size * innodb_log_files_in_group <= 512GB,单文件<=256GB
innodb_log_file_size = 1024M

#设置undoLog文件所占空间可以回收
#5.7之前的MySql的undoLog文件一直增大无法回收
innodb_undo_log_truncate = 1
innodb_undo_tablespaces = 3
innodb_undo_logs = 128

#5.7.7默认开启该参数 控制单列索引长度最大达到3072
#innodb_large_prefix = 1

#5.7.8默认为4个, Inodb后台清理工作的线程数
#innodb_purge_threads = 4

#通过设置配置参数innodb_thread_concurrency来限制并发线程的数量，
#一旦执行线程的数量达到这个限制，额外的线程在被放置到对队列中之前，会睡眠数微秒，
#可以通过设定参数innodb_thread_sleep_delay来配置睡眠时间
#该值默认为0,在官方doc上，对于innodb_thread_concurrency的使用，也给出了一些建议:
#(1)如果一个工作负载中，并发用户线程的数量小于64，建议设置innodb_thread_concurrency=0；
#(2)如果工作负载一直较为严重甚至偶尔达到顶峰，建议先设置innodb_thread_concurrency=128,
###并通过不断的降低这个参数，96, 80, 64等等，直到发现能够提供最佳性能的线程数
#innodb_thread_concurrency = 0

#强所有发生的死锁错误信息记录到error.log中，之前通过命令行只能查看最近一次死锁信息
innodb_print_all_deadlocks = 1

############################其他设置########################################

[mysqldump]
quick
max_allowed_packet = 128M

[mysql]
no-auto-rehash

[myisamchk]
key_buffer_size = 20M
sort_buffer_size = 256k
read_buffer = 2M
write_buffer = 2M

[mysqlhotcopy]
interactive-timeout

[mysqld_safe]
#增加每个进程的可打开文件数量
open-files-limit = 28192

```

- 设置开机启动

```
cp support-files/mysql.server /etc/init.d/mysql
chmod +x /etc/init.d/mysql 
#把mysql注册为开机启动的服务
chkconfig --add mysql  

#查看是否添加成功
chkconfig --list mysql  
```

- 启动服务
	

```
[root@VM_0_6_centos mysql]# service mysql start
Starting MySQL.. ERROR! The server quit without updating PID file (/usr/local/mysql/data/VM_0_6_centos.pid).

```
解决办法：

```
[root@VM_0_6_centos mysql]# mv /etc/my.cnf /etc/my.conf.bak #如果不重要的就删除

[root@VM_0_6_centos mysql]# service mysql start
Starting MySQL. SUCCESS! 

```

- 修改登录密码

先停止mysql

```
[root@VM_0_6_centos mysql]# service mysql stop
```

```
#运行
[root@VM_0_6_centos mysql]# ./bin/mysqld_safe --skip-grant-tables &

#为了安全可以这样禁止远程连接：
[root@VM_0_6_centos mysql]#  ./bin/mysqld_safe --skip-grant-tables --skip-networking &


[root@VM_0_6_centos mysql]# ./bin/mysql -u root -p
#然后直接enter键进入
```

![这里写图片描述](https://img-blog.csdn.net/20171210192138506?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

	
	到了这个界面就可以运行命令修改密码了密码改为root
```
mysql> update mysql.user set authentication_string=password('root') where user='root' and Host = 'localhost';
mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)

mysql> quit;
Bye

```

- 修改完毕。重启
 

```
[root@VM_0_6_centos mysql]# service mysql restart
Shutting down MySQL..2017-12-10T11:24:17.689364Z mysqld_safe mysqld from pid file /usr/local/mysql/data/VM_0_6_centos.pid ended
 SUCCESS! 
Starting MySQL. SUCCESS! 
[1]+  Done                    ./bin/mysqld_safe --skip-grant-tables

#登录就可以了
[root@VM_0_6_centos mysql]# ./bin/mysql -u root -p

```

操作的时候报错：ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.还要修改密码

```

mysql> create database newTest;
ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.
mysql> SET PASSWORD = PASSWORD('root');
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> ALTER USER 'root'@'localhost' PASSWORD EXPIRE NEVER;
Query OK, 0 rows affected (0.00 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.01 sec)

```
然后可以操作了。先添加一些测试数据

```
mysql> create database newTest;
Query OK, 1 row affected (0.00 sec)

mysql> use newTest;
Database changed
mysql> create table test(name varchar(10));
Query OK, 0 rows affected (0.12 sec)

mysql> insert into test values('zs');
Query OK, 1 row affected (0.03 sec)

mysql> insert into test values('ls');
Query OK, 1 row affected (0.05 sec)

```

###四、安装php模块
先安装libxml2

```
[root@VM_0_6_centos software]# tar -zxvf libxml2-2.7.4.tar.gz
[root@VM_0_6_centos software]# cd libxml2-2.7.4/
[root@VM_0_6_centos libxml2-2.7.4]# ./configure --prefix=/usr/local/libxml2
[root@VM_0_6_centos libxml2-2.7.4]# make && make install
```


```
[root@VM_0_6_centos software]# tar -zxvf php-5.5.38.tar.gz
[root@VM_0_6_centos software]# cd php-5.5.38/
[root@VM_0_6_centos php-5.5.38]# ./configure --prefix=/usr/local/php5.5 --with-mysql=/usr/local/mysql  --with-apxs2=/usr/local/apache2/bin/apxs --with-libxml-dir=/usr/local/libxml2
```

- php编译mysql模块时 error: Cannot find libmysqlclient_r under /usr/local/mysql，mysql默认为libmysqlclient.so，内容完全一样，做个链接即可

```
[root@VM_0_6_centos ~]# find /  -name libmysqlclient.so
/usr/local/mysql/lib/libmysqlclient.so
[root@VM_0_6_centos ~]# ln -s /usr/local/mysql/lib/libmysqlclient.so /usr/local/mysql/lib/libmysqlclient_r.so
[root@VM_0_6_centos php-5.5.38]# make && make install

```

- 下面就要使Apache支持解析php文件，修改apache的配置文件httpd.conf

```
[root@VM_0_6_centos apache2]# vi conf/httpd.conf

```
在末尾加入代码：

```
LoadModule php5_module modules/libphp5.so  #(注意，在apache安装目录下，modules下有libphp5.so，这是php安装时添加进去的，如果没有这个so，你需要编译php模块重装下,还有就是有的文件已经有这段代码，只需要下面一段代码就可以了)
AddType application/x-httpd-php .php      (.前面有空格)
```
###五、测试运行
现在编辑一个php文件测试下。

```
vi phpinfo.php
```
内容：
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

```
[root@VM_0_6_centos apache2]# ./bin/apachectl -k restart #重启Apache
```
![这里写图片描述](https://img-blog.csdn.net/20171210214406024?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

数据库里的数据已经查出来了。到此php基本运行环境已经有了,坑还是比较多,如果实在安装不了,建议大家用phpStudy的软件集成了php运行环境的还是挺不错的,有Windows，linux版本的；还有可以选择用docker之类的。
