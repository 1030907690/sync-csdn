@[TOC](目录)
# 前言
- 近期将Spring Boot 2升级到Spring Boot 3后，ES也随之升级。发现Flink SQL同步到ES 8有异常。
#  遇到的问题
- 第一次同步没有问题
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/690f6142b3fc4c0aa6086136ca413eb2.png)

- 发生在修改数据后出现如下错误：
- 
```java
Caused by: java.lang.NullPointerException
	at java.base/java.util.Objects.requireNonNull(Objects.java:209)
	at org.apache.flink.elasticsearch7.shaded.org.elasticsearch.action.DocWriteResponse.<init>(DocWriteResponse.java:127)
	at org.apache.flink.elasticsearch7.shaded.org.elasticsearch.action.update.UpdateResponse.<init>(UpdateResponse.java:65)
	at org.apache.flink.elasticsearch7.shaded.org.elasticsearch.action.update.UpdateResponse$Builder.build(UpdateResponse.java:172)
	at org.apache.flink.elasticsearch7.shaded.org.elasticsearch.action.update.UpdateResponse$Builder.build(UpdateResponse.java:160)
	at org.apache.flink.elasticsearch7.shaded.org.elasticsearch.action.bulk.BulkItemResponse.fromXContent(BulkItemResponse.java:159)
	at org.apache.flink.elasticsearch7.shaded.org.elasticsearch.action.bulk.BulkResponse.fromXContent(BulkResponse.java:188)
	at org.apache.flink.elasticsearch7.shaded.org.elasticsearch.client.RestHighLevelClient.parseEntity(RestHighLevelClient.java:1911)
	at org.apache.flink.elasticsearch7.shaded.org.elasticsearch.client.RestHighLevelClient.lambda$performRequestAsyncAndParseEntity$10(RestHighLevelClient.java:1699)
	at org.apache.flink.elasticsearch7.shaded.org.elasticsearch.client.RestHighLevelClient$1.onSuccess(RestHighLevelClient.java:1781)
	... 18 more

```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/35b4100baa2a4efbb3388a1c20e32ebb.png)
- 有极大可能`elasticsearch-7`不支持ES8，官方文档（[https://nightlies.apache.org/flink/flink-docs-release-1.20/zh/docs/connectors/table/elasticsearch/](https://nightlies.apache.org/flink/flink-docs-release-1.20/zh/docs/connectors/table/elasticsearch/)）的中文翻译似乎有问题。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/127d119bf977437d9018b0cc6ced9cd6.png)
- 而英文文档却没说支持更高版本
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/01b0f2833d52447f967f404ee61c8cbb.png)
- 翻找maven仓库并无`flink-sql-connector-elasticsearch8`的踪迹。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8662e1bdde2a47bca31d05c66592b8fc.png)
- 找到`flink-sql-connector-elasticsearch7`的源码 [https://github.com/apache/flink-connector-elasticsearch](https://github.com/apache/flink-connector-elasticsearch)也并没有`flink-sql-connector-elasticsearch8`
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6e8182aac265428aa5296c5ad3d956b9.png)
- 虽然搜寻无果，但也给了我一种启发，`flink-sql-connector-elasticsearch7`的代码有对于同步到ES8来说是API改变，可以模仿`flink-sql-connector-elasticsearch7`的逻辑写一个兼容ES8的`flink-sql-connector-elasticsearch8`

- 权衡之下Spring Boot 3使用ES 7要做的兼容工作量依旧不小,日后升级恐怕又是一个问题，还是升级ES,写一个兼容ES8的`flink-sql-connector-elasticsearch8`。

# 核心代码

- `pom` 文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.zzq.flink</groupId>
    <artifactId>flink-sql-connector-elasticsearch8-custom</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <flink.version>1.20.3</flink.version>
        <elasticsearch.version>8.18.8</elasticsearch.version>
        <scala.binary.version>2.12</scala.binary.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-table-common</artifactId>
            <version>${flink.version}</version>
            <scope>provided</scope>
        </dependency>

        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-table-api-java-bridge</artifactId>
            <version>${flink.version}</version>
            <scope>provided</scope>
        </dependency>

        <dependency>
            <groupId>co.elastic.clients</groupId>
            <artifactId>elasticsearch-java</artifactId>
            <version>${elasticsearch.version}</version>
        </dependency>

        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.15.0</version>
        </dependency>

        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>1.7.36</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>3.2.4</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>shade</goal>
                        </goals>
                        <configuration>
                            <artifactSet>
                                <excludes>
                                    <exclude>org.apache.flink:*</exclude>
                                    <exclude>org.slf4j:*</exclude>
                                    <exclude>log4j:*</exclude>
                                </excludes>
                            </artifactSet>
                            <filters>
                                <filter>
                                    <artifact>*:*</artifact>
                                    <excludes>
                                        <exclude>META-INF/*.SF</exclude>
                                        <exclude>META-INF/*.DSA</exclude>
                                        <exclude>META-INF/*.RSA</exclude>
                                    </excludes>
                                </filter>
                            </filters>
                            <transformers>
                                <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
                            </transformers>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

-  `ElasticsearchDynamicTableFactory`  入口点。负责解析 SQL 中的 WITH 参数，并决定创建 Sink 还是 Source。

```java
package com.zzq.flink.streaming.connectors.elasticsearch.table;

import com.zzq.flink.streaming.connectors.elasticsearch.config.ElasticsearchOptions;
import org.apache.flink.configuration.ConfigOption;
import org.apache.flink.configuration.ConfigOptions;
import org.apache.flink.configuration.ReadableConfig;
import org.apache.flink.table.connector.sink.DynamicTableSink;
import org.apache.flink.table.factories.DynamicTableSinkFactory;
import org.apache.flink.table.factories.FactoryUtil;
import org.apache.flink.table.types.DataType;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

/**
 * @author zzq
 * @date 2026/01/27 18:48:39
 * 入口点。负责解析 SQL 中的 WITH 参数，并决定创建 Sink 还是 Source
 */
public class ElasticsearchDynamicTableFactory implements DynamicTableSinkFactory {



    @Override
    public String factoryIdentifier() {
        return "elasticsearch-8"; // SQL 中使用的 'connector' 名称
    }

    @Override
    public Set<ConfigOption<?>> requiredOptions() {
        Set<ConfigOption<?>> options = new HashSet<>();
        options.add(ElasticsearchOptions.HOSTS); // 必须添加到这里
        options.add(ElasticsearchOptions.INDEX);
        return options;
    }

    @Override
    public Set<ConfigOption<?>> optionalOptions() {
        Set<ConfigOption<?>> options = new HashSet<>();
        options.add(ElasticsearchOptions.USERNAME);
        options.add(ElasticsearchOptions.PASSWORD);
        options.add(ElasticsearchOptions.BULK_FLUSH_MAX_ACTIONS);
        options.add(ElasticsearchOptions.CA_FINGERPRINT);
        return options;
    }

    @Override
    public DynamicTableSink createDynamicTableSink(Context context) {
        // 1. 获取配置
        FactoryUtil.TableFactoryHelper helper = FactoryUtil.createTableFactoryHelper(this, context);
        ReadableConfig config = helper.getOptions();

        // 2. 校验配置
        helper.validate();

        // 3. 获取物理数据类型（Schema）
        DataType physicalDataType = context.getCatalogTable().getResolvedSchema().toPhysicalRowDataType();

        return new ElasticsearchDynamicSink(config, physicalDataType);
    }
}
```

- `ElasticsearchDynamicSink` 描述数据如何写入。负责在提交 Job 时验证 Schema 和配置

```java
package com.zzq.flink.streaming.connectors.elasticsearch.table;


import com.zzq.flink.streaming.connectors.elasticsearch.config.ElasticsearchOptions;
import org.apache.flink.configuration.ReadableConfig;
import org.apache.flink.table.connector.ChangelogMode;
import org.apache.flink.table.connector.sink.DynamicTableSink;
import org.apache.flink.table.connector.sink.SinkFunctionProvider;
import org.apache.flink.table.types.DataType;
import org.apache.flink.types.RowKind;

/**
 * @author zzq
 * @date 2026/01/27 18:50:21
 * 描述数据如何写入。负责在提交 Job 时验证 Schema 和配置
 */

public class ElasticsearchDynamicSink implements DynamicTableSink {


    private final DataType physicalDataType;
    private final ReadableConfig config;

    // 构造函数，由 Factory 调用
    public ElasticsearchDynamicSink(ReadableConfig config, DataType physicalDataType) {
        this.config = config;
        this.physicalDataType = physicalDataType;
    }

    @Override
    public ChangelogMode getChangelogMode(ChangelogMode requestedMode) {
        // 告知 Flink 本 Sink 支持的数据操作类型
        // 支持所有操作类型：插入、更新前、更新后、删除
        return ChangelogMode.newBuilder()
                .addContainedKind(RowKind.INSERT)
                .addContainedKind(RowKind.UPDATE_BEFORE)
                .addContainedKind(RowKind.UPDATE_AFTER)
                .addContainedKind(RowKind.DELETE)
                .build();
    }

    @Override
    public SinkRuntimeProvider getSinkRuntimeProvider(Context context) {
        // 核心步骤：创建真正的物理 Sink 执行器
        // 我们可以把解析后的 physicalDataType 传递给 SinkFunction
        ElasticsearchSinkFunction sinkFunction = new ElasticsearchSinkFunction(config.get(ElasticsearchOptions.HOSTS),
                config.get(ElasticsearchOptions.INDEX), physicalDataType);

        // 返回 SinkFunctionProvider，Flink 会在并行算子中实例化它
        return SinkFunctionProvider.of(sinkFunction);
    }

    @Override
    public DynamicTableSink copy() {
        return new ElasticsearchDynamicSink(config, physicalDataType);
    }

    @Override
    public String asSummaryString() {
        return "Elasticsearch 8 Sink";
    }
}
```

- `ElasticsearchDynamicTableFactory` 真正操作ES的地方

```java
 package com.zzq.flink.streaming.connectors.elasticsearch.table;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.json.jackson.JacksonJsonpMapper;
import co.elastic.clients.transport.ElasticsearchTransport;
import co.elastic.clients.transport.rest_client.RestClientTransport;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;
import org.apache.flink.table.data.*;
import org.apache.flink.table.types.DataType;
import org.apache.flink.table.types.logical.LogicalType;
import org.apache.flink.table.types.logical.RowType;
import org.apache.flink.types.RowKind;
import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @author zzq
 * @date 2026/01/27 18:51:19
 * 真正操作ES的地方
 */
public class ElasticsearchSinkFunction extends RichSinkFunction<RowData> {
    private transient ElasticsearchClient client;
    private final String hosts;
    private final String index;
    private final DataType physicalDataType;
    private transient RowData.FieldGetter[] fieldGetters;
    private int primaryKeyIndex = 0; // 假设第一列是主键，实际应从 Schema 获取
    // 在类成员变量中定义格式化器
    private transient java.time.format.DateTimeFormatter formatter;

    public ElasticsearchSinkFunction(String hosts, String index, DataType physicalDataType) {
        this.hosts = hosts;
        this.index = index;
        this.physicalDataType = physicalDataType;
    }

    @Override
    public void open(Configuration parameters) throws Exception {
        this.formatter = java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        // 初始化 ES 8 客户端
        RestClient restClient = RestClient.builder(HttpHost.create(hosts)).build();
        ElasticsearchTransport transport = new RestClientTransport(restClient, new JacksonJsonpMapper());
        this.client = new ElasticsearchClient(transport);

        // 预编译字段提取器 (提高性能)
        LogicalType logicalType = physicalDataType.getLogicalType();
        RowType rowType = (RowType) logicalType;
        fieldGetters = new RowData.FieldGetter[rowType.getFieldCount()];
        for (int i = 0; i < rowType.getFieldCount(); i++) {
            fieldGetters[i] = RowData.createFieldGetter(rowType.getTypeAt(i), i);
        }
    }

    @Override
    public void invoke(RowData value, Context context) throws Exception {
        // 获取当前行操作类型
        RowKind kind = value.getRowKind();
        String docId = fieldGetters[primaryKeyIndex].getFieldOrNull(value).toString();

        if (kind == RowKind.INSERT || kind == RowKind.UPDATE_AFTER) {
            // Upsert 操作
            Map<String, Object> doc = rowToMap(value);
            client.index(i -> i
                    .index(index)
                    .id(docId)
                    .document(doc)
            );
        } else if (kind == RowKind.DELETE) {
            // 删除操作
            client.delete(d -> d.index(index).id(docId));
        }
        // UPDATE_BEFORE 通常忽略，因为紧接着的 UPDATE_AFTER 会覆盖整个 Doc
    }




    private Map<String, Object> rowToMap(RowData row) {
        Map<String, Object> map = new HashMap<>();
        RowType rowType = (RowType) physicalDataType.getLogicalType();
        List<String> fieldNames = rowType.getFieldNames();

        for (int i = 0; i < fieldGetters.length; i++) {
            Object val = fieldGetters[i].getFieldOrNull(row);
            // 获取该列的逻辑类型，用于处理复杂类型
            LogicalType type = rowType.getTypeAt(i);
            map.put(fieldNames.get(i), convertFlinkType(val, type));
        }
        return map;
    }

    private Object convertFlinkType(Object val, LogicalType type) {
        if (val == null) {
            return null;
        }

        // 处理嵌套行 (NestedRowData)
        if (val instanceof RowData) {
            RowData row = (RowData) val;
            RowType rowType = (RowType) type;
            Map<String, Object> nestedMap = new HashMap<>();
            List<String> fieldNames = rowType.getFieldNames();
            List<LogicalType> fieldTypes = rowType.getChildren();

            for (int i = 0; i < row.getArity(); i++) {
                // 为每一列创建临时 FieldGetter
                RowData.FieldGetter getter = RowData.createFieldGetter(fieldTypes.get(i), i);
                nestedMap.put(fieldNames.get(i), convertFlinkType(getter.getFieldOrNull(row), fieldTypes.get(i)));
            }
            return nestedMap;
        }

        // 处理 Map 类型
        if (val instanceof MapData) {
            MapData mapData = (MapData) val;
            LogicalType keyType = ((org.apache.flink.table.types.logical.MapType) type).getKeyType();
            LogicalType valueType = ((org.apache.flink.table.types.logical.MapType) type).getValueType();

            // 提取 Key 和 Value 的 FieldGetter (简单示例，生产建议缓存)
            ArrayData keyArray = mapData.keyArray();
            ArrayData valueArray = mapData.valueArray();
            Map<Object, Object> javaMap = new HashMap<>();

            for (int i = 0; i < mapData.size(); i++) {
                Object k = ArrayData.createElementGetter(keyType).getElementOrNull(keyArray, i);
                Object v = ArrayData.createElementGetter(valueType).getElementOrNull(valueArray, i);
                javaMap.put(convertFlinkType(k, keyType), convertFlinkType(v, valueType));
            }
            return javaMap;
        }

        // 处理 Array 类型
        if (val instanceof ArrayData) {
            ArrayData arrayData = (ArrayData) val;
            LogicalType eleType = ((org.apache.flink.table.types.logical.ArrayType) type).getElementType();
            List<Object> list = new java.util.ArrayList<>();
            for (int i = 0; i < arrayData.size(); i++) {
                Object ele = ArrayData.createElementGetter(eleType).getElementOrNull(arrayData, i);
                list.add(convertFlinkType(ele, eleType));
            }
            return list;
        }


        // 处理基础 Data 包装类
        if (val instanceof StringData) {
            return val.toString();
        }
        if (val instanceof TimestampData) {
            // 解决时间格式
            return ((TimestampData) val).toLocalDateTime().format(formatter);
        }
        if (val instanceof DecimalData) {
            return ((DecimalData) val).toBigDecimal();
        }
        return val;
    }

    @Override
    public void close() throws Exception {
        if (client != null) {
            client._transport().close();
        }
    }
}

```
- 声明`SPI`，让flink知道入口`META-INF/services/org.apache.flink.table.factories.Factory`
```java
com.zzq.flink.streaming.connectors.elasticsearch.table.ElasticsearchDynamicTableFactory
```

-  以上代码仅实现同步数据的基本功能。

# 验证

- 代码打包后放到flink lib目录，删除旧包。`connector`参数换成`elasticsearch-8`。
- 修改数据成功
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ef8d0cba78834cd3b1e8afc58ac058c7.png)
- flink也无报错信息。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b3fe04eb0f074d71a9dc77db0d9c9127.png)

# 题外话
- 我看到阿里云flink是支持ES 8的，apache却未提供`flink-sql-connector-elasticsearch8`,令人疑惑。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/08e683e2bd36425dbee3c010e0cbe974.png)


 
# 本文源码地址
- [https://github.com/1030907690/flink-sql-connector-elasticsearch8](https://github.com/1030907690/flink-sql-connector-elasticsearch8)
# 参考
- [https://github.com/apache/flink-connector-elasticsearch](https://github.com/apache/flink-connector-elasticsearch)
- [https://github.com/jeff-zou/flink-connector-redis](https://github.com/jeff-zou/flink-connector-redis)
- [https://github.com/apache/flink/blob/master/docs/content.zh/docs/dev/table/sourcesSinks.md](https://github.com/apache/flink/blob/master/docs/content.zh/docs/dev/table/sourcesSinks.md)
- Gemini AI