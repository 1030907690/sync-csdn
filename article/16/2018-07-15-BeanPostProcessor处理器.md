---
layout:					post
title:					"BeanPostProcessor处理器"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
####一、简介
- BeanPostProcessor处理器是Spring开放式架构中必不可少的亮点之一，给足用户权限根据自己的业务需求去更改或者扩展Spring，当然除了BeanPostProcessor外还有其他PostProcessor。BeanPostProcessor在调用初始化方法前及调用初始化方法只会分别调用它的postProcessBeforeInitialization和postProcessAfterInitialization方法，用户可以根据自己的业务需求做相应的处理。

####二、使用
- 先来看看BeanPostProcessor接口

```
public interface BeanPostProcessor {

	/**
	 * 可以对Bean在实例化之前添加一些逻辑处理  
	 */
	Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException;

	/**
	 * 可以对bean在实例化之后添加一些逻辑处理 
	 */
	Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException;

}

```
- 代码例子:CustomBeanPostProcessor.java

```
package com.zzq.core.test.processor;

import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;
import com.zzq.core.test.entity.MyTestBean;

/**
 * BeanPostProcessor接口的作用是在Spring容器完成Bean实例化前后可以添加一些自己的逻辑处理，我们可以定义一个或者多个BeanPostProcessor接口的实现。
 * spring有内置的 ApplicationContextAwareProcessor例子
 * */
public class CustomBeanPostProcessor implements BeanPostProcessor{

	@Override
	public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
		// TODO Auto-generated method stub
		//System.out.println("Bean在实例化之前添加一些逻辑处理 ");
		 System.out.println("对象" + beanName + "开始实例化");  
		return bean;
	}

	@Override
	public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
		// TODO Auto-generated method stub
		//System.out.println("Bean 实例化之后进行的处理 ");
		  System.out.println("对象" + beanName + "实例化完成" + bean);  
		if(bean instanceof MyTestBean){
			MyTestBean myTestBean = (MyTestBean)bean;
			myTestBean.setName("zhangSan");
		}
		return bean;
	}

}
```
spring-base.xml 配置：

```
 
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:aop="http://www.springframework.org/schema/aop"
      xmlns:tx="http://www.springframework.org/schema/tx"
      xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd  http://www.springframework.org/schema/aop
        http://www.springframework.org/schema/aop/spring-aop-3.0.xsd"

	 
	 >
  
 
    	
  
    <bean id ="myTestBean" class= "com.zzq.core.test.entity.MyTestBean" >
      
    </bean>
    
      <bean id ="customBeanPostProcessor" class= "com.zzq.core.test.processor.CustomBeanPostProcessor" ></bean>
    
 
</beans>
 
```
MyTestBean.java

```
package com.zzq.core.test.entity;

public class MyTestBean {

	private String name;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
	
	
	
}

```
最后运行：

```
package com.zzq.core.test;

import org.springframework.context.support.ClassPathXmlApplicationContext;

import com.zzq.core.test.entity.MyTestBean;

public class BootStrap {
	
	public static void main(String[] args) {
		ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext( "spring-base.xml");
		
		System.out.println(context.getBean("myTestBean") +  "--" + ((MyTestBean)context.getBean("myTestBean")).getName());
		
		 
	}

}

```
- 最后可以看到对象属性值在调用postProcessAfterInitialization后被改变。
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/86c3568015aa4c71fecbd728516b175d.png)

####三、源码分析
- 肯定是从ClassPathXmlApplicationContext看起，然后从构造方法进入AbstractApplicationContext refresh方法->finishBeanFactoryInitialization方法->AbstractBeanFactory getBean方法-> doGetBean方法

-> AbstractAutowireCapableBeanFactory createBean方法
```
protected Object createBean(String beanName, RootBeanDefinition mbd, Object[] args) throws BeanCreationException {
		if (logger.isDebugEnabled()) {
			logger.debug("Creating instance of bean '" + beanName + "'");
		}
		// Make sure bean class is actually resolved at this point.
		//锁定class ，根据class属性或者根据className来解析Class
		resolveBeanClass(mbd, beanName);

		// Prepare method overrides.
		try {
			//验证及准备覆盖的方法
			mbd.prepareMethodOverrides();
		}
		catch (BeanDefinitionValidationException ex) {
			throw new BeanDefinitionStoreException(mbd.getResourceDescription(),
					beanName, "Validation of method overrides failed", ex);
		}

		try {
			// 给BeanPostProcessors一个机会返回代理来替代真正的实例
			// Give BeanPostProcessors a chance to return a proxy instead of the target bean instance.
			Object bean = resolveBeforeInstantiation(beanName, mbd);
			if (bean != null) {
				return bean;
			}
		}
		catch (Throwable ex) {
			throw new BeanCreationException(mbd.getResourceDescription(), beanName,
					"BeanPostProcessor before instantiation of bean failed", ex);
		}
			
		
		  // 重头戏，创建 bean
		Object beanInstance = doCreateBean(beanName, mbd, args);
		if (logger.isDebugEnabled()) {
			logger.debug("Finished creating instance of bean '" + beanName + "'");
		}
		return beanInstance;
	}
```
-> doCreateBean方法
```
protected Object doCreateBean(final String beanName, final RootBeanDefinition mbd, final Object[] args) {
		// Instantiate the bean.
		BeanWrapper instanceWrapper = null;
		if (mbd.isSingleton()) {
			instanceWrapper = this.factoryBeanInstanceCache.remove(beanName);
		}
		if (instanceWrapper == null) {
			 // 说明不是 FactoryBean，这里实例化 Bean，这里非常关键，细节之后再说
			instanceWrapper = createBeanInstance(beanName, mbd, args);
		}
		// 这个就是 Bean 里面的 我们定义的类 的实例，很多地方我描述成 "bean 实例"
		final Object bean = (instanceWrapper != null ? instanceWrapper.getWrappedInstance() : null);
		 // 类型
		Class<?> beanType = (instanceWrapper != null ? instanceWrapper.getWrappedClass() : null);

		// Allow post-processors to modify the merged bean definition.
		  // 建议跳过吧，涉及接口：MergedBeanDefinitionPostProcessor
		synchronized (mbd.postProcessingLock) {
			if (!mbd.postProcessed) {
				   // MergedBeanDefinitionPostProcessor 
				applyMergedBeanDefinitionPostProcessors(mbd, beanType, beanName);
				mbd.postProcessed = true;
			}
		}

		// Eagerly cache singletons to be able to resolve circular references
		// even when triggered by lifecycle interfaces like BeanFactoryAware.
		 // 下面这块代码是为了解决循环依赖的问题，以后有时间，我再对循环依赖这个问题进行解析吧
		boolean earlySingletonExposure = (mbd.isSingleton() && this.allowCircularReferences &&
				isSingletonCurrentlyInCreation(beanName));
		if (earlySingletonExposure) {
			if (logger.isDebugEnabled()) {
				logger.debug("Eagerly caching bean '" + beanName +
						"' to allow for resolving potential circular references");
			}
			addSingletonFactory(beanName, new ObjectFactory<Object>() {
				public Object getObject() throws BeansException {
					return getEarlyBeanReference(beanName, mbd, bean);
				}
			});
		}

		// Initialize the bean instance.
		Object exposedObject = bean;
		try {
			 // 这一步也是非常关键的，这一步负责属性装配，因为前面的实例只是实例化了，并没有设值，这里就是设值
			populateBean(beanName, mbd, instanceWrapper);
			if (exposedObject != null) {
				 // 记得 init-method 吗还有 InitializingBean 接口还有 BeanPostProcessor 接口
		         // 这里就是处理 bean 初始化完成后的各种回调
				exposedObject = initializeBean(beanName, exposedObject, mbd);
			}
		}
		catch (Throwable ex) {
			if (ex instanceof BeanCreationException && beanName.equals(((BeanCreationException) ex).getBeanName())) {
				throw (BeanCreationException) ex;
			}
			else {
				throw new BeanCreationException(mbd.getResourceDescription(), beanName, "Initialization of bean failed", ex);
			}
		}

		if (earlySingletonExposure) {
			Object earlySingletonReference = getSingleton(beanName, false);
			if (earlySingletonReference != null) {
				if (exposedObject == bean) {
					exposedObject = earlySingletonReference;
				}
				else if (!this.allowRawInjectionDespiteWrapping && hasDependentBean(beanName)) {
					String[] dependentBeans = getDependentBeans(beanName);
					Set<String> actualDependentBeans = new LinkedHashSet<String>(dependentBeans.length);
					for (String dependentBean : dependentBeans) {
						if (!removeSingletonIfCreatedForTypeCheckOnly(dependentBean)) {
							actualDependentBeans.add(dependentBean);
						}
					}
					if (!actualDependentBeans.isEmpty()) {
						throw new BeanCurrentlyInCreationException(beanName,
								"Bean with name '" + beanName + "' has been injected into other beans [" +
								StringUtils.collectionToCommaDelimitedString(actualDependentBeans) +
								"] in its raw version as part of a circular reference, but has eventually been " +
								"wrapped. This means that said other beans do not use the final version of the " +
								"bean. This is often the result of over-eager type matching - consider using " +
								"'getBeanNamesOfType' with the 'allowEagerInit' flag turned off, for example.");
					}
				}
			}
		}

		// Register bean as disposable.
		try {
			registerDisposableBeanIfNecessary(beanName, bean, mbd);
		}
		catch (BeanDefinitionValidationException ex) {
			throw new BeanCreationException(mbd.getResourceDescription(), beanName, "Invalid destruction signature", ex);
		}

		return exposedObject;
	}
```
->initializeBean方法

```
protected Object initializeBean(final String beanName, final Object bean, RootBeanDefinition mbd) {
		if (System.getSecurityManager() != null) {
			AccessController.doPrivileged(new PrivilegedAction<Object>() {
				public Object run() {
					invokeAwareMethods(beanName, bean);
					return null;
				}
			}, getAccessControlContext());
		}
		else {
			 // 如果 bean 实现了 BeanNameAware、BeanClassLoaderAware 或 BeanFactoryAware 接口，回调
			invokeAwareMethods(beanName, bean);
		}

		Object wrappedBean = bean;
		if (mbd == null || !mbd.isSynthetic()) {
			// BeanPostProcessor 的 postProcessBeforeInitialization 回调,应用后处理器
			wrappedBean = applyBeanPostProcessorsBeforeInitialization(wrappedBean, beanName);
		}

		try {
			  // 处理 bean 中定义的 init-method，
		      // 或者如果 bean 实现了 InitializingBean 接口，调用 afterPropertiesSet() 方法
			invokeInitMethods(beanName, wrappedBean, mbd);
		}
		catch (Throwable ex) {
			throw new BeanCreationException(
					(mbd != null ? mbd.getResourceDescription() : null),
					beanName, "Invocation of init method failed", ex);
		}

		if (mbd == null || !mbd.isSynthetic()) {
			 // BeanPostProcessor 的 postProcessAfterInitialization 回调，,应用后处理器
			wrappedBean = applyBeanPostProcessorsAfterInitialization(wrappedBean, beanName);
		}
		return wrappedBean;
	}
```
applyBeanPostProcessorsBeforeInitialization方法
```
public Object applyBeanPostProcessorsBeforeInitialization(Object existingBean, String beanName)
			throws BeansException {

		Object result = existingBean;
		for (BeanPostProcessor beanProcessor : getBeanPostProcessors()) {
			result = beanProcessor.postProcessBeforeInitialization(result, beanName);
			if (result == null) {
				return result;
			}
		}
		return result;
	}
```
applyBeanPostProcessorsAfterInitialization 方法
```
public Object applyBeanPostProcessorsAfterInitialization(Object existingBean, String beanName)
			throws BeansException {

		Object result = existingBean;
		for (BeanPostProcessor beanProcessor : getBeanPostProcessors()) {
			result = beanProcessor.postProcessAfterInitialization(result, beanName);
			if (result == null) {
				return result;
			}
		}
		return result;
	}
```



- applyBeanPostProcessorsBeforeInitialization和applyBeanPostProcessorsAfterInitialization方法分别调用实现BeanPostProcessor处理器接口的类里面的postProcessBeforeInitialization和postProcessAfterInitialization方法

到这儿基本结束了，另外文章代码或者我理解有误的地方,希望能批评指出。