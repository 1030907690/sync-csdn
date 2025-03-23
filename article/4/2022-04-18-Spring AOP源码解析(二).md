---
layout:					post
title:					"Spring AOP源码解析(二)"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 接上文[Spring AOP源码解析(一)](https://sample.blog.csdn.net/article/details/106948046)，本文我们来看Spring是如何创建代理和执行增强功能的。

## 初始化对象
- 无论是创建普通对象还是代理类`AbstractBeanFactory#getBean`方法都是入口。我们往下
- 定位到`AbstractAutowireCapableBeanFactory#doCreateBean`

```java
 protected Object doCreateBean(final String beanName, final RootBeanDefinition mbd, final Object[] args) {
		// Instantiate the bean.
		BeanWrapper instanceWrapper = null;
		if (mbd.isSingleton()) {
			instanceWrapper = this.factoryBeanInstanceCache.remove(beanName);
		}
		if (instanceWrapper == null) {
			 // 说明不是 FactoryBean，这里实例化 Bean，这里非常关键
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
				   // MergedBeanDefinitionPostProcessor，这个我真不展开说了，直接跳过吧，很少用的
				applyMergedBeanDefinitionPostProcessors(mbd, beanType, beanName);
				mbd.postProcessed = true;
			}
		}

		// Eagerly cache singletons to be able to resolve circular references
		// even when triggered by lifecycle interfaces like BeanFactoryAware.
		 // 下面这块代码是为了解决循环依赖的问题
		boolean earlySingletonExposure = (mbd.isSingleton() && this.allowCircularReferences &&
				isSingletonCurrentlyInCreation(beanName));
		if (earlySingletonExposure) {
			if (logger.isDebugEnabled()) {
				logger.debug("Eagerly caching bean '" + beanName +
						"' to allow for resolving potential circular references");
			}
			// 高版本的源码是  <beanName,lambda(原始对象)>  , 提前暴露工厂,把刚创建好的对象传进去，这样遇上循环依赖（非构造方法的循环依赖）就有对象可用了
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
				 // 还记得 init-method 吗？还有 InitializingBean 接口？还有 BeanPostProcessor 接口？
		         // 这里就是处理 bean 初始化完成后的各种回调，里面也有机会返回代理
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
				// 判断后处理得到的对象是否是原始对象
				if (exposedObject == bean) {
					// 如果是得到getSingleton缓存里的对象
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

- 进入`initializeBean`方法

```java
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
			 //执行一部分Aware的接口的回调方法， 如果 bean 实现了 BeanNameAware、BeanClassLoaderAware 或 BeanFactoryAware 接口，回调
			invokeAwareMethods(beanName, bean);
		}

		Object wrappedBean = bean;
		if (mbd == null || !mbd.isSynthetic()) {
			//执行生命周期初始化回调方法，一部分Aware的接口 ，BeanPostProcessor 的 postProcessBeforeInitialization 回调,应用后处理器
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
			 // BeanPostProcessor 的 postProcessAfterInitialization 回调，,应用后处理器   。此处也是大部分使用了代理返回代理对象的地方
			wrappedBean = applyBeanPostProcessorsAfterInitialization(wrappedBean, beanName);
		}
		return wrappedBean;
	}
```
## 执行postProcessBeforeInitialization 回调,有可能返回代理对象
- `applyBeanPostProcessorsAfterInitialization`，大部分的代理对象都在这个时候产生。

```bash

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
- 然后回调到`AbstractAutoProxyCreator#postProcessAfterInitialization`方法

```java
	//BeanPostProcessor的后置处理
	public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
		if (bean != null) {
			//根据给定的bean的class和name 构建出个key,beanClassName  , beanName
			Object cacheKey = getCacheKey(bean.getClass(), beanName);
			//是否由于避免循环依赖而创建的bean代理
			if (!this.earlyProxyReferences.containsKey(cacheKey)) {
				return wrapIfNecessary(bean, beanName, cacheKey);
			}
		}
		return bean;
	}

```

## 寻找合适的Advisor
- 然后进入`wrapIfNecessary`方法。这个方法大概做这两件事。
>  1、找出指定bean对应的增强器
	 2、 根据找出的增强器创建代理

```java
 protected Object wrapIfNecessary(Object bean, String beanName, Object cacheKey) {
		//如果已经处理过
		if (beanName != null && this.targetSourcedBeans.containsKey(beanName)) {
			return bean;
		}
		if (Boolean.FALSE.equals(this.advisedBeans.get(cacheKey))) {
			return bean;
		}

		if("testServiceImpl".equals(beanName)){
			System.out.println("TestServiceImpl  进入代理");
		}
		
		if("testAopServiceImpl".equals(beanName)){
			System.out.println("TestAopServiceImpl  进入代理");
		}
		
		//给定的bean类是否代表一个基础设施类，不应代理
		if (isInfrastructureClass(bean.getClass()) || shouldSkip(bean.getClass(), beanName)) {
			this.advisedBeans.put(cacheKey, Boolean.FALSE);
			return bean;
		}

		//getAdvicesAndAdvisorsForBean(bean.getClass(), beanName, null)，这个方法将得到所有的可用于拦截当前 bean 的 advisor、advice、interceptor。
		//另一个就是 TargetSource 这个概念，它用于封装真实实现类的信息，上面用了 SingletonTargetSource 这个实现类，其实我们这里也不太需要关心这个，知道有这么回事就可以了。
		// 返回匹配当前 bean 的所有的 advisor、advice、interceptor
		// Create proxy if we have advice.
		//<bean>生成代理的条件
		//寻找合适的Advisor最终用于被代理对象执行它的方法时的拦截 DynamicAdvisedInterceptor#intercept 基本上可以说是它的执行链List<Object> chain = this.advised.getInterceptorsAndDynamicInterceptionAdvice(method, targetClass);
		Object[] specificInterceptors = getAdvicesAndAdvisorsForBean(bean.getClass(), beanName, null);
		if (specificInterceptors != DO_NOT_PROXY) {
			this.advisedBeans.put(cacheKey, Boolean.TRUE);
			//创建代理
			Object proxy = createProxy(bean.getClass(), beanName, specificInterceptors, new SingletonTargetSource(bean));
			this.proxyTypes.put(cacheKey, proxy.getClass());
			return proxy;
		}

		this.advisedBeans.put(cacheKey, Boolean.FALSE);
		return bean;
	}
```
- 还记得上篇在`ConfigBeanDefinitionParser#parseAdvice`的`AspectJPointcutAdvisor` BeanDefinition吗？
- 我们进入`BeanFactoryAdvisorRetrievalHelper#findAdvisorBeans`。

```java
 public List<Advisor> findAdvisorBeans() {
		// Determine list of advisor bean names, if not cached already.
		String[] advisorNames = null;
		synchronized (this) {
			advisorNames = this.cachedAdvisorBeanNames;
			if (advisorNames == null) {
				// Do not initialize FactoryBeans here: We need to leave all regular beans
				// uninitialized to let the auto-proxy creator apply to them!
			
				advisorNames = BeanFactoryUtils.beanNamesForTypeIncludingAncestors(
						this.beanFactory, Advisor.class, true, false);
				
				
				this.cachedAdvisorBeanNames = advisorNames;
			}
		}
		
		if (advisorNames.length == 0) {
			return new LinkedList<Advisor>();
		}

		List<Advisor> advisors = new LinkedList<Advisor>();
		for (String name : advisorNames) {
			if (isEligibleBean(name)) {
				if (this.beanFactory.isCurrentlyInCreation(name)) {
					if (logger.isDebugEnabled()) {
						logger.debug("Skipping currently created advisor '" + name + "'");
					}
				}
				else {
					try {
						// xml方式 ，这里拿到ConfigBeanDefinitionParser#parseAdvice注册的AspectJPointcutAdvisor 
						advisors.add(this.beanFactory.getBean(name, Advisor.class));
					}
					catch (BeanCreationException ex) {
						Throwable rootCause = ex.getMostSpecificCause();
						if (rootCause instanceof BeanCurrentlyInCreationException) {
							BeanCreationException bce = (BeanCreationException) rootCause;
							if (this.beanFactory.isCurrentlyInCreation(bce.getBeanName())) {
								if (logger.isDebugEnabled()) {
									logger.debug("Skipping advisor '" + name +
											"' with dependency on currently created bean: " + ex.getMessage());
								}
								// Ignore: indicates a reference back to the bean we're trying to advise.
								// We want to find advisors other than the currently created bean itself.
								continue;
							}
						}
						throw ex;
					}
				}
			}
		}
		 
		return advisors;
	}
```
- 这边返回的增强正是`AspectJPointcutAdvisor`，如下图所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f0fae165db9218a9223cbf94e9c17100.png)
- 注意：这里寻找到的是候选增强。`AbstractAdvisorAutoProxyCreator#findAdvisorsThatCanApply`在候选增强器中寻找匹配项。

```java
protected List<Advisor> findAdvisorsThatCanApply(
			List<Advisor> candidateAdvisors, Class beanClass, String beanName) {

		ProxyCreationContext.setCurrentProxiedBeanName(beanName);
		try {
			return AopUtils.findAdvisorsThatCanApply(candidateAdvisors, beanClass);
		}
		finally {
			ProxyCreationContext.setCurrentProxiedBeanName(null);
		}
	}
// AopUtils.findAdvisorsThatCanApply
public static List<Advisor> findAdvisorsThatCanApply(List<Advisor> candidateAdvisors, Class<?> clazz) {
		if (candidateAdvisors.isEmpty()) {
			return candidateAdvisors;
		}
		List<Advisor> eligibleAdvisors = new LinkedList<Advisor>();
		//首先处理引介增强
		for (Advisor candidate : candidateAdvisors) {			//整个方法的主要判断都围绕canApply展开方法
			if (candidate instanceof IntroductionAdvisor && canApply(candidate, clazz)) {
				eligibleAdvisors.add(candidate);
			}
		}
		boolean hasIntroductions = !eligibleAdvisors.isEmpty();
		for (Advisor candidate : candidateAdvisors) {
			//引介增强已经处理
			if (candidate instanceof IntroductionAdvisor) {
				// already processed
				continue;
			}
			//对于普通bean的处理
			if (canApply(candidate, clazz, hasIntroductions)) {
				eligibleAdvisors.add(candidate);
			}
		}
		return eligibleAdvisors;
	}
 
```

- 然后`AbstractAdvisorAutoProxyCreator#extendAdvisors`方法内部，会加上`ExposeInvocationInterceptor`，并且放到最前面。

```java

protected void extendAdvisors(List<Advisor> candidateAdvisors) {
		AspectJProxyUtils.makeAdvisorChainAspectJCapableIfNecessary(candidateAdvisors);
}

//AspectJProxyUtils#makeAdvisorChainAspectJCapableIfNecessary
public static boolean makeAdvisorChainAspectJCapableIfNecessary(List<Advisor> advisors) {
		// Don't add advisors to an empty list; may indicate that proxying is just not required
		if (!advisors.isEmpty()) {
			boolean foundAspectJAdvice = false;
			for (Advisor advisor : advisors) {
				// Be careful not to get the Advice without a guard, as
				// this might eagerly instantiate a non-singleton AspectJ aspect
				if (isAspectJAdvice(advisor)) {
					foundAspectJAdvice = true;
				}
			}
			if (foundAspectJAdvice && !advisors.contains(ExposeInvocationInterceptor.ADVISOR)) {
				advisors.add(0, ExposeInvocationInterceptor.ADVISOR);
				return true;
			}
		}
		return false;
	}
 
```


- 这里`getAdvicesAndAdvisorsForBean`的话，找到2个增强，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/42c6f266ad28db2be1428ada5eed494c.png)

- ExposeInvocationInterceptor 属于内置的，先不管，待会儿我们再看下是干嘛的。
- AspectJPointcutAdvisor#advisor 是根据我们配置的切面表达式匹配到的`OperatorLogs#doBefore`方法。

## 创建代理
- 然后创建代理，进入`AbstractAutoProxyCreator#createProxy`方法。

```java
protected Object createProxy(
			Class<?> beanClass, String beanName, Object[] specificInterceptors, TargetSource targetSource) {
		 // 创建 ProxyFactory 实例
		ProxyFactory proxyFactory = new ProxyFactory();
		// Copy our properties (proxyTargetClass etc) inherited from ProxyConfig.
		proxyFactory.copyFrom(this);

		// 在 schema-based 的配置方式中，我们介绍过，如果希望使用 CGLIB 来代理接口，可以配置
		   // proxy-target-class="true",这样不管有没有接口，都使用 CGLIB 来生成代理：
		   //   <aop:config proxy-target-class="true">......</aop:config>
		if (!shouldProxyTargetClass(beanClass, beanName)) {
			// Must allow for introductions; can't just set interfaces to
			// the target's interfaces only.
			Class<?>[] targetInterfaces = ClassUtils.getAllInterfacesForClass(beanClass, this.proxyClassLoader);
			for (Class<?> targetInterface : targetInterfaces) {
				proxyFactory.addInterface(targetInterface);
			}
		}

		//设置advisors很重要 在DynamicAdvisedInterceptor#getInterceptorsAndDynamicInterceptionAdvice#getInterceptorsAndDynamicInterceptionAdvice时通过advisor得到执行链列表
		// 这个方法会返回匹配了当前 bean 的 advisors 数组
	   // 注意：如果 specificInterceptors 中有 advice 和 interceptor，它们也会被包装成 advisor，进去看下源码就清楚了
		Advisor[] advisors = buildAdvisors(beanName, specificInterceptors);
		for (Advisor advisor : advisors) {
			proxyFactory.addAdvisor(advisor);
		}

		proxyFactory.setTargetSource(targetSource);
		customizeProxyFactory(proxyFactory);

		proxyFactory.setFrozen(this.freezeProxy);
		if (advisorsPreFiltered()) {
			proxyFactory.setPreFiltered(true);
		}
			
		/**
		 * 实现代码就一行，但是却明确告诉我们做了两件事情：
			创建AopProxy接口实现类
			通过AopProxy接口的实现类的getProxy方法获取<bean>对应的代理
		 * */
		return proxyFactory.getProxy(this.proxyClassLoader);
	}

```
- 进入`DefaultAopProxyFactory#createAopProxy`
```java
public AopProxy createAopProxy(AdvisedSupport config) throws AopConfigException {
		 // (optimize，默认false) || (proxy-target-class=true) || (没有接口)
		//config.isProxyTargetClass() 是 <aop:config proxy-target-class="true" >配置
		if (config.isOptimize() || config.isProxyTargetClass() || hasNoUserSuppliedProxyInterfaces(config)) {
			Class targetClass = config.getTargetClass();
			if (targetClass == null) {
				throw new AopConfigException("TargetSource cannot determine target class: " +
						"Either an interface or a target is required for proxy creation.");
			}
			 // 如果要代理的类本身就是接口，也会用 JDK 动态代理 
			if (targetClass.isInterface()) {
				return new JdkDynamicAopProxy(config);
			}
			return CglibProxyFactory.createCglibProxy(config);
		}
		else {
			 // 如果有接口，会跑到这个分支
			return new JdkDynamicAopProxy(config);
		}
	}

```
- 我没有特殊配置`proxy-target-class`，又因为被代理类是个接口，所以进入`JdkDynamicAopProxy#getProxy`。下面是熟悉的JDK动态代理。

```java
 public Object getProxy(ClassLoader classLoader) {
		if (logger.isDebugEnabled()) {
			logger.debug("Creating JDK dynamic proxy: target source is " + this.advised.getTargetSource());
		}
		Class<?>[] proxiedInterfaces = AopProxyUtils.completeProxiedInterfaces(this.advised);
		findDefinedEqualsAndHashCodeMethods(proxiedInterfaces);
		/**
		 java.lang.reflect.Proxy.newProxyInstance(…) 方法需要三个参数，第一个是 ClassLoader，第二个参数代表需要实现哪些接口，第三个参数最重要，是 InvocationHandler 实例，我们看到这里传了 this，因为 JdkDynamicAopProxy 本身实现了 InvocationHandler 接口。
		 * **/
		//jdk动态代理
		return Proxy.newProxyInstance(classLoader, proxiedInterfaces, this);
	}
```
- 然后回过来就能看到生成的`TestAopServiceImpl`是一个代理对象。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/06ea8f55ce16ea1afa939709acafa107.png)
## 执行方法
- 我们知道JDK动态代理的规则，当被代理对象调用某方法时会去调用其`invoke`方法。那么我们进入`JdkDynamicAopProxy#invoke`。

```java
public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
		MethodInvocation invocation;
		Object oldProxy = null;
		boolean setProxyContext = false;

		TargetSource targetSource = this.advised.targetSource;
		Class<?> targetClass = null;
		Object target = null;

		try {
			if (!this.equalsDefined && AopUtils.isEqualsMethod(method)) {
				// The target does not implement the equals(Object) method itself.
				 // 代理的 equals 方法
				return equals(args[0]);
			}
			if (!this.hashCodeDefined && AopUtils.isHashCodeMethod(method)) {
				// The target does not implement the hashCode() method itself.
				 // 代理的 hashCode 方法
				return hashCode();
			}
			if (!this.advised.opaque && method.getDeclaringClass().isInterface() &&
					method.getDeclaringClass().isAssignableFrom(Advised.class)) {
				// Service invocations on ProxyConfig with the proxy config...
				return AopUtils.invokeJoinpointUsingReflection(this.advised, method, args);
			}

			Object retVal;

			// 如果设置了 exposeProxy，那么将 proxy 放到 ThreadLocal 中
			if (this.advised.exposeProxy) {
				// Make invocation available if necessary.
				oldProxy = AopContext.setCurrentProxy(proxy);
				setProxyContext = true;
			}

			// May be null. Get as late as possible to minimize the time we "own" the target,
			// in case it comes from a pool.
			// 调用TargetSource的getTarget方法  默认的TargetSource是SingletonTargetSource 直接创建时传过去的target对象
			target = targetSource.getTarget();
			if (target != null) {
				targetClass = target.getClass();
			}

			// Get the interception chain for this method.
			// 创建一个 chain，包含所有要执行的 advice
			List<Object> chain = this.advised.getInterceptorsAndDynamicInterceptionAdvice(method, targetClass);

			// Check whether we have any advice. If we don't, we can fallback on direct
			// reflective invocation of the target, and avoid creating a MethodInvocation.
			if (chain.isEmpty()) {
				// We can skip creating a MethodInvocation: just invoke the target directly
				// Note that the final invoker must be an InvokerInterceptor so we know it does
				// nothing but a reflective operation on the target, and no hot swapping or fancy proxying.
				// chain 是空的，说明不需要被增强，这种情况很简单
				retVal = AopUtils.invokeJoinpointUsingReflection(target, method, args);
			}
			else {
				// We need to create a method invocation...
				 // 执行方法，得到返回值
				invocation = new ReflectiveMethodInvocation(proxy, target, method, args, targetClass, chain);
				// Proceed to the joinpoint through the interceptor chain.
				retVal = invocation.proceed();
			}

			// Massage return value if necessary.
			Class<?> returnType = method.getReturnType();
			if (retVal != null && retVal == target && returnType.isInstance(proxy) &&
					!RawTargetAccess.class.isAssignableFrom(method.getDeclaringClass())) {
				// Special case: it returned "this" and the return type of the method
				// is type-compatible. Note that we can't help if the target sets
				// a reference to itself in another returned object.
				retVal = proxy;
			}
			else if (retVal == null && returnType != Void.TYPE && returnType.isPrimitive()) {
				throw new AopInvocationException(
						"Null return value from advice does not match primitive return type for: " + method);
			}
			return retVal;
		}
		finally {
			if (target != null && !targetSource.isStatic()) {
				// Must have come from TargetSource.
				targetSource.releaseTarget(target);
			}
			if (setProxyContext) {
				// Restore old proxy.
				AopContext.setCurrentProxy(oldProxy);
			}
		}
	}
```
## 得到执行链chain
- 进入`AdvisedSupport#getInterceptorsAndDynamicInterceptionAdvice`
```java
public List<Object> getInterceptorsAndDynamicInterceptionAdvice(Method method, Class targetClass) {
		MethodCacheKey cacheKey = new MethodCacheKey(method);
		List<Object> cached = this.methodCache.get(cacheKey);
		if (cached == null) {
			cached = this.advisorChainFactory.getInterceptorsAndDynamicInterceptionAdvice(
					this, method, targetClass);
			this.methodCache.put(cacheKey, cached);
		}
		return cached;
	}
```
- 结果就是之前找到的增强
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cc5af25a72ebc53717725131bac37bd2.png)

## 执行增强proceed
- 进入`ReflectiveMethodInvocation#proceed`，这里维护了一个`currentInterceptorIndex`下标。

```java
public Object proceed() throws Throwable {
		//	We start with an index of -1 and increment early.
		if (this.currentInterceptorIndex == this.interceptorsAndDynamicMethodMatchers.size() - 1) {
			//如果执行完了 去invoke 执行代理的那个方法
			//System.out.println("执行真正的目标方法 ");
			return invokeJoinpoint();
		}

		// ++this.currentInterceptorIndex  链式执行
		Object interceptorOrInterceptionAdvice =
				this.interceptorsAndDynamicMethodMatchers.get(++this.currentInterceptorIndex);
		if (interceptorOrInterceptionAdvice instanceof InterceptorAndDynamicMethodMatcher) {
			// Evaluate dynamic method matcher here: static part will already have
			// been evaluated and found to match.
			InterceptorAndDynamicMethodMatcher dm =
					(InterceptorAndDynamicMethodMatcher) interceptorOrInterceptionAdvice;
			if (dm.methodMatcher.matches(this.method, this.targetClass, this.arguments)) {
				return dm.interceptor.invoke(this);
			}
			else {
				// Dynamic matching failed.
				// Skip this interceptor and invoke the next in the chain.
				return proceed();
			}
		}
		else {
			// It's an interceptor, so we just invoke it: The pointcut will have
			// been evaluated statically before this object was constructed.
			return ((MethodInterceptor) interceptorOrInterceptionAdvice).invoke(this);
		}
	}
```
###  执行ExposeInvocationInterceptor增强
- 首先拿出来的是`ExposeInvocationInterceptor`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/75100bd19de5daf6aae212d8d0b4cf2d.png)

- 进入`ExposeInvocationInterceptor#invoke`

```java
	private static final ThreadLocal<MethodInvocation> invocation =
			new NamedThreadLocal<MethodInvocation>("Current AOP method invocation");

 
	public Object invoke(MethodInvocation mi) throws Throwable {
		MethodInvocation oldInvocation = invocation.get();
		invocation.set(mi);
		try {
     		//再调用proceed 好执行下一个增强
			return mi.proceed();
		}
		finally {
			invocation.set(oldInvocation);
		}
	}
```
>invocation是一个ThreadLocal变量，可以看出ExposeInvocationInterceptor就是用来保存MethodInvocation的，方便其他地方拿到，在后续的环节，只要需要用到当前的MethodInvocation就通过ExposeInvocationInterceptor.currentInvocation()静态方法获得。

- 再执行进入`ReflectiveMethodInvocation#proceed`

### 执行MethodBeforeAdviceInterceptor增强
- 这次拿出的是`MethodBeforeAdviceInterceptor`，执行`OperatorLogs#doBefore`逻辑，进入`MethodBeforeAdviceInterceptor#invoke`

```java
 public Object invoke(MethodInvocation mi) throws Throwable {
		// advice是org.springframework.aop.aspectj.AspectJMethodBeforeAdvice   @Before注解修饰的方法会走这里
		this.advice.before(mi.getMethod(), mi.getArguments(), mi.getThis() );
		// 继续往下
		return mi.proceed();
	}
```
- 最后执行我们自己的逻辑`AspectJMethodBeforeAdvice(AbstractAspectJAdvice).invokeAdviceMethodWithGivenArgs`，后面就是反射调用`OperatorLogs#doBefore`。

```java
 
	protected Object invokeAdviceMethodWithGivenArgs(Object[] args) throws Throwable {
		Object[] actualArgs = args;
		if (this.aspectJAdviceMethod.getParameterTypes().length == 0) {
			actualArgs = null;
		}
		try {
			ReflectionUtils.makeAccessible(this.aspectJAdviceMethod);
			//执行方法如注解@Around配置的方法public java.lang.Object com.zzq.core.test.aop.OperatorLogs.around(org.aspectj.lang.ProceedingJoinPoint) 还有xml那种方式配置的
			// TODO AopUtils.invokeJoinpointUsingReflection
			System.out.println("执行的advice(增强器): "+this.getClass());
			return this.aspectJAdviceMethod.invoke(this.aspectInstanceFactory.getAspectInstance(), actualArgs);
		}
		catch (IllegalArgumentException ex) {
			throw new AopInvocationException("Mismatch on arguments to advice method [" +
					this.aspectJAdviceMethod + "]; pointcut expression [" +
					this.pointcut.getPointcutExpression() + "]", ex);
		}
		catch (InvocationTargetException ex) {
			throw ex.getTargetException();
		}
	}
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1edccbd47549958fcbcdadec2afc2a6f.png)
## 执行被代理类的业务逻辑
- 当执行`mi.proceed()`时，后面一句没有了，所以执行`invokeJoinpoint()`。

```java
	protected Object invokeJoinpoint() throws Throwable {
		return AopUtils.invokeJoinpointUsingReflection(this.target, this.method, this.arguments);
	}

```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/99c5535e4754944990a652cd29523a7c.png)

- 进入`AopUtils#invokeJoinpointUsingReflection`，此处反射直接调用被代理类的方法。

```java
	public static Object invokeJoinpointUsingReflection(Object target, Method method, Object[] args)
			throws Throwable {

		// Use reflection to invoke the method.
		try {
			ReflectionUtils.makeAccessible(method);
			return method.invoke(target, args);
		}
		catch (InvocationTargetException ex) {
			// Invoked method threw a checked exception.
			// We must rethrow it. The client won't see the interceptor.
			throw ex.getTargetException();
		}
		catch (IllegalArgumentException ex) {
			throw new AopInvocationException("AOP configuration seems to be invalid: tried calling method [" +
					method + "] on target [" + target + "]", ex);
		}
		catch (IllegalAccessException ex) {
			throw new AopInvocationException("Could not access method [" + method + "]", ex);
		}
	}

```
- 剩下的就是返回了。
## 小结
- 再来回顾下基本流程。
1、AOP非Spring默认标签，那么解析时会交给对应的`NamespaceHandler`处理，这个`NamespaceHandler`是`AopNamespaceHandler`。
2、创建对象时，回调`BeanPostProcessor#postProcessAfterInitialization`。
3、然后初始化解析器，解析阶段找到`Advice`（before、after之类的增强器）增强器注册到容器中。
4、创建Bean时会判断是否满足切面表达式，如果满足会创建代理，`寻找合适的Advice（增强器），构建执行器链`。
5、如果Bean是一个代理对象，在执行内部方法时，会`先执行Advice（增强器）链`，`执行完后再执行真正的方法`。 
- 本文没有涉及`Cglib`，不过思路是一样的。