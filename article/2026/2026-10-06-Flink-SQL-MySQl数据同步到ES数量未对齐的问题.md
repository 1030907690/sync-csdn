
@[TOC](目录)
#  问题背景
- 使用Flink SQL把MySQL的商品数据同步到ES，发现ES的数据条数总是会少一些。SQL大概是这样的：
```sql
-- 商品数据以及这个商品对应实物最小克重
INSERT INTO es_product
SELECT
    mp.id,
    mp.name,
    agg.minWeight,
    ...省略...
    FROM mysql_product AS mp
    LEFT JOIN (
    SELECT
        product_id,
        MIN(weight) AS minWeight，
        ... 省略...
    FROM mysql_product_code
    WHERE code_status = 0
    GROUP BY product_id
) AS agg ON agg.product_id = mp.id
... 省略...

```



# 排除过程

## 排除出未同步的商品数据
- 我写了一个接口，查询全部表数据，一条条向ES查询判断有没有，找出未同步的数据。

## 打开ES新增修改日志

```
logger.index_indexing_slowlog.name = org.elasticsearch.index.indexing.slowlog
logger.index_indexing_slowlog.level = TRACE
logger.index_indexing_slowlog.appenderRef.index_indexing_slowlog.ref = index_indexing_slowlog

```




```

PUT /product_dev/_settings
{
  "index.search.slowlog.threshold.query.warn": "10s",
  "index.search.slowlog.threshold.fetch.warn": "10s",
  "index.indexing.slowlog.threshold.index.warn": "0ms",
  "index.indexing.slowlog.threshold.index.info": "0ms",
  "index.indexing.slowlog.threshold.index.debug": "0ms",
  "index.indexing.slowlog.threshold.index.trace": "0ms",
  "index.indexing.slowlog.source": "true"
}
```



- 排查完后关闭慢日志
```

PUT /product_dev/_settings
{
  "index.indexing.slowlog.threshold.index.warn": "-1",
  "index.indexing.slowlog.threshold.index.info": "-1",
  "index.indexing.slowlog.threshold.index.debug": "-1",
  "index.indexing.slowlog.threshold.index.trace": "-1",
  "index.indexing.slowlog.source": "false"
}

```
- 为了防止日志文件被压缩或清理`config/log4j2.properties`
> appender.rolling.policies.size.size = 111128MB

## 打开Flink debug日志

- 设置环境变量 ,编辑`~/.bashrc`,加入一下内容
```bash
export ROOT_LOG_LEVEL=DEBUG
export MAX_LOG_FILE_NUMBER=1000
```

```bash
source ~/.bashrc
```
- 为了防止日志文件被压缩或清理 `conf/log4j.properties`
>appender.main.policies.size.size = 10000MB

## 发现
-  针对未同步到ES的数据，查看Flink日志有向ES发送，并且ES日志也有打印这些数据。

- 豆包与Gemini都提到我的SQL，双流JOIN 回撤的问题。修改我的日志打印。
- 这块代码是我之前写的 [flink-sql-connector-elasticsearch8](https://github.com/1030907690/flink-sql-connector-elasticsearch8/)
```java
   @Override
    public void invoke(RowData value, Context context) throws Exception {
        // 获取当前行操作类型
        RowKind kind = value.getRowKind();
        String docId = fieldGetters[primaryKeyIndex].getFieldOrNull(value).toString();

        log.info("write ES, index={}, docId={}, op={}", index, docId, kind);

        if (kind == RowKind.INSERT || kind == RowKind.UPDATE_AFTER) {

            // Upsert 操作（加入批量缓冲，不阻塞当前线程，吞吐远高于逐条写）
            Map<String, Object> doc = rowToMap(value);
            bulkIngester.add(op -> op.index(i -> i
                    .index(index)
                    .id(docId)
                    .document(doc)
            ));

            log.debug("write ES success, index={}, docId={}, doc={}", index, docId, doc);

        } else if (kind == RowKind.DELETE) {
            // 删除操作（同样进入批量，与写入共用同一缓冲队列）
            bulkIngester.add(op -> op.delete(d -> d.index(index).id(docId)));
        }
        // UPDATE_BEFORE 通常忽略，因为紧接着的 UPDATE_AFTER 会覆盖整个 Doc
    }

```


- 果然发现有`DELETE`操作。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9f9984e4fe404f42846bf802a9f5e711.png)



# 解决方案

-  攒批、去重
```sql
--------------------------------------------------------------------------------
-- 1. MiniBatch 微批攒批（解决 ES 频发删改乱序、提升 Sink 吞吐）
--------------------------------------------------------------------------------
SET 'table.exec.mini-batch.enabled' = 'true';
SET 'table.exec.mini-batch.allow-latency' = '2s';
SET 'table.exec.mini-batch.size' = '5000';

--------------------------------------------------------------------------------
-- 2. 撤回流与聚合优化（消除中间冗余 -D/-U 消息、防止 GROUP BY 热点）
--------------------------------------------------------------------------------
-- 在微批内存中抵消/去重同一批次内的 -D / -U / +U，只输出最终状态
SET 'table.exec.retract.deduplicate' = 'true';

-- 开启 Local-Global 两阶段聚合（解决热点 Key 倾斜，降低 RocksDB I/O）
SET 'table.optimizer.agg-phase-strategy' = 'TWO_PHASE';

--------------------------------------------------------------------------------
-- 3. 状态与物理执行优化
--------------------------------------------------------------------------------
-- 状态过期时间（按需调整，如 7 天；若不设置，GROUP BY / JOIN 的状态将永久保存直到内存/磁盘溢出）
-- SET 'table.exec.state.ttl' = '7d';

-- 开启子计划复用（降低拓扑复杂度）
SET 'table.optimizer.reuse-sub-plan-enabled' = 'true';
```

- 兜底，我的业务没有物理删除商品数据索引屏蔽`DELETE`操作。
```java
    @Override
    public void invoke(RowData value, Context context) throws Exception {
        // 获取当前行操作类型
        RowKind kind = value.getRowKind();
        String docId = fieldGetters[primaryKeyIndex].getFieldOrNull(value).toString();

        log.info("write ES, index={}, docId={}, op={}", index, docId, kind);

        if (kind == RowKind.INSERT || kind == RowKind.UPDATE_AFTER) {

            // Upsert 操作（加入批量缓冲，不阻塞当前线程，吞吐远高于逐条写）
            Map<String, Object> doc = rowToMap(value);
            bulkIngester.add(op -> op.index(i -> i
                    .index(index)
                    .id(docId)
                    .document(doc)
            ));

            log.debug("write ES success, index={}, docId={}, doc={}", index, docId, doc);

        } else if (kind == RowKind.DELETE) {
            // 删除操作（同样进入批量，与写入共用同一缓冲队列）
            // 双流join撤回流问题，一般不会物理删除，先屏蔽
           // bulkIngester.add(op -> op.delete(d -> d.index(index).id(docId)));
        }
        // UPDATE_BEFORE 通常忽略，因为紧接着的 UPDATE_AFTER 会覆盖整个 Doc
    }
```












# 参考
- 豆包、Gemini
