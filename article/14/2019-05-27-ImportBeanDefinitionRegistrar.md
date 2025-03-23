---
layout:					post
title:					"ImportBeanDefinitionRegistrar"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
#### 一、简介
- ImportBeanDefinitionRegistrar接口是也是spring的扩展点之一,它可以支持我们自己写的代码封装成`BeanDefinition`对象;实现此接口的类会回调`postProcessBeanDefinitionRegistry`方法，注册到spring容器中。把bean注入到spring容器不止有 `@Service @Component`等注解方式；还可以实现此接口。

#### 二、使用
- 接口的使用很简单，使用`@Import`注解导入这个类即可。
- 我先新建一个ConfigurationTest.java

```
 package com.zzq.core.configuration;
 
 
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

import com.zzq.core.importbeandefinitionregistrar.ImportBeanDefinitionRegistrarTest;
 

 
@Configuration
@Import(ImportBeanDefinitionRegistrarTest.class) //导入
public class ConfigurationTest {
 
	
}

```
- ImportBeanDefinitionRegistrarTest.java

```
 package com.zzq.core.importbeandefinitionregistrar;

import org.springframework.beans.MutablePropertyValues;
import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.beans.factory.support.BeanDefinitionRegistry;
import org.springframework.beans.factory.support.GenericBeanDefinition;
import org.springframework.context.annotation.ImportBeanDefinitionRegistrar;
import org.springframework.core.type.AnnotationMetadata;

import com.zzq.core.importbeandefinitionregistrar.bean.TestBean;
import com.zzq.other.autowired.autowiredtest1.AutowiredTest;

public class ImportBeanDefinitionRegistrarTest implements ImportBeanDefinitionRegistrar{
	
	 
	
	@Override
	public void registerBeanDefinitions(AnnotationMetadata importingClassMetadata, BeanDefinitionRegistry registry) {
		
		BeanDefinition beanDefinition = new GenericBeanDefinition();
		beanDefinition.setBeanClassName(TestBean.class.getName());
		MutablePropertyValues values = beanDefinition.getPropertyValues();
		values.addPropertyValue("id", 1);
		values.addPropertyValue("name", "ZhangSan");
		//这里注册bean
		registry.registerBeanDefinition("testBean", beanDefinition );
		
	}

}

```
- TestBean.java

```
package com.zzq.core.importbeandefinitionregistrar.bean;

public class TestBean {

	
	private Integer id;
	
	private String name;
	
	private String password;

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}
	
	
	
	
}
```
- 要拿到这个bean是一样的

```
  @Resource
	private TestBean testBean;
```
或者

```
@Autowired
	private TestBean testBean;
```
### 三、源码解析
- ImportBeanDefinitionRegistrarTest是被导入的,所以要加载到ImportBeanDefinitionRegistrarTest必然要先加载ConfigurationTest才行；所以先看Configuration的代码。
- 找到ConfigurationClassPostProcessor类，它实现了BeanDefinitionRegistryPostProcessor接口，在AbstractApplicationContext#invokeBeanFactoryPostProcessors方法有这样一段代码。

```
 Map<String, BeanDefinitionRegistryPostProcessor> beanMap =
					beanFactory.getBeansOfType(BeanDefinitionRegistryPostProcessor.class, true, false);
List<BeanDefinitionRegistryPostProcessor> registryPostProcessorBeans =
		new ArrayList<BeanDefinitionRegistryPostProcessor>(beanMap.values());
OrderComparator.sort(registryPostProcessorBeans);
for (BeanDefinitionRegistryPostProcessor postProcessor : registryPostProcessorBeans) {
	postProcessor.postProcessBeanDefinitionRegistry(registry);
}
```
- 这段代码的意图很明显，这在spring源码中，这种风格的写法很多(比如拿到一个后处理器集合之类的BeanFactoryPostProcessor)；这里是从spring容器中拿到实现了BeanDefinitionRegistryPostProcessor接口的类。拿到后执行对应的postProcessBeanDefinitionRegistry方法(题外话:目前看到mybatis源码MapperScannerConfigurer也是实现这个接口，然后扫描mapper,注入进spring容器的)。
- 现在定位到ConfigurationClassPostProcessor#postProcessBeanDefinitionRegistry方法。

```
 //从invokeBeanFactoryPostProcessors方法调过来
	public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) {
		RootBeanDefinition iabpp = new RootBeanDefinition(ImportAwareBeanPostProcessor.class);
		iabpp.setRole(BeanDefinition.ROLE_INFRASTRUCTURE);
		registry.registerBeanDefinition(IMPORT_AWARE_PROCESSOR_BEAN_NAME, iabpp);
		//取得registry的id并做判重处理或记录
		int registryId = System.identityHashCode(registry);
		if (this.registriesPostProcessed.contains(registryId)) {
			throw new IllegalStateException(
					"postProcessBeanDefinitionRegistry already called for this post-processor against " + registry);
		}
		if (this.factoriesPostProcessed.contains(registryId)) {
			throw new IllegalStateException(
					"postProcessBeanFactory already called for this post-processor against " + registry);
		}
		//保存处理过的registry，避免重复处理
		this.registriesPostProcessed.add(registryId);
		 //处理java配置形式的bean定义
		processConfigBeanDefinitions(registry);
	}
```
- processConfigBeanDefinitions方法

```
public void processConfigBeanDefinitions(BeanDefinitionRegistry registry) {
		Set<BeanDefinitionHolder> configCandidates = new LinkedHashSet<BeanDefinitionHolder>();
		//加载当前已知所有bean定义
		for (String beanName : registry.getBeanDefinitionNames()) {
			BeanDefinition beanDef = registry.getBeanDefinition(beanName);
			//   判断对应bean是否为配置类,如果是,则加入到configCandidates
			// @Configuration, @Component, @ComponentScan, @Import, @Bean等注解
			if (ConfigurationClassUtils.checkConfigurationClassCandidate(beanDef, this.metadataReaderFactory)) {
				configCandidates.add(new BeanDefinitionHolder(beanDef, beanName));
			}
		}

		// Return immediately if no @Configuration classes were found
		//如果找不到@configuration类，则立即返回
		if (configCandidates.isEmpty()) {
			return;
		}

		// Detect any custom bean name generation strategy supplied through the enclosing application context
		 // 3. 如果BeanDefinitionRegistry 是SingletonBeanRegistry 子类的话,由于我们当前传入的是DefaultListableBeanFactory,是
	    // SingletonBeanRegistry 的子类。因此会将registry强转为SingletonBeanRegistry
		SingletonBeanRegistry singletonRegistry = null;
		if (registry instanceof SingletonBeanRegistry) {
			singletonRegistry = (SingletonBeanRegistry) registry;
			if (!this.localBeanNameGeneratorSet && singletonRegistry.containsSingleton(CONFIGURATION_BEAN_NAME_GENERATOR)) {
				  // 如果localBeanNameGeneratorSet 等于false 并且SingletonBeanRegistry 中有 id 为 org.springframework.context.annotation.internalConfigurationBeanNameGenerator
	            // 的bean .则将componentScanBeanNameGenerator,importBeanNameGenerator 赋值为 该bean.
 
				BeanNameGenerator generator = (BeanNameGenerator) singletonRegistry.getSingleton(CONFIGURATION_BEAN_NAME_GENERATOR);
				this.componentScanBeanNameGenerator = generator;
				this.importBeanNameGenerator = generator;
			}
		}

		// Parse each @Configuration class
		 // 实例化ConfigurationClassParser 为了解析 各个配置类
		ConfigurationClassParser parser = new ConfigurationClassParser(
				this.metadataReaderFactory, this.problemReporter, this.environment,
				this.resourceLoader, this.componentScanBeanNameGenerator, registry);
		for (BeanDefinitionHolder holder : configCandidates) {
			BeanDefinition bd = holder.getBeanDefinition();
			System.out.println("ConfigurationClassPostProcessor bd " + bd.getBeanClassName());
			try {
				if (bd instanceof AbstractBeanDefinition && ((AbstractBeanDefinition) bd).hasBeanClass()) {
					parser.parse(((AbstractBeanDefinition) bd).getBeanClass(), holder.getBeanName());
				}
				else {
					parser.parse(bd.getBeanClassName(), holder.getBeanName());
				}
			}
			catch (IOException ex) {
				throw new BeanDefinitionStoreException("Failed to load bean class: " + bd.getBeanClassName(), ex);
			}
		}
		parser.validate();

		// Handle any @PropertySource annotations
		Stack<PropertySource<?>> parsedPropertySources = parser.getPropertySources();
		if (!parsedPropertySources.isEmpty()) {
			if (!(this.environment instanceof ConfigurableEnvironment)) {
				logger.warn("Ignoring @PropertySource annotations. " +
						"Reason: Environment must implement ConfigurableEnvironment");
			}
			else {
				MutablePropertySources envPropertySources = ((ConfigurableEnvironment)this.environment).getPropertySources();
				while (!parsedPropertySources.isEmpty()) {
					envPropertySources.addLast(parsedPropertySources.pop());
				}
			}
		}

		// Read the model and create bean definitions based on its content
		if (this.reader == null) {
			this.reader = new ConfigurationClassBeanDefinitionReader(
					registry, this.sourceExtractor, this.problemReporter, this.metadataReaderFactory,
					this.resourceLoader, this.environment, this.importBeanNameGenerator);
		}
		this.reader.loadBeanDefinitions(parser.getConfigurationClasses());

		// Register the ImportRegistry as a bean in order to support ImportAware @Configuration classes
		if (singletonRegistry != null) {
			if (!singletonRegistry.containsSingleton(IMPORT_REGISTRY_BEAN_NAME)) {
				singletonRegistry.registerSingleton(IMPORT_REGISTRY_BEAN_NAME, parser.getImportRegistry());
			}
		}

		if (this.metadataReaderFactory instanceof CachingMetadataReaderFactory) {
			((CachingMetadataReaderFactory) this.metadataReaderFactory).clearCache();
		}
	}
```
- ConfigurationClassParser#parse方法

```
 public void parse(String className, String beanName) throws IOException {
		MetadataReader reader = this.metadataReaderFactory.getMetadataReader(className);
		processConfigurationClass(new ConfigurationClass(reader, beanName));
	}

```

```
protected void processConfigurationClass(ConfigurationClass configClass) throws IOException {
		...................
		// Recursively process the configuration class and its superclass hierarchy.
		do {
		     //重点
			metadata = doProcessConfigurationClass(configClass, metadata);
		}
		while (metadata != null);

 .................
	}
```

```
protected AnnotationMetadata doProcessConfigurationClass(ConfigurationClass configClass, AnnotationMetadata metadata) throws IOException {
		// Recursively process any member (nested) classes first
		processMemberClasses(metadata);

		// Process any @PropertySource annotations
		//处理@PropertySource  加载外面资源文件
		AnnotationAttributes propertySource = MetadataUtils.attributesFor(metadata,
				org.springframework.context.annotation.PropertySource.class);
		if (propertySource != null) {
			processPropertySource(propertySource);
		}

		// Process any @ComponentScan annotations
		//处理  @ComponentScan 扫描包
		AnnotationAttributes componentScan = MetadataUtils.attributesFor(metadata, ComponentScan.class);
		if (componentScan != null) {
			// The config class is annotated with @ComponentScan -> perform the scan immediately
			Set<BeanDefinitionHolder> scannedBeanDefinitions =
					this.componentScanParser.parse(componentScan, metadata.getClassName());

			// Check the set of scanned definitions for any further config classes and parse recursively if necessary
			for (BeanDefinitionHolder holder : scannedBeanDefinitions) {
				if (ConfigurationClassUtils.checkConfigurationClassCandidate(holder.getBeanDefinition(), this.metadataReaderFactory)) {
					this.parse(holder.getBeanDefinition().getBeanClassName(), holder.getBeanName());
				}
			}
		}

		//处理@Import注解
		// Process any @Import annotations
		Set<Object> imports = new LinkedHashSet<Object>();
		Set<String> visited = new LinkedHashSet<String>();
		collectImports(metadata, imports, visited);
		if (!imports.isEmpty()) {
			processImport(configClass, metadata, imports, true);
		}

		// Process any @ImportResource annotations
		if (metadata.isAnnotated(ImportResource.class.getName())) {
			AnnotationAttributes importResource = MetadataUtils.attributesFor(metadata, ImportResource.class);
			String[] resources = importResource.getStringArray("value");
			Class<? extends BeanDefinitionReader> readerClass = importResource.getClass("reader");
			for (String resource : resources) {
				String resolvedResource = this.environment.resolveRequiredPlaceholders(resource);
				configClass.addImportedResource(resolvedResource, readerClass);
			}
		}

		// Process individual @Bean methods
		//处理@Bean注解
		Set<MethodMetadata> beanMethods = metadata.getAnnotatedMethods(Bean.class.getName());
		for (MethodMetadata methodMetadata : beanMethods) {
			configClass.addBeanMethod(new BeanMethod(methodMetadata, configClass));
		}

		// Process superclass, if any
		if (metadata.hasSuperClass()) {
			String superclass = metadata.getSuperClassName();
			if (!superclass.startsWith("java") && !this.knownSuperclasses.containsKey(superclass)) {
				this.knownSuperclasses.put(superclass, configClass);
				// superclass found, return its annotation metadata and recurse
				if (metadata instanceof StandardAnnotationMetadata) {
					Class<?> clazz = ((StandardAnnotationMetadata) metadata).getIntrospectedClass();
					return new StandardAnnotationMetadata(clazz.getSuperclass(), true);
				}
				else {
					MetadataReader reader = this.metadataReaderFactory.getMetadataReader(superclass);
					return reader.getAnnotationMetadata();
				}
			}
		}

		// No superclass -> processing is complete
		return null;
	}
```

```
 private void processImport(ConfigurationClass configClass, AnnotationMetadata metadata,
			Collection<?> classesToImport, boolean checkForCircularImports) throws IOException {

		if (checkForCircularImports && this.importStack.contains(configClass)) {
			this.problemReporter.error(new CircularImportProblem(configClass, this.importStack, configClass.getMetadata()));
		}
		else {
			this.importStack.push(configClass);
			try {
				for (Object candidate : classesToImport) {
					Object candidateToCheck = (candidate instanceof Class ? (Class) candidate :
							this.metadataReaderFactory.getMetadataReader((String) candidate));
					//实现ImportSelector接口的处理
					if (checkAssignability(ImportSelector.class, candidateToCheck)) {
						// Candidate class is an ImportSelector -> delegate to it to determine imports
						Class<?> candidateClass = (candidate instanceof Class ? (Class) candidate :
								this.resourceLoader.getClassLoader().loadClass((String) candidate));
						ImportSelector selector = BeanUtils.instantiateClass(candidateClass, ImportSelector.class);
						processImport(configClass, metadata, Arrays.asList(selector.selectImports(metadata)), false);
					}
					//实现ImportBeanDefinitionRegistrar接口的处理
					else if (checkAssignability(ImportBeanDefinitionRegistrar.class, candidateToCheck)) {
						// Candidate class is an ImportBeanDefinitionRegistrar ->
						// delegate to it to register additional bean definitions
						Class<?> candidateClass = (candidate instanceof Class ? (Class) candidate :
								this.resourceLoader.getClassLoader().loadClass((String) candidate));
						ImportBeanDefinitionRegistrar registrar =
								BeanUtils.instantiateClass(candidateClass, ImportBeanDefinitionRegistrar.class);
						invokeAwareMethods(registrar);
						//调用该类的registerBeanDefinitions方法
						registrar.registerBeanDefinitions(metadata, this.registry);
					}
					else {
						//候选类不是importSelector或importBeanDefinitionRegistrar 
						//@Configuration类的处理
						// Candidate class not an ImportSelector or ImportBeanDefinitionRegistrar ->
						// process it as a @Configuration class
						this.importStack.registerImport(metadata,
								(candidate instanceof Class ? ((Class) candidate).getName() : (String) candidate));
						processConfigurationClass(candidateToCheck instanceof Class ?
								new ConfigurationClass((Class) candidateToCheck, true) :
								new ConfigurationClass((MetadataReader) candidateToCheck, true));
					}
				}
			}
			catch (ClassNotFoundException ex) {
				throw new NestedIOException("Failed to load import candidate class", ex);
			}
			finally {
				this.importStack.pop();
			}
		}
	}
```
- 调用ImportBeanDefinitionRegistrar接口实现类的地方也找到了，下面看DefaultListableBeanFactory#registerBeanDefinition方法。

```
 public void registerBeanDefinition(String beanName, BeanDefinition beanDefinition)
			throws BeanDefinitionStoreException {

		Assert.hasText(beanName, "Bean name must not be empty");
		Assert.notNull(beanDefinition, "BeanDefinition must not be null");

		if("configurationTest".equals(beanName)){
			System.out.println(" registerBeanDefinition(String beanName, BeanDefinition beanDefinition) " + beanName);
		}
		
		if (beanDefinition instanceof AbstractBeanDefinition) {
			try {
				((AbstractBeanDefinition) beanDefinition).validate();
			}
			catch (BeanDefinitionValidationException ex) {
				throw new BeanDefinitionStoreException(beanDefinition.getResourceDescription(), beanName,
						"Validation of bean definition failed", ex);
			}
		}
		  // old? 还记得 “允许 bean 覆盖” 这个配置吗？allowBeanDefinitionOverriding
		BeanDefinition oldBeanDefinition;

		synchronized (this.beanDefinitionMap) {
			  // 之后会看到，所有的 Bean 注册后会放入这个 beanDefinitionMap 中
			oldBeanDefinition = this.beanDefinitionMap.get(beanName);
			// 处理重复名称的 Bean 定义的情况
			if (oldBeanDefinition != null) {
				if (!this.allowBeanDefinitionOverriding) {
					 // 如果不允许覆盖的话，抛异常
					throw new BeanDefinitionStoreException(beanDefinition.getResourceDescription(), beanName,
							"Cannot register bean definition [" + beanDefinition + "] for bean '" + beanName +
							"': There is already [" + oldBeanDefinition + "] bound.");
				}
				else {
					if (this.logger.isInfoEnabled()) {
						this.logger.info("Overriding bean definition for bean '" + beanName +
								"': replacing [" + oldBeanDefinition + "] with [" + beanDefinition + "]");
					}
				}
			}
			else {
				//添加beanDefinitionNames
				this.beanDefinitionNames.add(beanName);
				this.frozenBeanDefinitionNames = null;
			}
			// 覆盖
			this.beanDefinitionMap.put(beanName, beanDefinition);
		}

		if (oldBeanDefinition != null || containsSingleton(beanName)) {
			resetBeanDefinition(beanName);
		}
	}

	public void removeBeanDefinition(String beanName) throws NoSuchBeanDefinitionException {
		Assert.hasText(beanName, "'beanName' must not be empty");

		synchronized (this.beanDefinitionMap) {
			BeanDefinition bd = this.beanDefinitionMap.remove(beanName);
			if (bd == null) {
				if (this.logger.isTraceEnabled()) {
					this.logger.trace("No bean named '" + beanName + "' found in " + this);
				}
				throw new NoSuchBeanDefinitionException(beanName);
			}
			this.beanDefinitionNames.remove(beanName);
			this.frozenBeanDefinitionNames = null;
		}

		resetBeanDefinition(beanName);
	}
```
- 这段代码主要就是把定义的bean放到beanDefinitionMap里去。beanDefinitionMap维护的就是bean的定义，当需要获取的时候就从里面拿到对应的BeanDefinition，根据BeanDefinition生成一个对象。

- 至此ImportBeanDefinitionRegistrar接口的初始化及调用过程完毕。