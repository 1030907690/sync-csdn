---
layout:					post
title:					"Spring MVC(Boot) Servlet 3.0异步处理，DeferredResult和Callable（续篇）"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 上篇[Spring MVC(Boot) Servlet 3.0异步处理，DeferredResult和Callable](https://blog.csdn.net/baidu_19473529/article/details/123596792)，我把`WebMvcConfig` 代码(继承WebMvcConfigurationSupport )加入项目后，会报冲突的问题。如下所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e4515955077bf2ab21399d0b30d23f0a.png)

>- requestMappingHandlerMapping: defined by method 'requestMappingHandlerMapping' in class path resource [com/works/framework/config/WebMvcConfig.class]
	- controllerEndpointHandlerMapping: defined by method 'controllerEndpointHandlerMapping' in class path resource [org/springframework/boot/actuate/autoconfigure/endpoint/web/servlet/WebMvcEndpointManagementContextConfiguration.class]

## 意外发现
- 我找到创建`requestMappingHandlerMapping`的地方是`WebMvcAutoConfiguration`。这块是Spring Boot自动装配的代码。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7fbcee2be31b189188173003a1166137.png)

- 我想`requestMappingHandlerMapping`框架自动配置了，那异步可以自动配置吗？
- 于是我搜索关键字`configureAsyncSupport`，还真的有自动配置异步的方法。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a2b2ac942ea5e1f4e7a27d2b54cb286b.png)
- 只要有Bean的名称是`TaskExecutionAutoConfiguration.APPLICATION_TASK_EXECUTOR_BEAN_NAME`并且是属于`AsyncTaskExecutor`的对象，那就能自动配置异步处理的线程池了。


- 另外，`TaskExecutionAutoConfiguration`是自动配置线程池的配置类。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/12759470a977dfb93db88d1a8ec2e34c.png)
- 只要有对应的配置，就可以初始化线程池和异步，可以看出`Spring Boot`在约定配置这块很智能。

## 结论
-  那么`Spring MVC(Boot) Servlet 3.0异步处理，Callable方式`就有`3`种方案了。
	- 继承`WebMvcConfigurationSupport` 。
	- 实现 `WebMvcConfigurer` 接口。
	- 创建Bean的名称是`TaskExecutionAutoConfiguration.APPLICATION_TASK_EXECUTOR_BEAN_NAME`并且是属于`AsyncTaskExecutor`的对象。

- 我直接在我创建线程池的地方增加了一个BeanName。代码如下

```java
	...省略...
	@Bean(name = {"threadPoolTaskExecutor",TaskExecutionAutoConfiguration.APPLICATION_TASK_EXECUTOR_BEAN_NAME})
    public ThreadPoolTaskExecutor threadPoolTaskExecutor() {

        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setMaxPoolSize(maxPoolSize);
        executor.setCorePoolSize(corePoolSize);
        executor.setQueueCapacity(queueCapacity);
        executor.setKeepAliveSeconds(keepAliveSeconds);
        // 线程池对拒绝任务(无线程可用)的处理策略 ，CallerRunsPolicy 如果没有线程了，用主线程
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.setThreadNamePrefix("taskExecutor-");
        return executor;
    }
	...省略...
```
