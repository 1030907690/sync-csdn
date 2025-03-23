---
layout:					post
title:					"《Spring Cloud Alibaba微服务实战》 之 Nacos + OpenResty + Keepalived高可用集群"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)

- 上一小节说到此时Nacos集群服务只是基本的高可用，因为此时的短板在于OpenResty，它就只有一个服务，试想下，如果中途宕机（虽然这个概率很小），那就引发单点故障，请求连入口都进不来。
- 至于如何解决呢？
- 可能很多读者朋友都能想到了，既然Nacos能做集群，那OpenResty也可以呀！虽然OpenResty不能像Tomcat那样直接配置集群，但是可以联合Keepalived做成高可用的集群。加入Keepalived后的部署架构图如图4.24所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7546a4859e55a67a81b80991539f9b87.png#pic_center)
<center>图4.24  加入Keepalived后的部署架构图
</center>


- 从图上可以看出客户端请求VIP（虚拟IP），然后请求到某个OpenResty，最后由OpenResty转发到具体的某个Nacos节点。这中间OpenResty服务是高可用的，因为一台服务宕机了，VIP会转到另一台OpenResty服务。
- Keepalived最早是为LVS设计的，用来监控LVS集群系统中服务节点的状态，后续加入了VRRP（Virtual Router Redundancy Protocol）功能，中文名称虚拟路由器冗余协议，是用来解决静态路由单点故障，保证服务高可用的解决方案。

- VRRP协议为两台或多台设备提供出一个或多个VIP（Virtual IP），其内部节点角色分为MASTER和BACKUP。通过算法选举产生。假设有两台服务，一个MASTER一个BACKUP，首先会选举MASTER提供服务；当BACKUP无法接收到MASTER心跳时会重新选举（根据优先级）BACKUP节点来提供服务。
- 为了更好的演示，笔者克隆了一台虚拟机，使用2台Centos7.0的虚拟机，部署规划如表4.2所示。

<center>
表4.2  Nacos + OpenResty + Keepalived部署规划
</center>

|名称|	部署的服务器IP|	主从|
|--|--|--|
|Nacos node1	|192.168.42.128|	-|
|Nacos node2	|192.168.42.128	|-|
|Nacos node3|	192.168.42.128|	-|
|OpenResty	|192.168.42.128	|-|
|OpenResty	|192.168.42.129	|-|
|Keepalived|	192.168.42.128|	BACKUP|
|Keepalived	|192.168.42.129	|MASTER|

- 下面看看具体的部署过程，Nacos和OpenResty的部署就不做过多赘述了，都是上一小节的知识。
- 正常部署情况下192.168.42.129主机缺少OpenResty和Keepalived，192.168.42.128主机缺少Keepalived，不过笔者虚拟机是克隆的，所以这两台主机只缺Keepalived，如果要安装可以使用上面的脚本（前提是Centos7.X）。安装好OpenResty记得负载均衡的地址不能是127.0.0.1了，而是填写内网IP，代码如下所示。

```
upstream nacosCluster{
	server 192.168.42.128:8848;
	server 192.168.42.128:8849;
	server 192.168.42.128:8850;
}
```

> 注意：记得设置防火墙端口允许访问或者暂时关闭防火墙。

- 现在进入主题下载、安装、配置Keepalived。
- 1．Keepalived官网下载地址：https://www.keepalived.org/download.html。笔者下载的是目前较新keepalived-2.1.5.tar.gz版本。
- 2．解压缩包，两台主机都这样操作。


```
tar -zxvf keepalived-2.1.5.tar.gz
```

- 3．切换到解压后的目录，配置、编译、安装；两台主机都这样操作。

```
cd keepalived-2.1.5  # 切换到目录
./configure --prefix=/usr/local/keepalived  # 配置
make && make install  # 编译安装
```
- 4．把Keepalived设置为系统服务，两台主机都这样操作。

```
mkdir /etc/keepalived   #先创建配置文件存放目录
cp /usr/local/keepalived/etc/keepalived/keepalived.conf /etc/keepalived/  #复制配置文件到默认路径
cp /usr/local/keepalived/sbin/keepalived /usr/sbin/  # 拷贝执行文件
cp /root/software/keepalived-2.1.5/keepalived/etc/init.d/keepalived /etc/init.d/   # 将初始化脚本拷贝到系统初始化目录下  /root/software/keepalived-2.1.5是源码包路径
cp /root/software/keepalived-2.1.5/keepalived/etc/sysconfig/keepalived /etc/sysconfig  # 将keepalived配置文件拷贝到etc下 /root/software/keepalived-2.1.5是源码包路径
chmod +x /etc/init.d/keepalived  # 添加可执行权限
```
- 5．加入到开机自启动，两台主机都这样操作。

```
chkconfig --add keepalived  # 添加keepalived到开机启动
chkconfig keepalived on
```
- 6．允许vrrp包发送（或者暂时关闭防火墙），两台主机都这样操作，否则可能两台都有VIP。

```
firewall-cmd --direct --permanent --add-rule ipv4 filter INPUT 0  --protocol vrrp -j ACCEPT
firewall-cmd --reload
```
- 7．编辑MASTER /etc/keepalived/keepalived.conf文件，里面内容很多，不过可以删除一下，修改后的内容如下。

```
vrrp_script chk_openresty {
   script "/etc/keepalived/openresty_check.sh"  #检测 nginx 状态的脚本路径
   interval 2 # 检测时间间隔
    weight -20 # 如果条件成立，权重-20 
}
vrrp_instance VI_1 {
    state MASTER  # 主节点为 MASTER，对应的备份节点为 BACKUP
    interface ens33  # 绑定虚拟 IP 的网络接口，与本机 IP 地址所在的网络接口相同,笔者是ens33
    virtual_router_id 51 # 虚拟路由的 ID 号，两个节点设置必须一样，可选 IP 最后一段使用, 相同的 VRID 为一个组，他将决定多播的 MAC 地址
    priority 100 # 节点优先级，值范围 0-254，MASTER 要比 BACKUP 高
    advert_int 1 # 组播信息发送间隔，两个节点设置必须一样
    authentication { # 设置验证信息， 两个节点设置必须一样，用于节点间信息转发时的加密
        auth_type PASS
        auth_pass 1111
}
	track_script {# 将 track_script 块加入 instance 配置块
		chk_openresty # 执行 openresty 监控的服务
	}
    virtual_ipaddress {
        192.168.42.130/24 # 此处的虚拟ip同一个网段即可 24代表3个255的子网掩码
    }
}
```

- 8．编辑BACKUP /etc/keepalived/keepalived.conf文件，修改后的内容如下。

```
vrrp_script chk_openresty {
   script "/etc/keepalived/openresty_check.sh"  #检测 nginx 状态的脚本路径
   interval 2 # 检测时间间隔
    weight -20 # 如果条件成立，权重-20 
}
vrrp_instance VI_1 {
    state BACKUP  # 主节点为 MASTER，对应的备份节点为 BACKUP
    interface ens33  # 绑定虚拟 IP 的网络接口，与本机 IP 地址所在的网络接口相同,笔者是ens33
    virtual_router_id 51 # 虚拟路由的 ID 号，两个节点设置必须一样，可选 IP 最后一段使用, 相同的 VRID 为一个组，他将决定多播的 MAC 地址
    priority 50 # 节点优先级，值范围 0-254，MASTER 要比 BACKUP 高
    advert_int 1 # 组播信息发送间隔，两个节点设置必须一样
    authentication { # 设置验证信息， 两个节点设置必须一样，用于节点间信息转发时的加密
        auth_type PASS
        auth_pass 1111
}
	track_script {# 将 track_script 块加入 instance 配置块
		chk_openresty # 执行 openresty 监控的服务
	}
    virtual_ipaddress {
        192.168.42.130/24 # 此处的虚拟ip同一个网段即可 24代表3个255的子网掩码
    }
}
```
- 9．编写检测OpenResty服务的脚本，路径为 /etc/keepalived/openresty_check.sh，两台主机都要这个脚本，内容如下所示。

```
#!/bin/bash
n=`ps -C openresty --no-header |wc -l` # 得到openresty进程的个数
if [ $n -eq 0 ];then # 如果为0
 /usr/local/openresty/bin/openresty  # 尝试启动openresty
 sleep 2  # 睡眠2秒
 if [ `ps -C openresty --no-header |wc -l` -eq 0 ];then  # 启动之后,再次检查openresty进程的个数是否等于0
 killall keepalived  # 如果还为0杀死keepalived进程,让其他的机器来提供服务
 fi
fi
```
- 10．启动服务，两台主机都启动，使用以下命令。

```
service keepalived start
```
- 11．使用命令查看IP，已经有虚拟IP 192.168.42.130了。返回内容如下所示就是成功的。

```
ip addr
...省略...
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:ce:85:90 brd ff:ff:ff:ff:ff:ff
    inet 192.168.42.129/24 brd 192.168.42.255 scope global noprefixroute dynamic ens33
       valid_lft 1633sec preferred_lft 1633sec
    inet 192.168.42.130/24 scope global secondary ens33
       valid_lft forever preferred_lft forever
    inet6 fe80::ec72:b84b:da19:1a7f/64 scope link tentative noprefixroute dadfailed 
       valid_lft forever preferred_lft forever
    inet6 fe80::fb72:cffc:c3df:e507/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
...省略...
```
- 12．Keepalived的其他常用命令。

```
service keepalived stop # 停止
service keepalived restart # 重启
service keepalived status # 查看状态
```



- 服务已经做好了，下面开始进入验证阶段。
- 首先笔者使用浏览器打开地址http://192.168.42.130/nacos/index.html，确认换成虚拟IP能否访问到Nacos，结果如图4.25所示。
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8f81cf7e059cb9ec8220c9f7c4b36dd2.png#pic_center)
<center>图4.25  使用虚拟IP访问
</center>

- 下一步笔者验证脚本是否生效，OpenResty停止后是否能自启动。笔者先使用命令关闭，然后看它自启动，效果如图4.26所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e7795d054b2090306f04b642f6a223c0.png#pic_center)

<center>图4.26  OpenResty停止后自启动
</center>


- 这步是最重要的一项测试，测试高可用，比如笔者现在把MASTER（192.168.42.129）这台主机关机，模拟宕机的效果；再来看看虚拟IP会不会到BACKUP（192.168.42.129）这台主机，效果如图4.27所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9c813bdd626651345e8f5f181d15347e.png#pic_center)
<center>图4.27  VIP切换到备机
</center>

- 再次访问页面也能打开，效果如图4.28所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f224e0aa594acce2bf887bf511ef07b4.png#pic_center)
<center>图4.28  切换到备机后测试页面能否访问
</center>

- 最后一步代码测试，笔者只需要将配置文件中配置项spring.cloud.nacos.discover.server-addr和spring.cloud.nacos.config.server-addr修改为192.168.42.130:80即可，使用curl测试结果如下所示即表示成功。

```
D:\software\curl-7.71.1-win64-mingw\bin>curl http://localhost:8080/getConfig
nacos cluster namespace fast_team group CUSTOM_GROUP active dev mysql database
```
- 好了Nacos + OpenResty + Keepalived高可用集群到此结束，过程的确有些繁琐，但也是没办法的事，有的时候还会做得更严谨更复杂些，这里还只是简单体验下。
- 大部分小公司Nacos + OpenResty这样的搭配一般都是足够了，OpenResty服务宕机的概率还是很小的，之前被人DDOS攻击几个星期，从来没发生过宕机的情况，只是多了一堆日志。还是那句话根据自己的业务量来选择。

- 本文是《Spring Cloud Alibaba微服务实战》书摘之一，如有兴趣可购买书籍。[天猫](https://detail.tmall.com/item.htm?spm=a230r.1.14.40.4d013ed4NkvyPZ&id=650584628890&ns=1&abbucket=3)、[京东](https://item.jd.com/13365970.html)、[当当](http://product.dangdang.com/29275400.html)。书中内容有任何问题，可在本博客下留言，或者到[https://github.com/1030907690](https://github.com/1030907690)提issues。