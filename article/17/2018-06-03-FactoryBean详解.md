---
layout:					post
title:					"FactoryBean详解"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
####一、首先来看看FactoryBean与BeanFactory:
- 这个两个拼写起来很相似,比较容易搞混,是反过来的。

- FactoryBean ： 是一个Java Bean，但是它是一个能生产出当前对象的工厂Bean,它的实现和工厂模式及修饰器模式很像。
- BeanFactory:这就是一个Factory，是整个Spring IOC容器的核心内容,生产并存储很多的bean。

####二、应用

- 现在就建一个对象实现FactoryBean接口试试：

```

package test;

import org.springframework.beans.factory.FactoryBean;

/**
 * 
 * @author 
 */
public class MyTestBean implements FactoryBean<MyTestBean> {
	
	private String name;

	
	public String getName() {
		return name;
	}

	
	public void setName(String name) {
		this.name = name;
	}
	
//返回由FactoryBean创建的bean实例，如果isSingleton()返回true，则该实例会放到Spring容器中单实例缓存池中。
	@Override
	public MyTestBean getObject() throws Exception {
		MyTestBean bean = new MyTestBean();
		bean.setName("Tom");
		return bean;
	}

//返回FactoryBean创建的bean类型。 
	@Override
	public Class<?> getObjectType() {
		return  MyTestBean.class;
	}

	//返回由FactoryBean创建的bean实例的作用域是singleton还是prototype。  
	@Override
	public boolean isSingleton() {
		return true;
	}
	
	

}
```

- xml配置

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd "  >
  
    <bean id ="myTestBean" class= "test.MyTestBean" >  </bean>

</beans>
```
- 运行：

```
ApplicationContext xmlBeanFactory = new ClassPathXmlApplicationContext("spring-base.xml");
		
MyTestBean myTestBean = (MyTestBean) xmlBeanFactory.getBean("myTestBean");
System.out.println(myTestBean + "--" + myTestBean.getName());
```
- 这里MyTestBean实现了FactoryBean接口，这个时候我们getBean("myTestBean")得到的就是getObject()返回的对象(`注意:这个返回的对象不一定就是当前类的这个对象,也就是说可以不是MyTestBean对象,根据自己的需求可以是其他的`)，走FactoryBean它定义的getObject()方法;所以最后打印的name自然是Tom。

- 如果非要得到MyTestBean对象(就是不取getObject()返回的那个对象)可以在getBean的时候前面多加一个`"&"`。


####三、源码是如何实现的
 - 既然是getBean方法开始的,那么就从getBean看起。我的源码版本比较老,是spring 3.2.18.RELEASE,找到AbstractBeanFactory 229行左右doGetBean方法是从getBean方法调用过来的,这个方法也是初始化bean的过程

```
protected <T> T doGetBean(
			final String name, final Class<T> requiredType, final Object[] args, boolean typeCheckOnly)
			throws BeansException {

		// 获取一个 “正统的” beanName，处理两种情况，一个是前面说的 FactoryBean(前面带 "&")，
		   // 一个是别名问题，因为这个方法是 getBean，获取 Bean 用的，你要是传一个别名进来，是完全可以的
		final String beanName = transformedBeanName(name);//转换name
		
		 // 注意跟着这个，这个是返回值
		Object bean;

		// Eagerly check singleton cache for manually registered singletons.
		 // 检查下是不是已经创建过了
		Object sharedInstance = getSingleton(beanName);
		 // 这里说下 args 呗，虽然看上去一点不重要。前面我们一路进来的时候都是 getBean(beanName)，
		   // 所以 args 其实是 null 的，但是如果 args 不为空的时候，那么意味着调用方不是希望获取 Bean，而是创建 Bean
		if (sharedInstance != null && args == null) {
			if (logger.isDebugEnabled()) {
				if (isSingletonCurrentlyInCreation(beanName)) {
					logger.debug("Returning eagerly cached instance of singleton bean '" + beanName +
							"' that is not fully initialized yet - a consequence of a circular reference");
				}
				else {
					logger.debug("Returning cached instance of singleton bean '" + beanName + "'");
				}
			}
			// 下面这个方法：如果是普通 Bean 的话，直接返回 sharedInstance，
		      // 如果是 FactoryBean 的话，返回它创建的那个实例对象
		      // 此次FactoryBean 重点
			bean = getObjectForBeanInstance(sharedInstance, name, beanName, null);
		}

		else {
			// Fail if we're already creating this bean instance:
			// We're assumably within a circular reference.
			if (isPrototypeCurrentlyInCreation(beanName)) {
				// 当前线程已经创建过了此 beanName 的 prototype 类型的 bean，那么抛异常
				throw new BeanCurrentlyInCreationException(beanName);
			}

			// Check if bean definition exists in this factory.
			// 检查一下这个 BeanDefinition 在容器中是否存在
			BeanFactory parentBeanFactory = getParentBeanFactory();
			if (parentBeanFactory != null && !containsBeanDefinition(beanName)) {
				// Not found -> check parent.
				 // 如果当前容器不存在这个 BeanDefinition，试试父容器中有没有
				String nameToLookup = originalBeanName(name);
				if (args != null) {
					// Delegation to parent with explicit args.
					// 返回父容器的查询结果
					return (T) parentBeanFactory.getBean(nameToLookup, args);
				}
				else {
					// No args -> delegate to standard getBean method.
					return parentBeanFactory.getBean(nameToLookup, requiredType);
				}
			}

			if (!typeCheckOnly) {
				 // typeCheckOnly 为 false，将当前 beanName 放入一个 alreadyCreated 的 Set 集合中。
				markBeanAsCreated(beanName);
			}

			  /*
		       * 到这里的话，要准备创建 Bean 了，对于 singleton 的 Bean 来说，容器中还没创建过此 Bean；
		       * 对于 prototype 的 Bean 来说，本来就是要创建一个新的 Bean。
		       */
			try {
				final RootBeanDefinition mbd = getMergedLocalBeanDefinition(beanName);
				checkMergedBeanDefinition(mbd, beanName, args);

				// Guarantee initialization of beans that the current bean depends on.
			    // 先初始化依赖的所有 Bean
		         // 注意，这里的依赖指的是 depends-on 中定义的依赖
				String[] dependsOn = mbd.getDependsOn();
				if (dependsOn != null) {
					for (String dependsOnBean : dependsOn) {
						
						// if (isDependent(beanName, dep)) {
						 // 先初始化被依赖项
						getBean(dependsOnBean);
						 // 注册一下依赖关系
						registerDependentBean(dependsOnBean, beanName);
					}
				}

				// Create bean instance.
				// 创建 singleton 的实例
				if (mbd.isSingleton()) {
					sharedInstance = getSingleton(beanName, new ObjectFactory<Object>() {
						public Object getObject() throws BeansException {
							try {
								// 执行创建 Bean
								return createBean(beanName, mbd, args);
							}
							catch (BeansException ex) {
								// Explicitly remove instance from singleton cache: It might have been put there
								// eagerly by the creation process, to allow for circular reference resolution.
								// Also remove any beans that received a temporary reference to the bean.
								destroySingleton(beanName);
								throw ex;
							}
						}
					});
					bean = getObjectForBeanInstance(sharedInstance, name, beanName, mbd);
				}
				
				  // 创建 prototype 的实例
				else if (mbd.isPrototype()) {
					// It's a prototype -> create a new instance.
					Object prototypeInstance = null;
					try {
						beforePrototypeCreation(beanName);
						 // 执行创建 Bean
						prototypeInstance = createBean(beanName, mbd, args);
					}
					finally {
						afterPrototypeCreation(beanName);
					}
					bean = getObjectForBeanInstance(prototypeInstance, name, beanName, mbd);
				}
				 // 如果不是 singleton 和 prototype 的话，需要委托给相应的实现类来处理
				else {
					String scopeName = mbd.getScope();
					final Scope scope = this.scopes.get(scopeName);
					if (scope == null) {
						throw new IllegalStateException("No Scope registered for scope '" + scopeName + "'");
					}
					try {
						Object scopedInstance = scope.get(beanName, new ObjectFactory<Object>() {
							public Object getObject() throws BeansException {
								beforePrototypeCreation(beanName);
								try {
									  // 执行创建 Bean
									return createBean(beanName, mbd, args);
								}
								finally {
									afterPrototypeCreation(beanName);
								}
							}
						});
						bean = getObjectForBeanInstance(scopedInstance, name, beanName, mbd);
					}
					catch (IllegalStateException ex) {
						throw new BeanCreationException(beanName,
								"Scope '" + scopeName + "' is not active for the current thread; " +
								"consider defining a scoped proxy for this bean if you intend to refer to it from a singleton",
								ex);
					}
				}
			}
			catch (BeansException ex) {
				cleanupAfterBeanCreationFailure(beanName);
				throw ex;
			}
		}

		// Check if required type matches the type of the actual bean instance.
		  // 最后，检查一下类型对不对，不对的话就抛异常，对的话就返回了
		if (requiredType != null && bean != null && !requiredType.isAssignableFrom(bean.getClass())) {
			try {
				return getTypeConverter().convertIfNecessary(bean, requiredType);
			}
			catch (TypeMismatchException ex) {
				if (logger.isDebugEnabled()) {
					logger.debug("Failed to convert bean '" + name + "' to required type [" +
							ClassUtils.getQualifiedName(requiredType) + "]", ex);
				}
				throw new BeanNotOfRequiredTypeException(name, requiredType, bean.getClass());
			}
		}
		return (T) bean;
	}	
```
- 实现了FactoryBean的bean对象重点就在getObjectForBeanInstance方法 在 AbstractBeanFactory 1475行左右

```
protected Object getObjectForBeanInstance(
			Object beanInstance, String name, String beanName, RootBeanDefinition mbd) {
		
		
		// Don't let calling code try to dereference the factory if the bean isn't a factory.
		 //如果是对FactoryBean的解引用，但bean对象不是FactoryBean，抛出异常  
		//Dereference(解引用)：一个在C/C++中应用的比较多术语，在C++中，"*"是解引用符号,得到对象的值;"&"是引用符号,得到对象内存地址。
		//解引用：变量所指向的是所引用对象的本身数据，而不是对象的内存地址。
		if (BeanFactoryUtils.isFactoryDereference(name) && !(beanInstance instanceof FactoryBean)) {
			throw new BeanIsNotAFactoryException(transformedBeanName(name), beanInstance.getClass());
		}

		// Now we have the bean instance, which may be a normal bean or a FactoryBean.
		// If it's a FactoryBean, we use it to create a bean instance, unless the
		// caller actually wants a reference to the factory.
		 //如果Bean实例不是FactoryBean，或者指定名称是FactoryBean的解引用，也就是普通的bean调用，则直接返回当前的Bean实例    
		if (!(beanInstance instanceof FactoryBean) || BeanFactoryUtils.isFactoryDereference(name)) {
			return beanInstance;
		}

		//处理对FactoryBean的调用 
		Object object = null;
		if (mbd == null) {
			//从Bean工厂缓存中获取给定名称的实例对象  
			object = getCachedObjectForFactoryBean(beanName);
		}
		if (object == null) {
			// Return bean instance from factory.
			FactoryBean<?> factory = (FactoryBean<?>) beanInstance;
			// Caches object obtained from FactoryBean if it is a singleton.
			//如果从Bean工厂生产的Bean是单态模式的，则缓存  
			if (mbd == null && containsBeanDefinition(beanName)) {
				mbd = getMergedLocalBeanDefinition(beanName);
			}
			boolean synthetic = (mbd != null && mbd.isSynthetic());
			 //调用FactoryBeanRegistrySupport类的getObjectFromFactoryBean方法，实现FactoryBean生产Bean对象实例的过程    
			object = getObjectFromFactoryBean(factory, beanName, !synthetic);
		}
		return object;
	}
```
- 再进入FactoryBeanRegistrySupport的getObjectFromFactoryBean 大概在98行

```
// Bean工厂生产Bean实例对象  
protected Object getObjectFromFactoryBean(FactoryBean<?> factory, String beanName, boolean shouldPostProcess) {
		 // Bean工厂是单态模式，并且Bean工厂缓存中存在指定名称的Bean实例对象  
		if (factory.isSingleton() && containsSingleton(beanName)) {
			synchronized (getSingletonMutex()) {
				 // 直接从Bean工厂缓存中获取指定名称的Bean实例对象  
				Object object = this.factoryBeanObjectCache.get(beanName);
				 // Bean工厂缓存中没有指定名称的实例对象，则生产该实例对象  
				if (object == null) {
					// 调用Bean工厂的getObject方法生产指定Bean的实例对象  
					object = doGetObjectFromFactoryBean(factory, beanName);
					// Only post-process and store if not put there already during getObject() call above
					// (e.g. because of circular reference processing triggered by custom getBean calls)
					// 将生产的实例对象添加到Bean工厂缓存中  
					Object alreadyThere = this.factoryBeanObjectCache.get(beanName);
					if (alreadyThere != null) {
						object = alreadyThere;
					}
					else {
						if (object != null && shouldPostProcess) {
							try {
								object = postProcessObjectFromFactoryBean(object, beanName);
							}
							catch (Throwable ex) {
								throw new BeanCreationException(beanName,
										"Post-processing of FactoryBean's singleton object failed", ex);
							}
						}
						this.factoryBeanObjectCache.put(beanName, (object != null ? object : NULL_OBJECT));
					}
				}
				return (object != NULL_OBJECT ? object : null);
			}
		}
		else {
			// 调用Bean工厂的getObject方法生产指定Bean的实例对象  
			Object object = doGetObjectFromFactoryBean(factory, beanName);
			if (object != null && shouldPostProcess) {
				try {
					object = postProcessObjectFromFactoryBean(object, beanName);
				}
				catch (Throwable ex) {
					throw new BeanCreationException(beanName, "Post-processing of FactoryBean's object failed", ex);
				}
			}
			return object;
		}
	}
```

- 来到doGetObjectFromFactoryBean方法 154行左右

```
//调用FactoryBean接口实现类的创建对象方法的地方
private Object doGetObjectFromFactoryBean(final FactoryBean<?> factory, final String beanName)
			throws BeanCreationException {

		Object object;
		try {
			if (System.getSecurityManager() != null) {
				AccessControlContext acc = getAccessControlContext();
				try {
					//实现PrivilegedExceptionAction接口的匿名内置类    
	                   //根据JVM检查权限，然后决定BeanFactory创建实例对象  
					object = AccessController.doPrivileged(new PrivilegedExceptionAction<Object>() {
						public Object run() throws Exception {
							//调用FactoryBean接口实现类的创建对象方法   
								return factory.getObject();
							}
						}, acc);
				}
				catch (PrivilegedActionException pae) {
					throw pae.getException();
				}
			}
			else {
				//调用FactoryBean接口实现类的创建对象方法   
				object = factory.getObject();
			}
		}
		catch (FactoryBeanNotInitializedException ex) {
			throw new BeanCurrentlyInCreationException(beanName, ex.toString());
		}
		catch (Throwable ex) {
			throw new BeanCreationException(beanName, "FactoryBean threw exception on object creation", ex);
		}

		 //创建出来的实例对象为null，或者因为单态对象正在创建而返回null    
		// Do not accept a null value for a FactoryBean that's not fully
		// initialized yet: Many FactoryBeans just return null then.
		if (object == null && isSingletonCurrentlyInCreation(beanName)) {
			throw new BeanCurrentlyInCreationException(
					beanName, "FactoryBean which is currently in creation returned null from getObject");
		}
		return object;
	}
```
>到这里就是一个实现了FactoryBean接口初始化不带"&"符号的一个基本过程。

另外文章代码或者我理解有误的地方,希望能批评指出。

