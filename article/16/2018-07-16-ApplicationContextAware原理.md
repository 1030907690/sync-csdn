---
layout:					post
title:					"ApplicationContextAware原理"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 1、紧接上文[BeanPostProcessor处理器](https://blog.csdn.net/baidu_19473529/article/details/81057974) 的应用，ApplicationContextAware也可以说是spring框架中对BeanPostProcessor的一个应用，还包括一些其他的Aware,如BeanFactoryAware、ResourceLoaderAware、ServletContextAware等等。

- 2 、先来一段代码看看

```
@Component
    public class BeansUtils implements ApplicationContextAware {

        private static ApplicationContext context;

        public static <T> T getBean(Class<T> bean) {
            return context.getBean(bean);
        }
        public static <T> T getBean(String var1, @Nullable Class<T> var2){
            return context.getBean(var1, var2);
        }

        public static ApplicationContext getContext() {
            return context;
        }

        @Override
        public void setApplicationContext(ApplicationContext context) throws BeansException {
            BeansUtils.context = context;
        }
    }
```
- 2.1  这样的代码相信用过spring框架的人大部分都知道；通过这样的代码，就可以得到spring容器的一些基础功能,可以通过getBean方法获取容器中得对象等等。那么它的原理是怎样实现的呢？毋庸置虑是肯定setApplicationContext把ApplicationContext设置进来的；下面就看看具体的流程。
- 3、查看源码
- 3.1 首先还是定位到入口类ClassPathXmlApplicationContext->AbstractApplicationContext refresh方法 ->prepareBeanFactory方法

```
protected void prepareBeanFactory(ConfigurableListableBeanFactory beanFactory) {
		// Tell the internal bean factory to use the context's class loader etc.
		 // 设置 BeanFactory 的类加载器，我们知道 BeanFactory 需要加载类，也就需要类加载器，
		   // 这里设置为当前 ApplicationContext 的类加载器
		beanFactory.setBeanClassLoader(getClassLoader());
		 // 设置 BeanExpressionResolver
		beanFactory.setBeanExpressionResolver(new StandardBeanExpressionResolver());
		beanFactory.addPropertyEditorRegistrar(new ResourceEditorRegistrar(this, getEnvironment()));

		// Configure the bean factory with context callbacks.
		 // 添加一个 BeanPostProcessor，这个 processor 比较简单，
		   // 实现了 Aware 接口的几个特殊的 beans 在初始化的时候，这个 processor 负责回调
		beanFactory.addBeanPostProcessor(new ApplicationContextAwareProcessor(this));
		 // 下面几行的意思就是，如果某个 bean 依赖于以下几个接口的实现类，在自动装配的时候忽略它们，
		   // Spring 会通过其他方式来处理这些依赖。
		beanFactory.ignoreDependencyInterface(EnvironmentAware.class);
		beanFactory.ignoreDependencyInterface(EmbeddedValueResolverAware.class);
		beanFactory.ignoreDependencyInterface(ResourceLoaderAware.class);
		beanFactory.ignoreDependencyInterface(ApplicationEventPublisherAware.class);
		beanFactory.ignoreDependencyInterface(MessageSourceAware.class);
		beanFactory.ignoreDependencyInterface(ApplicationContextAware.class);

		// BeanFactory interface not registered as resolvable type in a plain factory.
		// MessageSource registered (and found for autowiring) as a bean.
		
		beanFactory.registerResolvableDependency(BeanFactory.class, beanFactory);
		beanFactory.registerResolvableDependency(ResourceLoader.class, this);
		beanFactory.registerResolvableDependency(ApplicationEventPublisher.class, this);
		beanFactory.registerResolvableDependency(ApplicationContext.class, this);

		// Detect a LoadTimeWeaver and prepare for weaving, if found.
		
		if (beanFactory.containsBean(LOAD_TIME_WEAVER_BEAN_NAME)) {
			beanFactory.addBeanPostProcessor(new LoadTimeWeaverAwareProcessor(beanFactory));
			// Set a temporary ClassLoader for type matching.
			beanFactory.setTempClassLoader(new ContextTypeMatchClassLoader(beanFactory.getBeanClassLoader()));
		}

		  /**
		    * 从下面几行代码我们可以知道，Spring 往往很 "智能" 就是因为它会帮我们默认注册一些有用的 bean，
		    * 我们也可以选择覆盖
		    */
		// Register default environment beans.
		 // 如果没有定义 "environment" 这个 bean，那么 Spring 会 "手动" 注册一个
		if (!beanFactory.containsLocalBean(ENVIRONMENT_BEAN_NAME)) {
			beanFactory.registerSingleton(ENVIRONMENT_BEAN_NAME, getEnvironment());
		}
		
		 // 如果没有定义 "systemProperties" 这个 bean，那么 Spring 会 "手动" 注册一个
		if (!beanFactory.containsLocalBean(SYSTEM_PROPERTIES_BEAN_NAME)) {
			beanFactory.registerSingleton(SYSTEM_PROPERTIES_BEAN_NAME, getEnvironment().getSystemProperties());
		}
		
		 // 如果没有定义 "systemEnvironment" 这个 bean，那么 Spring 会 "手动" 注册一个
		if (!beanFactory.containsLocalBean(SYSTEM_ENVIRONMENT_BEAN_NAME)) {
			beanFactory.registerSingleton(SYSTEM_ENVIRONMENT_BEAN_NAME, getEnvironment().getSystemEnvironment());
		}
	}

```

- 3.2 此次要关注的重点就是beanFactory.addBeanPostProcessor(new ApplicationContextAwareProcessor(this)); ，spring源码里面将ApplicationContextAwareProcessor加入到BeanPostProcessor处理器里面了，并且传的是一个ApplicationContext类型参数进去。
- 3.3 再来看看ApplicationContextAwareProcessor里面做了什么事儿。

```
/*
 * Copyright 2002-2012 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.springframework.context.support;

import java.security.AccessControlContext;
import java.security.AccessController;
import java.security.PrivilegedAction;

import org.springframework.beans.BeansException;
import org.springframework.beans.factory.Aware;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.beans.factory.config.ConfigurableBeanFactory;
import org.springframework.context.ApplicationContextAware;
import org.springframework.context.ApplicationEventPublisherAware;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.EmbeddedValueResolverAware;
import org.springframework.context.EnvironmentAware;
import org.springframework.context.MessageSourceAware;
import org.springframework.context.ResourceLoaderAware;
import org.springframework.util.StringValueResolver;

/**
 * {@link org.springframework.beans.factory.config.BeanPostProcessor}
 * implementation that passes the ApplicationContext to beans that
 * implement the {@link EnvironmentAware}, {@link EmbeddedValueResolverAware},
 * {@link ResourceLoaderAware}, {@link ApplicationEventPublisherAware},
 * {@link MessageSourceAware} and/or {@link ApplicationContextAware} interfaces.
 *
 * <p>Implemented interfaces are satisfied in order of their mention above.
 *
 * <p>Application contexts will automatically register this with their
 * underlying bean factory. Applications do not use this directly.
 *
 * @author Juergen Hoeller
 * @author Costin Leau
 * @author Chris Beams
 * @since 10.10.2003
 * @see org.springframework.context.EnvironmentAware
 * @see org.springframework.context.EmbeddedValueResolverAware
 * @see org.springframework.context.ResourceLoaderAware
 * @see org.springframework.context.ApplicationEventPublisherAware
 * @see org.springframework.context.MessageSourceAware
 * @see org.springframework.context.ApplicationContextAware
 * @see org.springframework.context.support.AbstractApplicationContext#refresh()
 */
class ApplicationContextAwareProcessor implements BeanPostProcessor {

	private final ConfigurableApplicationContext applicationContext;


	/**
	 * Create a new ApplicationContextAwareProcessor for the given context.
	 */
	//beanFactory.addBeanPostProcessor(new ApplicationContextAwareProcessor(this));调用此构造方法把ApplicationContext传过来
	public ApplicationContextAwareProcessor(ConfigurableApplicationContext applicationContext) {
		this.applicationContext = applicationContext;
	}

	
	//实例化之前进行的处理
	public Object postProcessBeforeInitialization(final Object bean, String beanName) throws BeansException {
		AccessControlContext acc = null;

		if (System.getSecurityManager() != null &&
				(bean instanceof EnvironmentAware || bean instanceof EmbeddedValueResolverAware ||
						bean instanceof ResourceLoaderAware || bean instanceof ApplicationEventPublisherAware ||
						bean instanceof MessageSourceAware || bean instanceof ApplicationContextAware)) {
			acc = this.applicationContext.getBeanFactory().getAccessControlContext();
		}

		if (acc != null) {
			AccessController.doPrivileged(new PrivilegedAction<Object>() {
				public Object run() {
					//给Aware的实现类set值进去
					invokeAwareInterfaces(bean);
					return null;
				}
			}, acc);
		}
		else {
			//给Aware的实现类set值进去
			invokeAwareInterfaces(bean);
		}

		return bean;
	}

	private void invokeAwareInterfaces(Object bean) {
		if (bean instanceof Aware) {
			if (bean instanceof EnvironmentAware) {
				((EnvironmentAware) bean).setEnvironment(this.applicationContext.getEnvironment());
			}
			if (bean instanceof EmbeddedValueResolverAware) {
				((EmbeddedValueResolverAware) bean).setEmbeddedValueResolver(
						new EmbeddedValueResolver(this.applicationContext.getBeanFactory()));
			}
			if (bean instanceof ResourceLoaderAware) {
				((ResourceLoaderAware) bean).setResourceLoader(this.applicationContext);
			}
			if (bean instanceof ApplicationEventPublisherAware) {
				((ApplicationEventPublisherAware) bean).setApplicationEventPublisher(this.applicationContext);
			}
			if (bean instanceof MessageSourceAware) {
				((MessageSourceAware) bean).setMessageSource(this.applicationContext);
			}
			//判读是否是属于ApplicationContextAware接口的类
			if (bean instanceof ApplicationContextAware) {
				//调用实现类的setApplicationContext方法把applicationContext set进去
				((ApplicationContextAware) bean).setApplicationContext(this.applicationContext);
			}
		}
	}

	//bean实例化之后
	public Object postProcessAfterInitialization(Object bean, String beanName) {
		return bean;
	}


	private static class EmbeddedValueResolver implements StringValueResolver {

		private final ConfigurableBeanFactory beanFactory;

		public EmbeddedValueResolver(ConfigurableBeanFactory beanFactory) {
			this.beanFactory = beanFactory;
		}

		public String resolveStringValue(String strVal) {
			return this.beanFactory.resolveEmbeddedValue(strVal);
		}
	}

}

```
- 3.4  我们都知道了实现了BeanPostProcessor处理器，可以在bean初始化前、后根据自己业务做一些事情(具体可参考拙作[BeanPostProcessor处理器](https://blog.csdn.net/baidu_19473529/article/details/81057974))；可以看到postProcessAfterInitialization只是返回bean而已，可以忽略它；关键在于postProcessBeforeInitialization方法里面，里面invokeAwareInterfaces方法是怎样都会走的,里面有这样一段代码((ApplicationContextAware) bean).setApplicationContext(this.applicationContext);这就是去调用具体实现类的setApplicationContext方法把applicationContext传进去了。其他Aware基本上也是这个道理。

到这儿基本结束了，另外文章代码或者我理解有误的地方,希望能批评指出。