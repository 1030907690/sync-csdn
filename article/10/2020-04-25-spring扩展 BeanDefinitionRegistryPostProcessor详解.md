---
layout:					post
title:					"spring扩展 BeanDefinitionRegistryPostProcessor详解"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
### 简介
- 首先引出一个问题，怎样的bean会被交给spring初始化？
> 一般而言Spring容器启动的过程中，解析配置文件  java config等等，会将Bean解析成Spring内部的BeanDefinition结构；试想一下如果我们能直接给spring BeanDefinition对象,这个bean交给spring去初始化。
- 上面说的`直接给spring BeanDefinition对象,这个bean交给spring去初始化`的确可以这样做的。实现`BeanDefinitionRegistryPostProcessor`接口，`自定义标签`都可以实现一种更为灵活的注册bean对象;自定义标签的文章可以参考[spring自定义标签](https://blog.csdn.net/baidu_19473529/article/details/96509442)；如果要注册bean可以参考`AbstractBeanDefinitionParser.java`中的`registerBeanDefinition(holder, parserContext.getRegistry());`其他的我就不过多赘述了。
- mybatis `MapperScannerConfigurer`实现了`BeanDefinitionRegistryPostProcessor`接口动态的注册mapper，我们使用起来才这么爽。


### 使用
- 创建一个实体类对象RegistryBeanSample.java

```java
package com.zzq.core.beaneefinitionregistrypostprocessor;

public class RegistryBeanSample {
	
	private String name;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
}

```

- 实现`BeanDefinitionRegistryPostProcessor`接口的类BeanDefinitionRegistryPostProcessorSample.java

```java
package com.zzq.core.beaneefinitionregistrypostprocessor;

import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.ConfigurableListableBeanFactory;
import org.springframework.beans.factory.support.BeanDefinitionRegistry;
import org.springframework.beans.factory.support.BeanDefinitionRegistryPostProcessor;
import org.springframework.beans.factory.support.GenericBeanDefinition;
import org.springframework.stereotype.Component;

@Component
public class BeanDefinitionRegistryPostProcessorSample implements BeanDefinitionRegistryPostProcessor {

	@Override
	public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) throws BeansException {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) throws BeansException {
		// GenericBeanDefinition是BeanDefinition其中一个实现
		GenericBeanDefinition beanDefinition = new GenericBeanDefinition();
		// 设置初始化对象的类
		beanDefinition.setBeanClass(RegistryBeanSample.class);
		// 注册进spring ioc容器
		registry.registerBeanDefinition("registryBeanSample", beanDefinition);
	}

	
	
}

```
- 因为`BeanDefinitionRegistryPostProcessor`是继承`BeanFactoryPostProcessor`后处理器的，所以要实现`postProcessBeanFactory`方法，这里的话我们关注点不在这儿，暂时忽略不管；
- <font color="red">调用`registry.registerBeanDefinition("registryBeanSample", beanDefinition);`会进入`DefaultListableBeanFactory#registerBeanDefinition`方法，把bean信息放到`beanDefinitionMap`中，spring会根据这些信息生成对应的对象。</font>
- 然后下一步就测试下spring容器中有没有这个bean，我用了`ApplicationListener<ContextRefreshedEvent>`启动完就会触发。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/680c131facc97f471496442b96486c4d.png)
- 测试是成功的;当然在`BeanDefinitionRegistryPostProcessorSample#postProcessBeanDefinitionRegistry`方法中我只是简单的示例，并不够动态；像mybatis的`MapperScannerConfigurer`做的就比较动态了。


### 源码分析
- 不管是spring项目、spring mvc或者spring boot项目都会进入`AbstractApplicationContext#refresh`方法，我们就从这个地方看起。`BeanDefinitionRegistryPostProcessor`接口源码，主要关注`invokeBeanFactoryPostProcessors`就可以了

```java
public void refresh() throws BeansException, IllegalStateException {
	 .........省略..........
				// Invoke factory processors registered as beans in the context.
				// 调用 BeanFactoryPostProcessor 各个实现类的 postProcessBeanFactory(factory) 方法
				invokeBeanFactoryPostProcessors(beanFactory);

	 ..........省略............
	}
```
- `invokeBeanFactoryPostProcessors`方法源码
```java
protected void invokeBeanFactoryPostProcessors(ConfigurableListableBeanFactory beanFactory) {
		// Invoke BeanDefinitionRegistryPostProcessors first, if any.
		Set<String> processedBeans = new HashSet<String>();
		if (beanFactory instanceof BeanDefinitionRegistry) {
			BeanDefinitionRegistry registry = (BeanDefinitionRegistry) beanFactory;
			List<BeanFactoryPostProcessor> regularPostProcessors = new LinkedList<BeanFactoryPostProcessor>();
			List<BeanDefinitionRegistryPostProcessor> registryPostProcessors =
					new LinkedList<BeanDefinitionRegistryPostProcessor>();
			//getBeanFactoryPostProcessors()大部分情况下里面元素是空的,所以主要还是走下面beanFactory.getBeanNamesForType方法得到处理器
			for (BeanFactoryPostProcessor postProcessor : getBeanFactoryPostProcessors()) {
				if (postProcessor instanceof BeanDefinitionRegistryPostProcessor) {
					BeanDefinitionRegistryPostProcessor registryPostProcessor =
							(BeanDefinitionRegistryPostProcessor) postProcessor;
					registryPostProcessor.postProcessBeanDefinitionRegistry(registry);
					registryPostProcessors.add(registryPostProcessor);
				}
				else {
					regularPostProcessors.add(postProcessor);
				}
			}
			
			//目前看到mybatis框架  MapperScannerConfigurer实现BeanDefinitionRegistryPostProcessor接口  、spring的ConfigurationClassPostProcessor
			Map<String, BeanDefinitionRegistryPostProcessor> beanMap =
					beanFactory.getBeansOfType(BeanDefinitionRegistryPostProcessor.class, true, false);
			List<BeanDefinitionRegistryPostProcessor> registryPostProcessorBeans =
					new ArrayList<BeanDefinitionRegistryPostProcessor>(beanMap.values());
			OrderComparator.sort(registryPostProcessorBeans);
			for (BeanDefinitionRegistryPostProcessor postProcessor : registryPostProcessorBeans) {
				postProcessor.postProcessBeanDefinitionRegistry(registry);
			}
			invokeBeanFactoryPostProcessors(registryPostProcessors, beanFactory);
			invokeBeanFactoryPostProcessors(registryPostProcessorBeans, beanFactory);
			invokeBeanFactoryPostProcessors(regularPostProcessors, beanFactory);
			processedBeans.addAll(beanMap.keySet());
		}
		else {
			// Invoke factory processors registered with the context instance.
			invokeBeanFactoryPostProcessors(getBeanFactoryPostProcessors(), beanFactory);
		}

		// Do not initialize FactoryBeans here: We need to leave all regular beans
		// uninitialized to let the bean factory post-processors apply to them!
		//根据BeanFactoryPostProcessor接口得到它的实现类
		String[] postProcessorNames =
				beanFactory.getBeanNamesForType(BeanFactoryPostProcessor.class, true, false);

		// Separate between BeanFactoryPostProcessors that implement PriorityOrdered,
		// Ordered, and the rest.
		//将BeanFactoryPostProcessor处理器分成几种来执行 priorityOrderedPostProcessors  orderedPostProcessorNames  nonOrderedPostProcessorNames
		List<BeanFactoryPostProcessor> priorityOrderedPostProcessors = new ArrayList<BeanFactoryPostProcessor>();
		List<String> orderedPostProcessorNames = new ArrayList<String>();
		List<String> nonOrderedPostProcessorNames = new ArrayList<String>();
		for (String ppName : postProcessorNames) {
			if (processedBeans.contains(ppName)) {
				// skip - already processed in first phase above
			}
			else if (isTypeMatch(ppName, PriorityOrdered.class)) {
				priorityOrderedPostProcessors.add(beanFactory.getBean(ppName, BeanFactoryPostProcessor.class));
			}
			else if (isTypeMatch(ppName, Ordered.class)) {
				orderedPostProcessorNames.add(ppName);
			}
			else {
				nonOrderedPostProcessorNames.add(ppName);
			}
		}

		// First, invoke the BeanFactoryPostProcessors that implement PriorityOrdered.
		OrderComparator.sort(priorityOrderedPostProcessors);
		invokeBeanFactoryPostProcessors(priorityOrderedPostProcessors, beanFactory);

		// Next, invoke the BeanFactoryPostProcessors that implement Ordered.
		List<BeanFactoryPostProcessor> orderedPostProcessors = new ArrayList<BeanFactoryPostProcessor>();
		for (String postProcessorName : orderedPostProcessorNames) {
			orderedPostProcessors.add(getBean(postProcessorName, BeanFactoryPostProcessor.class));
		}
		OrderComparator.sort(orderedPostProcessors);
		invokeBeanFactoryPostProcessors(orderedPostProcessors, beanFactory);

		// Finally, invoke all other BeanFactoryPostProcessors.
		//最后，调用所有其他后处理器。
		List<BeanFactoryPostProcessor> nonOrderedPostProcessors = new ArrayList<BeanFactoryPostProcessor>();
		for (String postProcessorName : nonOrderedPostProcessorNames) {
			nonOrderedPostProcessors.add(getBean(postProcessorName, BeanFactoryPostProcessor.class));
		}
	
		invokeBeanFactoryPostProcessors(nonOrderedPostProcessors, beanFactory);
	}
```
- 然后我们稍微debug`beanFactory.getBeansOfType(BeanDefinitionRegistryPostProcessor.class, true, false);`这段代码。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9705acd07139cdc73a0fab021683b149.png)
- 继续跟进`DefaultListableBeanFactory#getBeanNamesForType`方法
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e9860fc478b689c9f6865bfc0ce68668.png)
- 进入`DefaultListableBeanFactory#doGetBeanNamesForType`方法
- 获取到所有已注册的`BeanDefinition`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/12060f1ff1b207431f62290a04683ac5.png)
- 匹配成功的会加入`result`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fc6055937a7e4174575b334b6b212db0.png)
- 最后返回`result`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dc0def91cb2939e34a7ae7dcfb163db3.png)
- 然后回过头来看DefaultListableBeanFactory#getBeansOfType方法；result会返回初始化好的bean

```java
	public <T> Map<String, T> getBeansOfType(Class<T> type, boolean includeNonSingletons, boolean allowEagerInit)
			throws BeansException {

		String[] beanNames = getBeanNamesForType(type, includeNonSingletons, allowEagerInit);
		Map<String, T> result = new LinkedHashMap<String, T>(beanNames.length);
		for (String beanName : beanNames) {
			try {
				//getBean(beanName, type) bean如果没有初始化 会在这儿初始化
				result.put(beanName, getBean(beanName, type));
			}
			catch (BeanCreationException ex) {
				Throwable rootCause = ex.getMostSpecificCause();
				if (rootCause instanceof BeanCurrentlyInCreationException) {
					BeanCreationException bce = (BeanCreationException) rootCause;
					if (isCurrentlyInCreation(bce.getBeanName())) {
						if (this.logger.isDebugEnabled()) {
							this.logger.debug("Ignoring match to currently created bean '" + beanName + "': " +
									ex.getMessage());
						}
						onSuppressedException(ex);
						// Ignore: indicates a circular reference when autowiring constructors.
						// We want to find matches other than the currently created bean itself.
						continue;
					}
				}
				throw ex;
			}
		}
		return result;
	}
```
- 在回过来看看`beanFactory.getBeansOfType(BeanDefinitionRegistryPostProcessor.class, true, false);`的结果
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/164d176e1f03a8172ffeaf96f3eb36e7.png)
-  下面看看它拿到这个`beanMap`干了什么?
- 回调实现了`BeanDefinitionRegistryPostProcessor`接口的类，把`registry`传进去
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6ad52d6d6c292b0abb59eb8f36e9f378.png)
- 下一步就会进我们自定义那个类了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f07997ffe338a8643f8d693bc8c9e15a.png)
- 最后就是注册一个`BeanDefinition`进去了；`DefaultListableBeanFactory#registerBeanDefinition`方法
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/68f994dabad2afe6f546b2a0bf91b777.png)
- 这样我们自定义的bean就交给了spring了。本人水平有限，如果文章有误的地方，希望批评指正，感谢您的观看。


