@[TOC](目录)
# 简介
- MySQL Shell 是 MySQL 官方新一代客户端工具，可替代传统 `mysql` 命令行，支持使用Python、SQL等多种交互模式，是 8.0+ 主推工具。
- 最让我惊喜的是它的备份恢复功能，执行效率碾压`mysqldump`。本文也主要讲这块。


# 安装
- Linux  (以 Ubuntu/Debian 为例)
```bash
sudo apt install mysql-shell
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/38907a7118da4480ace5e39ecc2408d9.png)
> 如果不用最新版本先用命令看支持哪些版本
>  apt-cache madison mysql-shell
>  安装命令 ： sudo apt install mysql-shell=版本


- Windows 下载地址：[https://dev.mysql.com/downloads/shell/](https://dev.mysql.com/downloads/shell/)  ，可能你不需要最新版本，可点击`Archives`进入存档版本。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/915edd79c50d4d3298990e0066602761.png)



# 备份库
- 先登陆 
```bash
mysqlsh -uroot -p -h192.168.23.166 -P3306
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/cd57c8200a6c4a3dab1e73385beb4467.png)

- 备份库(以`test`库为例)

```bash
util.dump_schemas(["test"], "/tmp/test_bak", {"threads": 4,"consistent": True,"showProgress": True})

```
- 重要参数解释：

> threads : 线程数
> **consistent ： 开启一致性快照备份**
> showProgress：控制台打印实时导出进度条、已导出行数、剩余预估，可视化进度

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ebf4bfa2c27c436fa331bad721fab89a.png)

# 恢复库
- 依然是先登陆
```bash
mysqlsh -uroot -p -h192.168.23.166 -P3306
```

- 切换到sql模式执行，设置允许客户端从**自己本地电脑 / 客户端服务器**读取文件。
```bash
\sql
SET GLOBAL local_infile = ON;
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/22d34543a16f4028914d1cebfe7f65c1.png)
- 切换到python模式，恢复库（恢复到`test_v2`为例）
```bash
\py
util.load_dump("/tmp/test_bak", {"threads": 4, "schema":  "test_v2"})
```


![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/7ff4d120652b4eb2a7bc585b8b6275be.png)
- 查看结果成功
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5262482fbcc548da9964641b42d59836.png)



- 使用了`local_infile`完成后关闭。
```bash
\sql
SET GLOBAL local_infile = OFF;
```





