---
layout:					post
title:					"《Spring Cloud Alibaba微服务实战》 之 Sentinel集群流控"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
- 集群流控是为了解决在服务集群下流量不均匀导致总体限流效果不佳的问题。前面已经做了单机的流控。假设随着网站访问增加，1个服务提供者已经不够用了，为了提升承载量，再增加1个服务提供者。
- 那么在一个集群中问题就来了。服务提供者集群有2台机器，设置单机阀值为10 QPS，理想状态下整个集群的限流阈值就为 20 QPS，不过实际的流量到具体服务分配不均，导致总量没有到的情况下某些机器就开始限流，还有可能会超过阀值，可能实际限流QPS = 阀值 * 节点数。
- 这时候就需要集群流控了，集群流控的基本原理就是server端来专门来统计总量，其它client实例都与 server端通信来判断是否可以调用，并结合单机限流兜底，发挥更好的流量控制效果。

> 注意：Token Client（集群流控客户端）与Token Server（集群流控服务端）连接失败或通信失败时，如果勾选了失败退化，会退化到本地的限流模式

- 集群流控有以下两种角色。
Token Server：集群流控服务端，处理来自 Token Client 的请求，根据配置的集群规则判断是否运行通过。
Token Client：集群流控客户端，向Token Server发起请求，根据返回结果判断是否要限流。
实现集群流控服务端（Token Server）有以下两种方式。
独立模式（Alone）：服务独立运行，独立部署，隔离性好。
嵌入模式（Embedded）：即可以是集群流控服务端也可以是集群流控客户端，无需单独部署，灵活性比较好。不过为了不影响服务本身，需要限制QPS。
>不过本书只使用嵌入模式。下面就开始集群流控的具体操作吧！


### 1．向服务消费者的pom.xml文件dependencies标签内导入集群流控服务端、集群流控客户端和访问Nacos数据源的相关依赖。

```
<!--sentinel持久化 访问nacos数据源的依赖-->
<dependency>
	<groupId>com.alibaba.csp</groupId>
	<artifactId>sentinel-datasource-nacos</artifactId>
</dependency>
<!--集群流控客户端依赖-->
<dependency>
	<groupId>com.alibaba.csp</groupId>
	<artifactId>sentinel-cluster-client-default</artifactId>
</dependency>
<!--集群流控服务端依赖-->
<dependency>
	<groupId>com.alibaba.csp</groupId>
	<artifactId>sentinel-cluster-server-default</artifactId>
</dependency>
```
### 2．通过SPI完成配置源注册。定义com.alibaba.csp.sentinel.init.InitFunc的实现。

>注意：SPI（Service Provider Interface）是一种服务发现机制，查找META-INF/services下的文件，加载文件里所定义的类。说白了就是一个接口然后开发者自己去定义这个接口的实现类。

- 编写ApplicationInitializer类实现InitFunc接口，步骤就是注册客户端动态规则数据源、注册户端相关数据源、注册动态规则数据源、初始化服务器传输配置属性以及初始化群集状态属性，具体ApplicationInitializer代码和相关类如下所示（代码有点多）。

```
public class ApplicationInitializer implements InitFunc {
    private static final String APP_NAME = AppNameUtil.getAppName(); // 应用名称
    private final String remoteAddress = "127.0.0.1:8848"; // nacos服务地址
    private final String groupId = "DEFAULT_GROUP"; // 分组
    private final String flowDataId = APP_NAME + Constants.FLOW_POSTFIX; // 限流配置dataId
    private final String clusterMapDataId = APP_NAME + Constants.CLUSTER_MAP_POSTFIX;
    private static final String SEPARATOR = "@";
    @Override
    public void init() throws Exception {
        initDynamicRuleProperty();// 注册客户端动态规则数据源
        initClientServerAssignProperty(); // 注册户端相关数据源
        registerClusterRuleSupplier(); // 注册动态规则数据源
        initServerTransportConfigProperty();  //初始化服务器传输配置属性
        initStateProperty(); //初始化群集状态属性
    }
    private void initDynamicRuleProperty() {
        ReadableDataSource<String, List<FlowRule>> ruleSource = new NacosDataSource<>(remoteAddress, groupId,
                flowDataId, source -> JSON.parseObject(source, new TypeReference<List<FlowRule>>() {
        }));
        FlowRuleManager.register2Property(ruleSource.getProperty());// 注册动态规则数据源
    }
    private void initServerTransportConfigProperty() {
        ReadableDataSource<String, ServerTransportConfig> serverTransportDs = new NacosDataSource<>(remoteAddress, groupId, clusterMapDataId, source -> {
            List<ClusterGroupEntity> groupList = JSON.parseObject(source, new TypeReference<List<ClusterGroupEntity>>() {
            });
            return Optional.ofNullable(groupList).flatMap(this::extractServerTransportConfig).orElse(null);
        });
        ClusterServerConfigManager.registerServerTransportProperty(serverTransportDs.getProperty());
    }
    private void registerClusterRuleSupplier() {
        ClusterFlowRuleManager.setPropertySupplier(namespace -> {
            ReadableDataSource<String, List<FlowRule>> ds = new NacosDataSource<>(remoteAddress, groupId,
                    namespace + Constants.FLOW_POSTFIX, source -> JSON.parseObject(source, new TypeReference<List<FlowRule>>() {
            }));
            return ds.getProperty();
        });
        ClusterParamFlowRuleManager.setPropertySupplier(namespace -> {
            ReadableDataSource<String, List<ParamFlowRule>> ds = new NacosDataSource<>(remoteAddress, groupId,
                    namespace + Constants.PARAM_FLOW_POSTFIX, source -> JSON.parseObject(source, new TypeReference<List<ParamFlowRule>>() {
            }));
            return ds.getProperty();
        });
    }
    private void initClientServerAssignProperty() {
        ReadableDataSource<String, ClusterClientAssignConfig> clientAssignDs = new NacosDataSource<>(remoteAddress, groupId,
                clusterMapDataId, source -> {
            List<ClusterGroupEntity> groupList = JSON.parseObject(source, new TypeReference<List<ClusterGroupEntity>>() {
            });
            return Optional.ofNullable(groupList).flatMap(this::extractClientAssignment).orElse(null);
        }); 
        ClusterClientConfigManager.registerServerAssignProperty(clientAssignDs.getProperty());
    }
    private void initStateProperty() {
        ReadableDataSource<String, Integer> clusterModeDs = new NacosDataSource<>(remoteAddress, groupId,
                clusterMapDataId, source -> {
            List<ClusterGroupEntity> groupList = JSON.parseObject(source, new TypeReference<List<ClusterGroupEntity>>() {
            });
            return Optional.ofNullable(groupList).map(this::extractMode).orElse(ClusterStateManager.CLUSTER_NOT_STARTED);
        });
        ClusterStateManager.registerProperty(clusterModeDs.getProperty());
    }
    private int extractMode(List<ClusterGroupEntity> groupList) {
        if (groupList.stream().anyMatch(this::machineEqual)) {
            return ClusterStateManager.CLUSTER_SERVER;
        }
        boolean canBeClient = groupList.stream().flatMap(e -> e.getClientSet().stream()).filter(Objects::nonNull).anyMatch(e -> e.equals(getCurrentMachineId()));
        return canBeClient ? ClusterStateManager.CLUSTER_CLIENT : ClusterStateManager.CLUSTER_NOT_STARTED;
    }
    private Optional<ServerTransportConfig> extractServerTransportConfig(List<ClusterGroupEntity> groupList) {
        return groupList.stream().filter(this::machineEqual).findAny().map(e -> new ServerTransportConfig().setPort(e.getPort()).setIdleSeconds(600));
    }
    private Optional<ClusterClientAssignConfig> extractClientAssignment(List<ClusterGroupEntity> groupList) {
        if (groupList.stream().anyMatch(this::machineEqual)) {
            return Optional.empty();
        }
        for (ClusterGroupEntity group : groupList) {
            if (group.getClientSet().contains(getCurrentMachineId())) {
                String ip = group.getIp();
                Integer port = group.getPort();
                return Optional.of(new ClusterClientAssignConfig(ip, port));
            }
        }
        return Optional.empty();
    }
    private boolean machineEqual(/*@Valid*/ ClusterGroupEntity group) {
        return getCurrentMachineId().equals(group.getMachineId());
    }
    private String getCurrentMachineId() {
        return HostNameUtil.getIp() + SEPARATOR + TransportConfig.getRuntimePort();
    }
}
public class ClusterGroupEntity {
    private String machineId; //机器id
    private String ip; // ip地址
    private Integer port; // 端口
    private Set<String> clientSet;
    public String getMachineId() {
        return machineId;
    }
    public ClusterGroupEntity setMachineId(String machineId) {
        this.machineId = machineId;
        return this;
    }
    public String getIp() {
        return ip;
    }
    public ClusterGroupEntity setIp(String ip) {
        this.ip = ip;
        return this;
    }
    public Integer getPort() {
        return port;
    }
    public ClusterGroupEntity setPort(Integer port) {
        this.port = port;
        return this;
    }
    public Set<String> getClientSet() {
        return clientSet;
    }
    public ClusterGroupEntity setClientSet(Set<String> clientSet) {
        this.clientSet = clientSet;
        return this;
    }
    @Override
    public String toString() {
        return "ClusterGroupEntity{" +
                "machineId='" + machineId + '\'' +
                ", ip='" + ip + '\'' +
                ", port=" + port +
                ", clientSet=" + clientSet +
                '}';
    }
}
public class Constants {
    public static final String FLOW_POSTFIX = "-flow-rules";
    public static final String PARAM_FLOW_POSTFIX = "-param-rules";
    public static final String CLUSTER_MAP_POSTFIX = "-cluster-map";
}
```
- 下面就该指定ApplicationInitializer为com.alibaba.csp.sentinel.init.InitFunc的实现类了。在项目resources目录下创建META-INF/services/com.alibaba.csp.sentinel.init.InitFunc文件，填写如下内容。

```
com.springcloudalibaba.sentinel.init.ApplicationInitializer
```
### 3．服务提供者再增加一个节点。

- 既然要做一个服务提供者集群，那么至少也要2个节点，笔者将服务提供者复制了一份，修改一下端口，并把应用名称统一为sentinel-provider-sample，服务消费者修改下调用的应用名称。

### 4．在Nacos控制台创建一条新的DataId数据，具体内容如图6.40所示。


![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cada58b052b0dabd14ab0c6599e339f0.png#pic_center)
<center>图6.40  集群流控持久化规则</center>


- sentinel-provider-sample-flow-rules对应的就是ApplicationInitializer类中flowDataId变量的值。
- 配置内容中json字段解释。
resource：资源名称。
grade：阀值类型（0 - 线程数限制、1 - QPS）。
count：限流阀值（本次设置的QPS是100）。
clusterMode：是否是集群模式。
clusterConfig：集群配置。
flowId：全局唯一id。
thresholdType：集群阈值模式（0 - 单机均摊、1 - 总体阈值）。
fallbackToLocalWhenFail：如果 Token Server不可用是否退化到单机限流。


### 5．启动2个提供者服务和1个消费者服务，并请求一次它们各自的接口，使Sentinel出现对它们的操作界面。

### 6．如果Nacos持久化规则配置成功，则会出现如图6.41所示/test资源的流控规则。


![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/52dd52c92ee39c4d901975cca9447ace.png#pic_center)
<center>图6.41  Sentinel控制台集群流控持久化规则</center>


- 只看正向的效果可能不好断定集群限流是否生效，先不配置集群流控，先来看看“反向操作”的效果。
- 笔者使用JMeter工具2个线程一直循环调用服务消费者的/test接口，服务消费者的/test又会去调用服务提供者的/test接口。发起调用后在Sentinel控制台实时监控的结果如图6.42所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/720cbdfef94a9ddf617d242bcfcd08d8.png#pic_center)
<center>图6.42  未配置集群流控的效果</center>

- 从上图可以看出，集群总体阀值是100，而通过的QPS是200QPS，通过的QPS = 阀值 * 集群节点数，这明显是不正确的结果。

### 7．看完错误的结果后，来到最为重要的一步，设置Token Server（集群流控服务端）和Token Client（集群流控客户端）。


- 来到集群流控页面，点击新增Token Server，集群类型选择应用内机器，选择集群下拉框随便选择一个就可以，Server端口可以使用默认的，最大允许QPS也可以使用默认的，最后就是选取Token Client（集群流控客户端），配置如图6.43所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/01a2ddf1ca8ca5a82466fdc5ff8e6cf7.png#pic_center)
<center>图6.43  配置Token Server（集群流控服务端）和Token Client（集群流控客户端）</center>

>注意：目前Sentinel并未提供Token Server高可用的解决方案，不过Token Server挂了降级为本地流控，也不会有太大问题。
- 这些代码和配置都完成后，就来简单验证下。现在的流控规则配置是集群QPS总体阀值100。
- 再使用JMeter工具2个线程一直循环调用服务消费者的/test接口。发起调用后在Sentinel控制台实时监控的结果如图6.44所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/581d48fcadaafb1f439eadaa18aded48.png#pic_center)

<center>图6.44  集群流控效果</center>

- 从上图看出服务提供者的通过QPS基本稳定在100左右。可以断定集群流控还是有效果的。
- 上面是简单的流控规则，像热点参数限流也是类似的，使用如下代码。

```
ReadableDataSource<String, List<ParamFlowRule>> paramRuleSource = new NacosDataSource<>
(remoteAddress, groupId,paramDataId, source -> JSON.parseObject(source, new TypeReference<List<ParamFlowRule>>(){}));
ParamFlowRuleManager.register2Property(paramRuleSource.getProperty());
```
- paramDataId变量值就是要在Nacos新增的DataId，热点参数的规则。


- 本文是《Spring Cloud Alibaba微服务实战》书摘之一，如有兴趣可购买书籍。[天猫](https://detail.tmall.com/item.htm?spm=a230r.1.14.40.4d013ed4NkvyPZ&id=650584628890&ns=1&abbucket=3)、[京东](https://item.jd.com/13365970.html)、[当当](http://product.dangdang.com/29275400.html)。书中内容有任何问题，可在本博客下留言，或者到[https://github.com/1030907690](https://github.com/1030907690)提issues。