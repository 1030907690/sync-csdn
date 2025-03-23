---
layout:					post
title:					"《Spring Cloud Alibaba微服务实战》 之 Spring Cloud Gateway整合Sentinel功能"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)

- 自1.6.0版本开始，Sentinel提供了Spring Cloud Gateway的适配模块，能针对路由（route）和自定义API分组两个维度进行限流。
## 路由维度

- 路由维度指配置文件中的路由条目，资源名是对应的routeId，相比自定义API维度这是一个较为粗粒度的限流。
下面就来实现网关路由维度的限流。

- 1．首先导入Sentinel组件为Spring Cloud Gateway提供的适配模块依赖包，在项目pom.xml文件dependencies标签内添加如下代码。

```
<!--Sentinel组件为Spring Cloud Gateway提供的适配模块依赖包-->
<dependency>
	<groupId>com.alibaba.csp</groupId>
	<artifactId>sentinel-spring-cloud-gateway-adapter</artifactId>
</dependency>
```


- 2．新增配置类SentinelRouteConfiguration，实例化SentinelGatewayFilter和SentinelGatewayBlockExceptionHandler对象，初始化限流规则，自定义限流后的界面显示，具体代码如下所示。

```
@Configuration // 标记为配置类
public class SentinelRouteConfiguration { // 路由维度限流配置类
    private final List<ViewResolver> viewResolvers;
    private final ServerCodecConfigurer serverCodecConfigurer;
    public SentinelRouteConfiguration(ObjectProvider<List<ViewResolver>> viewResolversProvider, // 构造函数
                                      ServerCodecConfigurer serverCodecConfigurer) {
        this.viewResolvers = viewResolversProvider.getIfAvailable(Collections::emptyList);
        this.serverCodecConfigurer = serverCodecConfigurer;
    }
    @PostConstruct
    public void initGatewayRules() { //初始化限流规则
        Set<GatewayFlowRule> rules = new HashSet<>();
        GatewayFlowRule gatewayFlowRule = new GatewayFlowRule("user_route");// 资源名称，对应routeId的值 此处限流用户服务
        gatewayFlowRule.setCount(1); // 限流阀值
        gatewayFlowRule.setIntervalSec(1); // 统计时间窗口（单位：秒），默认是1秒
        rules.add(gatewayFlowRule);
        GatewayRuleManager.loadRules(rules); // 载入规则
    }
    @PostConstruct
    public void initBlockHandlers() {  // 自定义限流后的界面
        BlockRequestHandler blockRequestHandler = new BlockRequestHandler() {
            @Override
            public Mono<ServerResponse> handleRequest(ServerWebExchange serverWebExchange, Throwable throwable) {
                Map<String, String> result = new HashMap<>(); //  限流提示
                result.put("code", "0");
                result.put("message", "您已被限流");
                return ServerResponse.status(HttpStatus.OK).contentType(MediaType.APPLICATION_JSON_UTF8).
                        body(BodyInserters.fromObject(result));
            }
        };
        GatewayCallbackManager.setBlockHandler(blockRequestHandler);
    }
    @Bean
    @Order(Ordered.HIGHEST_PRECEDENCE)
    public SentinelGatewayBlockExceptionHandler sentinelGatewayBlockExceptionHandler() { // 配置限流异常处理器
        return new SentinelGatewayBlockExceptionHandler(viewResolvers, serverCodecConfigurer);
    }
    @Bean
    @Order(Ordered.HIGHEST_PRECEDENCE)
    public GlobalFilter sentinelGatewayFilter() { //初始化一个限流的过滤器
        return new SentinelGatewayFilter();
    }
}
```
>注意：Spring Cloud Gateway限流是通过Filter实现的，主要是注入SentinelGatewayFilter实例和SentinelGatewayBlockExceptionHandler实例。

- application.yml文件依然维持最开始配置的user_route和shop_route路由。然后使用curl命令，快速调用用户服务和商品服务，每个服务都调用2次，结果如下所示。

```
D:\software\curl-7.71.1-win64-mingw\bin>curl http://localhost:8083/user/findById?id=1
ZhangSan
D:\software\curl-7.71.1-win64-mingw\bin>curl http://localhost:8083/user/findById?id=1
{"code":"0","message":"您已被限流"}
D:\software\curl-7.71.1-win64-mingw\bin>curl http://localhost:8083/shop/findById?id=1
这是苹果
D:\software\curl-7.71.1-win64-mingw\bin>curl http://localhost:8083/shop/findById?id=1
这是苹果
```
- 快速调用/user/findById接口2次，发现第2次被限流了；快速调用/shop/findById接口2次，结果都正常，只针对user_route路由的接口生效，验证了代码的配置。

## 自定义API维度

- 通过上面一种限流方式可以看出，灵活性还不够。自定义API维度可以利用Sentinel提供的API自定义分组来限流。相比路由维度这是一种更为细粒度的方式。
- 下面来看实现自定义API维度的具体步骤。
- 1．导入Sentinel组件为Spring Cloud Gateway提供的适配模块依赖包，前面已经导入过了，这里就不再赘述了。直接进入下一个环节，新增自定义API维度的配置类SentinelApiGroupConfiguration。

- 依然是实例化SentinelGatewayFilter和SentinelGatewayBlockExceptionHandler对象，初始化限流规则，定义API分组，自定义限流后的界面显示，具体代码如下所示。

```
@Configuration // 标记为配置类
public class SentinelApiGroupConfiguration { // API分组维度限流配置类
    private final List<ViewResolver> viewResolvers;
    private final ServerCodecConfigurer serverCodecConfigurer;
    public SentinelApiGroupConfiguration(ObjectProvider<List<ViewResolver>> viewResolversProvider, // 构造函数
                                      ServerCodecConfigurer serverCodecConfigurer) {
        this.viewResolvers = viewResolversProvider.getIfAvailable(Collections::emptyList);
        this.serverCodecConfigurer = serverCodecConfigurer;
    }
    @PostConstruct
    public void initGatewayRules() {// 初始化限流规则
        Set<GatewayFlowRule> rules = new HashSet<>();
        GatewayFlowRule gatewayFlowRule = new GatewayFlowRule("user_api");
        gatewayFlowRule.setCount(1); // 限流阀值
        gatewayFlowRule.setIntervalSec(1); // 统计时间窗口（单位：秒），默认是1秒
        rules.add(gatewayFlowRule);
        GatewayRuleManager.loadRules(rules); // 载入规则
    }
    @PostConstruct
    public void initCustomizedApis() { //  自定义API分组
        Set<ApiDefinition> apiDefinitions = new HashSet<>();
        ApiDefinition apiDefinition = new ApiDefinition("user_api") // user_api是api分组名称
                .setPredicateItems(new HashSet<ApiPredicateItem>() { {
                add(new ApiPathPredicateItem().setPattern("/user/group/**") // 匹配路径
                  .setMatchStrategy(SentinelGatewayConstants.URL_MATCH_STRATEGY_PREFIX)); // 匹配策略，匹配前缀
            }});
        apiDefinitions.add(apiDefinition);
        GatewayApiDefinitionManager.loadApiDefinitions(apiDefinitions); // 载入API分组定义
    }
    @PostConstruct
    public void initBlockHandlers() {  // 自定义限流后的界面
        BlockRequestHandler blockRequestHandler = new BlockRequestHandler() {
            @Override
            public Mono<ServerResponse> handleRequest(ServerWebExchange serverWebExchange, Throwable throwable) {
                Map<String, String> result = new HashMap<>(); //  限流提示
                result.put("code", "0");
                result.put("message", "您已被限流");
                return ServerResponse.status(HttpStatus.OK).contentType(MediaType.APPLICATION_JSON_UTF8).
                        body(BodyInserters.fromObject(result));
            }
        };
        GatewayCallbackManager.setBlockHandler(blockRequestHandler);
    }
    @Bean
    @Order(Ordered.HIGHEST_PRECEDENCE)
    public SentinelGatewayBlockExceptionHandler sentinelGatewayBlockExceptionHandler() { // 配置限流异常处理器
        return new SentinelGatewayBlockExceptionHandler(viewResolvers, serverCodecConfigurer);
    }
    @Bean
    @Order(Ordered.HIGHEST_PRECEDENCE)
    public GlobalFilter sentinelGatewayFilter() { //初始化一个限流的过滤器
        return new SentinelGatewayFilter();
    }
}
```
> 注意：匹配路径不仅可以使用通配符，如/user/group/**，也可以固定某个地址，如/user/group/findById，如果是固定的地址，也无需再使用setMatchStrategy方法了。

- 2．为了看到API分组更清晰的效果，新增/user/group/findById接口，代码如下所示。

```
@RequestMapping("/user/group/findById")
public String groupFindById(@RequestParam("id") Integer id){ // 根据id查询用户信息的方法 -- 为了测试API分组新增的方法
	return userInfo.getOrDefault(id,null);
}
```


- 现在可以使用curl命令调用/user/group/findById和/user/findById接口，分别快速调用2次结果如下所示。

```
D:\software\curl-7.71.1-win64-mingw\bin>curl http://localhost:8083/user/group/findById?id=1
ZhangSan
D:\software\curl-7.71.1-win64-mingw\bin>curl http://localhost:8083/user/group/findById?id=1
{"code":"0","message":"您已被限流"}
D:\software\curl-7.71.1-win64-mingw\bin>curl http://localhost:8083/user/findById?id=1
ZhangSan
D:\software\curl-7.71.1-win64-mingw\bin>curl http://localhost:8083/user/findById?id=1
ZhangSan
```
- /user/group/findById接口地址是符合API分组匹配规则的，在调用第2次时被限流了。/user/findById接口地址不符合API分组匹配规则，所以快速调用时没有被限流。

- 本文是《Spring Cloud Alibaba微服务实战》书摘之一，如有兴趣可购买书籍。[天猫](https://detail.tmall.com/item.htm?spm=a230r.1.14.40.4d013ed4NkvyPZ&id=650584628890&ns=1&abbucket=3)、[京东](https://item.jd.com/13365970.html)、[当当](http://product.dangdang.com/29275400.html)。书中内容有任何问题，可在本博客下留言，或者到[https://github.com/1030907690](https://github.com/1030907690)提issues。