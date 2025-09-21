@[TOC](目录) 

 # 安装
- 我的操作系统是Ubuntu，使用如下命令安装。

```bash
 apt install mysql-server
```

- 默认密码在`/etc/mysql/debian.cnf`文件中。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ec140f3126c6463ab1d2c282af5855e6.png)
- 进入MySQL，查看有哪些库

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/86f64ca413e14bb2b3ae7139475b3444.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/89a4a8601dd04cd3bafcdb405994a8e2.png)


# 不区分大小写的问题

- MySQL默认情况是区分大小写的。例如我先创建`T_USER`表。
```sql
CREATE TABLE `T_USER` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `age` int(11) NOT NULL,
  `phone` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

```

- 使用以下查询语句就能看出效果。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/132db77754c4470fa377800a1567092a.png)

- 在实际项目开发中，`Quartz`和`Flowable`框架的代码里使用表名大写，如果数据库里实际是小写，区分了大小写就找不到表。

# 设置不区分大小写

 - MySQL8不太一样要重新初始化MySQL

- 先停止当前MySQL
```bash
systemctl stop mysql

```

- 备份数据目录
```bash
 cp -r /var/lib/mysql /root/backup/
```

- 删除并新建mysql目录,改变目录所有者和组
```bash
mkdir /var/lib/mysql
chown -R mysql:mysql /var/lib/mysql
```

- 增加不区分大小写参数，编辑文件 `vim /etc/mysql/mysql.conf.d/mysqld.cnf`
```
lower_case_table_names  = 1
```

>lower_case_table_names 参数值含义：
0：表名区分大小写，且按照用户指定存储
1：表不区分大小写，使用小写存储
2：表不区分大小写，按照用户指定存储

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/68402e20531c47c79d633941378e9182.png)
- 无密码的初始化
```bash
# 无密码的初始化
mysqld --initialize-insecure 
```





- 启动MySQL
- 
```bash
systemctl start mysql
```

- 验证是否修改成功

- `mysql -u root -p` 无需密码，按enter键进入。
- `show variables like 'lower_case_table_names';`查看参数配置。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/96eca20ea1a948a9ae69912022c3aa5f.png)




 


#   参考
- [https://dblab.xmu.edu.cn/blog/3835/](https://dblab.xmu.edu.cn/blog/3835/)
- [https://blog.csdn.net/xhmico/article/details/136680013](https://blog.csdn.net/xhmico/article/details/136680013)