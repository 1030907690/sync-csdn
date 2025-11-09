@[TOC](目录)
# 前言
- 自MySQL 5.7.8开始引入原生JSON支持，可用于存储动态的列。此时如果想要建立索引，要先建立JSON某一列的`虚拟列`，使用虚拟列查询。从MySQL 8.0.17开始，InnoDB支持`多值索引`，相比老版本的查询方式就更直接了。
# 准备
- 创建一张配置表，建表语句如下。
```shell
CREATE TABLE `t_config` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `extras` json DEFAULT NULL COMMENT '扩展列json字段',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='配置表';
```
- 测试数据
```shell
INSERT INTO `t_config` (`id`, `extras`) VALUES (1, '{\"color\": \"red\", \"phone\": [\"157\", \"153\"]}');
INSERT INTO `t_config` (`id`, `extras`) VALUES (2, '{\"color\": \"green\", \"phone\": [\"157\", \"154\"]}');
```

- 下面就开始介绍`虚拟列`和`多值索引`查询与索引方式。
#  虚拟列

- 测试平台`5.7.26` 
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8914fed2f6a0492a8957fd32f3700cce.png)

- 查询 
```shell
SELECT * FROM `t_config` WHERE extras->'$.color' = 'red';
或
SELECT * FROM `t_config` WHERE json_contains(extras->'$.color','"red"');
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ce730d8630814ceaa180a9801412f028.png)

- 现在是走全表扫描
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/4597325d330a45e392a35797e39471b3.png)

- 下面创建虚拟列和索引
```shell
ALTER TABLE `t_config`
ADD COLUMN `v_color` VARCHAR(32) GENERATED ALWAYS AS
(JSON_UNQUOTE(JSON_EXTRACT(`extras`, _utf8mb4'$.color'))) VIRTUAL NULL;

CREATE INDEX idx_v_color on t_config(v_color);
```
- 查询就能走索引了
```shell
EXPLAIN SELECT * FROM `t_config` WHERE v_color = 'red';

```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6a228d23c3204019b91177016ec39195.png)

- 但是数组`phone`未找到合适的方式查询。
#  多值索引
- 测试平台`8.0.43`
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b08f31c31ad8476b8d01a47bc335980d.png)

- 查询（第二条语句不能利用索引）
```shell
SELECT * FROM `t_config` WHERE json_contains(extras->'$.color','"red"');
 或者
SELECT * FROM `t_config` WHERE extras->'$.color' = 'red';  

```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/4916783d5c0f4fe7b2bf33266f633ae5.png)
- 当前是全表扫描
```shell
EXPLAIN SELECT * FROM `t_config` WHERE json_contains(extras->'$.color','"red"');
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b6ce30d899044314ab4116c4bd674061.png)
- 增加json里 color字段索引
```shell
alter table t_config add index json_color( (cast(extras->'$.color' as char(32) array)));
```
- 现在就能走索引了
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f39e6a19f2de49f7b89b53be40e92356.png)

- 对于数字数组字段,查询方式

- 要先创建索引，才能查到数据
```shell
alter table t_config add index phone( (cast(extras->'$.phone' as unsigned array)) );
```
```shell
 -- 查询phone字段
 SELECT * FROM `t_config` WHERE json_contains(extras->'$.phone' , '157');

-- 查询phone字段, 参数数组
 SELECT * FROM `t_config` WHERE json_contains(extras->'$.phone' , CAST('[157,153]' AS JSON));
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8c98495d68fd4dcca8acd0203d059ac0.png)


- 能走索引
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/48f0a28d14504f9f870fe5e88c7a8ee7.png)



# 总结
- 从执行计划看，虚拟列的索引执行计划更优，但利用多值索引的`json_contains`查询方式就不需要转换SQL。虚拟列暂未找到查询数组的方式。


# 参考
- [https://cloud.tencent.com/developer/article/1843199](https://cloud.tencent.com/developer/article/1843199)
- [https://www.bilibili.com/video/BV1WP4y1K7xB/](https://www.bilibili.com/video/BV1WP4y1K7xB/)