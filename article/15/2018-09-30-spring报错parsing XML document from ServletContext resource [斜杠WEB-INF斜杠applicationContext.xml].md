---
layout:					post
title:					"spring报错parsing XML document from ServletContext resource [/WEB-INF/applicationContext.xml]"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
#### 一、 报错如下:

```

org.springframework.beans.factory.BeanDefinitionStoreException: IOException parsing XML document from ServletContext resource [/WEB-INF/applicationContext.xml]; nested exception is java.io.FileNotFoundException: Could not open ServletContext resource [/WEB-INF/applicationContext.xml]
	at org.springframework.beans.factory.xml.XmlBeanDefinitionReader.loadBeanDefinitions(XmlBeanDefinitionReader.java:344)
	at org.springframework.beans.factory.xml.XmlBeanDefinitionReader.loadBeanDefinitions(XmlBeanDefinitionReader.java:303)
	at org.springframework.beans.factory.support.AbstractBeanDefinitionReader.loadBeanDefinitions(AbstractBeanDefinitionReader.java:176)
	at org.springframework.beans.factory.support.AbstractBeanDefinitionReader.loadBeanDefinitions(AbstractBeanDefinitionReader.java:211)
	at org.springframework.beans.factory.support.AbstractBeanDefinitionReader.loadBeanDefinitions(AbstractBeanDefinitionReader.java:182)
	at org.springframework.web.context.support.XmlWebApplicationContext.loadBeanDefinitions(XmlWebApplicationContext.java:125)
	at org.springframework.web.context.support.XmlWebApplicationContext.loadBeanDefinitions(XmlWebApplicationContext.java:94)
	at org.springframework.context.support.AbstractRefreshableApplicationContext.refreshBeanFactory(AbstractRefreshableApplicationContext.java:138)
	at org.springframework.context.support.AbstractApplicationContext.obtainFreshBeanFactory(AbstractApplicationContext.java:580)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:460)
	at org.springframework.web.context.ContextLoader.configureAndRefreshWebApplicationContext(ContextLoader.java:410)
	at org.springframework.web.context.ContextLoader.initWebApplicationContext(ContextLoader.java:306)
	at org.springframework.web.context.ContextLoaderListener.contextInitialized(ContextLoaderListener.java:112)
	at org.apache.catalina.core.StandardContext.listenerStart(StandardContext.java:5118)
	at org.apache.catalina.core.StandardContext.startInternal(StandardContext.java:5634)
	at org.apache.catalina.util.LifecycleBase.start(LifecycleBase.java:145)
	at org.apache.catalina.core.ContainerBase$StartChild.call(ContainerBase.java:1571)
	at org.apache.catalina.core.ContainerBase$StartChild.call(ContainerBase.java:1561)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.io.FileNotFoundException: Could not open ServletContext resource [/WEB-INF/applicationContext.xml]
	at org.springframework.web.context.support.ServletContextResource.getInputStream(ServletContextResource.java:140)
	at org.springframework.beans.factory.xml.XmlBeanDefinitionReader.loadBeanDefinitions(XmlBeanDefinitionReader.java:330)
	... 21 more

```

- 我的配置文件是在classes文件夹下的，在web.xml已经配置了xml的路径的,但是比较奇怪的是走了/WEB-INF/applicationContext.xml它的默认路径去找了。

```
  <!-- springMvc servlet -->
    <servlet>
        <servlet-name>manager</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:applicationContext.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>manager</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
    
     
    <listener>
          <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class> 
    </listener>
     
```


- 后来慢慢的发现这个情况出现在`<listener>`为`org.springframework.web.context.ContextLoaderListener`的情况下，`org.springframework.web.util.IntrospectorCleanupListener`不会出现。

#### 二、 查看下代码看看是怎么回事

- 首先定位到ContextLoaderListener#contextInitialized方法

```
/**
	 
	public void contextInitialized(ServletContextEvent event) {
		this.contextLoader = createContextLoader();
		if (this.contextLoader == null) {
			this.contextLoader = this;
		}
		this.contextLoader.initWebApplicationContext(event.getServletContext());
	}
```
- 发现最后调用initWebApplicationContext初始化应用上下文,下一步到ContextLoader#initWebApplicationContext方法

```
...................省略
//如果上下文不存在则创建
if (this.context == null) {
				this.context = createWebApplicationContext(servletContext);
			}
			if (this.context instanceof ConfigurableWebApplicationContext) {
				ConfigurableWebApplicationContext cwac = (ConfigurableWebApplicationContext) this.context;
				if (!cwac.isActive()) {
					// The context has not yet been refreshed -> provide services such as
					// setting the parent context, setting the application context id, etc
					if (cwac.getParent() == null) {
						// The context instance was injected without an explicit parent ->
						// determine parent for root web application context, if any.
						ApplicationContext parent = loadParentContext(servletContext);
						cwac.setParent(parent);
					}
					//重点 最终到这里 配置和刷新上下文
					configureAndRefreshWebApplicationContext(cwac, servletContext);
				}
			}.
...................省略
```
- 再到了configureAndRefreshWebApplicationContext方法

```
........................省略
	  //这个wac是XmlWebApplicationContext
        wac.setServletContext(sc);
        //这个CONFIG_LOCATION_PARAM的值就是contextConfigLocation
		String configLocationParam = sc.getInitParameter(CONFIG_LOCATION_PARAM);
		//如果不等于null则设置配置文件路径 
		if (configLocationParam != null) {
			wac.setConfigLocation(configLocationParam);
		}

		// The wac environment's #initPropertySources will be called in any case when the context
		// is refreshed; do it eagerly here to ensure servlet property sources are in place for
		// use in any post-processing or initialization that occurs below prior to #refresh
		ConfigurableEnvironment env = wac.getEnvironment();
		if (env instanceof ConfigurableWebEnvironment) {
			((ConfigurableWebEnvironment) env).initPropertySources(sc, null);
		}

		customizeContext(sc, wac);
		wac.refresh();
```
- 好，上面是有配置contextConfigLocation的情况，那么如果没有配置contextConfigLocation的情况呢 ? 再往下看看这个XmlWebApplicationContext里面setConfigLocation方法。
- ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fac870c4e7fcc2d8980a410f2324ec6c.png)
- 可以看到XmlWebApplicationContext里面根本setConfigLocation方法，那么肯定会在它的父类。找找父类。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a0ba5e5c3b6c307871a99a85057ebd4b.png)
- 在AbstractRefreshableConfigApplicationContext找到了setConfigLocation方法,最终会把值放到configLocations数组里去。

```
public void setConfigLocation(String location) {
		setConfigLocations(StringUtils.tokenizeToStringArray(location, CONFIG_LOCATION_DELIMITERS));
	}

	/**
	 * Set the config locations for this application context.
	 * <p>If not set, the implementation may use a default as appropriate.
	 */
	public void setConfigLocations(String[] locations) {
		if (locations != null) {
			Assert.noNullElements(locations, "Config locations must not be null");
			this.configLocations = new String[locations.length];
			for (int i = 0; i < locations.length; i++) {
				this.configLocations[i] = resolvePath(locations[i]).trim();
			}
		}
		else {
			this.configLocations = null;
		}
	}
```
- 再找到了获取configLocations的方法

```
//得到配置文件路径
	protected String[] getConfigLocations() {
		return (this.configLocations != null ? this.configLocations : getDefaultConfigLocations());
	}

```
- 已经很明显了如果没有配置contextConfigLocation则会调用XmlWebApplicationContext#getDefaultConfigLocations方法

```
/** Default config location for the root context */
	public static final String DEFAULT_CONFIG_LOCATION = "/WEB-INF/applicationContext.xml";

	/** Default prefix for building a config location for a namespace */
	public static final String DEFAULT_CONFIG_LOCATION_PREFIX = "/WEB-INF/";

	/** Default suffix for building a config location for a namespace */
	public static final String DEFAULT_CONFIG_LOCATION_SUFFIX = ".xml";
 // 默认的配置文件路径
	@Override
	protected String[] getDefaultConfigLocations() {
		if (getNamespace() != null) {
			return new String[] {DEFAULT_CONFIG_LOCATION_PREFIX + getNamespace() + DEFAULT_CONFIG_LOCATION_SUFFIX};
		}
		else {
			return new String[] {DEFAULT_CONFIG_LOCATION};
		}
	}
```
#### 三、解决方案
- 到这里基本已经通了。

```
  <servlet>
        <servlet-name>manager</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:applicationContext.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>manager</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
```
- 这个地方的contextConfigLocation是针对DispatcherServlet(contextConfigLocation属性在父类FrameworkServlet里)里初始化上下文用的,对ContextLoaderListener不起作用。
- 看了下ContextLoaderListener的代码流程终于明白了,原来ContextLoaderListener要启动spring，需要得到配置文件的路径contextConfigLocation,如果不配置就会启用默认的路径。
- 加上一个就好了  `<context-param>`

 

```
<?xml version="1.0" encoding="UTF-8"?>

<web-app version="3.0" xmlns="http://java.sun.com/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://java.sun.com/xml/ns/javaee
     http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd">
  <display-name>Archetype Created Web Application</display-name>
  
   <!-- springMvc servlet -->
    <servlet>
        <servlet-name>manager</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:applicationContext.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>manager</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
    
     
    <listener>
  
          <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class> 
    </listener>
     
   <!-- 新加的 -->
    <context-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>classpath:applicationContext.xml</param-value>
    </context-param>
</web-app>

```
