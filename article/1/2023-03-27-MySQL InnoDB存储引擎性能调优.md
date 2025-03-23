---
layout:					post
title:					"MySQL InnoDB存储引擎性能调优"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
## CPU
- 在InnoDB存储引擎的设计架构上看，其主要的后台操作都是在一个单独的master thread中完成的，因此并不能很好地支持多核应用。当然，开源社区已经通过多种方法来改变这种局面。
- 如果你的CPU是多核，可以通过修改参数`innodb_read_io_threads`和`innodb_write_io_threads`来增大IO的线程，充分利用CPU的多核性能。
## 内存
- InnoDB存储引擎的缓冲池（InnoDB Buffer Pool） ,它的大小直接影响了数据库的性能。
- 如何判断当前数据库的内存是否已经达到瓶颈呢？可以通过查看当前服务器的状态，比较物理磁盘的读取和内存读取的比例来判断缓冲池的命中率。通常InnoDB存储引擎的缓冲池命中率不应该低于99%。
- 我们需要使用下方公式计算缓冲池命中率。
	 $$
	\frac{ Innodb\_buffer\_pool\_read\_requests } { Innodb\_buffer\_pool\_read\_requests  + Innodb\_buffer\_pool\_read\_ahead + Innodb\_buffer\_pool\_reads} = 缓冲池命中率
	$$
- 使用如`show global status like 'innodb%read%';`命令可以看到统计值，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9bb449247bff4636c14a91f866a7fd55.png)
> Innodb_buffer_pool_reads : 表示从物理磁盘读取页的次数。
> Innodb_buffer_pool_read_ahead ： 预读的次数。
> Innodb_buffer_pool_read_ahead_evicted ： 预读的页，但是没有被读取就从缓冲池被替换的页的数量，一般用来判断预读的效率。
> Innodb_buffer_pool_read_requests ： 从缓冲池中读取页的次数。
> Innodb_data_read ： 总共读入的字节数。
> Innodb_data_reads ： 发起读取请求的次数，每次读取可能需要读取多个页。

- 从上图可以看出，缓冲池命中率 = 16507 / (16507 + 0 + 868) ≈ 95%，可尝试增加缓冲池大小。主要调整`innodb_buffer_pool_instances`和`innodb_buffer_pool_size`参数。
> innodb_buffer_pool_size：缓冲池大小，默认的内存大小是 128M，理论上设置得越大，InnoDB 表性能就越好。不过，设置过大，可能会导致系统发生 SWAP 页交换。MySQL 推荐配置的大小为服务器物理内存的 80%。
>  innodb_buffer_pool_instances： 缓冲池被划分为了多个实例，对于具有数千兆字节的缓冲池的系统来说，将缓冲池划分为单独的实例可以减少不同线程读取和写入缓存页面时的争用，从而提高系统的并发性。该参数项仅在将 innodb_buffer_pool_size 设置为 1GB 或更大时才有意义。
- 计算平均每次读取的字节数公式如下。

	 $$
	\frac{ Innodb\_data\_read } { Innodb\_data\_reads  } = 平均每次读取的字节数
	$$

## RAID
- RAID（Redundant Array of Independent Disks,独立磁盘冗余数组）的基本思想，就是把多个相对便宜的硬盘组合起来，成为一个磁盘数组，使性能达到甚至超过一个价格昂贵、容量巨大的硬盘。由于将多个硬盘组合成为一个逻辑扇区，RAID看起来就像单独的硬盘或逻辑存储单元，因此操作系统会把它当做一个硬盘。

## 操作系统
- 大部分服务器内存已超过4GB，为了更好地使用大于4GB的内存容量，必须使用64位操作系统。并且使用64位MySQL，才能充分发挥64位操作系统寻址能力。
## 基准测试工具
- 基准测试工具可以用来对操作系统或数据库调优前后的性能作对比。常用的工具有`sysbench`和`mysql-tpcc`。
## 参考
- 《MySQL技术内幕 InnoDB存储引擎》