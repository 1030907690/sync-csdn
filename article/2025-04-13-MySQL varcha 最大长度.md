 
@[TOC](目录)
## 基本存储规则
### MySQL 4.0版本以下
- `varchar(20)，指的是20字节`，如果存放UTF8汉字时，只能存6个（每个汉字3字节）。
### MySQL 5.0版本以上
- `varchar(20)，指的是20字符`，无论存放的是数字、字母还是汉字，都可以存放20个。


>`varchar`最多能存储`65535`个字节的数据。
- MySQL 4.0版本以下不考虑，几乎不会用到，我目前用的是MySQL 8.0。
- 本文验证用的是MySQL 8.0。
## 在utf8mb4字符集下

- varchar最多能存储`65535`个字节的数据。在`utf8mb4`字符集下，一个字符最多占用`4`个字节，因为不知道你要存什么，所以按最大的算。
- `粗略计算 65535   ÷   4 = 16383.75`，所以理论上`VARCHAR(16383)`最多可以占用。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ff8c1d1272e64f1da3f1e065cd31c74d.png)

## MySQL InnoDB 行格式
- 实际上，在在`utf8mb4`字符集下，表中存在其他字段或额外存储就用不了VARCHAR(16383)，受限于`最大行长度`。MySQL要求一个行的定义长度不能超过`65535`。
- 官方文档地址：[https://dev.mysql.com/doc/refman/8.4/en/column-count-limit.html](https://dev.mysql.com/doc/refman/8.4/en/column-count-limit.html)
![](https://i-blog.csdnimg.cn/direct/903b014175ed4ca5badfb1c9d0621b27.png)
- 下面以以COMPACT 行格式为例。查看行的存储结构。
### COMPACT 行格式
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/1443eb16af404b43897389afa9378de5.png)
- 变长字段长度列表：varchar类型声明存储最大字节数超过`255`字节，用`2`个字节表示，否则用`1`字节。
- NULL 值列表： 如果表中没有允许存储NULL的列，则NULL 值列表不存在，就不会占用空间。否则将每个允许存储NULL的列对应一个二进制位，`1个字节可以对应8个允许存储NULL的列`。如果超过8个就多占1个字节。
	- 二进制位值为1，表示该列为null。
	- 二进制位值为0，表示该列有真实数据。
- 记录头信息： 固定5字节组成。不计入限制65535个字节内。

## 计算方式
### 因素
- 实际上有三个因素影响varchar最大长度。
	- 1、变长字段长度列表占用的字节数。
	- 2、NULL 值列表占用的字节数。
	- 3、其他列占用的字节数。

### 计算公式
- 所以我们可以推导出更严谨的计算公式。
```
varchar可声明最大长度 = 65535 -  变长字段长度列表占用 - NULL 值列表占用 - 其他列占用
```

## 验证

例如我添加一个`type tinyint类型`，就会超过最大行长度，建议我把某些字段改为`text`或`BLOB`。
`MySQL 行大小最大限制为65535，不包括TEXT、BLOB`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5d10e851499e431791dd7fa7b13cec58.png)

- 我现在把列都改为不允许为空，就能省出1个字节。计算公式如下。
```
65535 - 2 - 0 - 1 = 65532
```
>  2是变长字段长度列表占用的字节数。
   0是NULL 值列表占用的字节数。
   1是我tinyint列占用的字节数。



- 结果是`65532`字节,utf8mb4每个字符以4字节计算，65532 / 4 = 16383。所以保存就能成功。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/99ff754e47bb4dedbc2b1481afa31d2e.png)







## 参考
- https://dev.mysql.com/doc/refman/8.4/en/column-count-limit.html#row-size-limits
- 《MySQL是怎样运行的：从根儿上理解MySQL》 - 4.3 InnoDB 行格式
- https://www.cnblogs.com/gomysql/p/3615897.html
- https://www.cnblogs.com/ivictor/p/15142160.html
- https://juejin.cn/post/6970934163973079048
- https://zhuanlan.zhihu.com/p/627823888
- https://www.cnblogs.com/dbf-/p/11611765.html