---
layout:					post
title:					"Spring AOP源码解析(一)"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)

## 一、本章目标
- 由于我发现源码分析的文章有些过长了，所以我把它分成几篇文章，这样各位看官和我都会省点力气，我思路也会更清晰。
- 1、AOP简单介绍
- 2、使用Spring AOP
- 3、分析Spring AOP源码入口
## 二、简介
### 什么是AOP
 - AOP（Aspect Oriented Programming）称为`面向切面编程`，在程序开发中主要用来解决一些系统层面上的问题，AOP可以说是OOP(Object Oriented Programming,面向对象编程)的`补充和完善`。OOP引入封装、继承、多态等概念来建立一种对象层次结构。不过OOP允许开发者定义纵向的关系，但并不适合定义横向的关系。 
 
### 具体应用
- 比如日志，事务，权限等等，Struts2的拦截器设计就是基于AOP的思想。
 
### AOP相关术语
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fac8fbdf5602d10efbbd896ca1d91de1.png#pic_center)
- Aspect(切面):通常是一个类，里面可以定义切入点和通知。
- Advice(通知):AOP在特定的切入点上执行的增强处理，有before(前置),after(后置),afterReturning(最终),afterThrowing(异常),around(环绕)
- Pointcut(切入点):就是带有通知的连接点，在程序中主要体现为书写切入点表达式
- JointPoint(连接点):程序执行过程中明确的点(某个方法)，一般是方法的调用。被拦截到的点，因为Spring只支持方法类型的连接点，所以在Spring中连接点指的就是被拦截到的方法，实际上连接点还可以是字段或者构造器 
- weave(织入)：将切面应用到目标对象并生成新的代理对象的过程
- 目标对象(Target Object): 包含连接点的对象。也被称作被通知或被代理对象。POJO
- AOP代理(AOP Proxy)：AOP框架创建的对象，代理就是目标对象的加强。Spring中的AOP代理默认被代理对象有接口使用JDK动态代理，没有则使用CGLIB代理，jdk代理基于接口，cglib基于继承实现。

## 三、使用Spring Aop
- 本例子会在执行真正的方法前，执行一段逻辑。
### XML配置
- 首先xml配置`spring-base.xml`(我这里是老版本的源码)

```java
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:aop="http://www.springframework.org/schema/aop"
      xmlns:tx="http://www.springframework.org/schema/tx"
       xmlns:context="http://www.springframework.org/schema/context"
      xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd  http://www.springframework.org/schema/aop
        http://www.springframework.org/schema/aop/spring-aop-3.0.xsd http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.0.xsd"
	 >
  	<!-- 扫描包-->
   <context:component-scan base-package="com.zzq.core.test"/>
	<!-- 支持注解aop -->
    <aop:aspectj-autoproxy  />
    <!-- 注册Bean -->
    <bean id="testAopServiceImpl" class="com.zzq.core.test.service.impl.TestAopServiceImpl" />
        <bean id="operatorLogs" class="com.zzq.core.test.aop.OperatorLogs" />
	<!-- 配置AOP -->
      <aop:config >
        <aop:aspect id="operatorLogs" ref="operatorLogs">
        	<!-- 声明切点 -->
            <aop:pointcut id="serviceMethod" expression="execution(* com.zzq.core.test.service.impl..*.*(..))"  />
            <!-- 执行真正目标方法前执行 OperatorLogs#doBefore方法-->
            <aop:before method="doBefore" pointcut-ref="serviceMethod" /> 
        </aop:aspect>
    </aop:config>
</beans>
```
切面表达式详解：
| 标识符 | 含义 |
| --- | ---|
|execution| 表达式的主体 |
|第一个“*”号| 表示返回值可以任意类型 |
| com.zzq.core.test.service | AOP所切的服务的包名，需要进行横切的业务类 |
| “..” | 表示当前包及子包|
| 第二个“*”号| 表示类名，*即任意类名 |
|.*(..)|   表示任何方法名，括号表示参数，两个点表示任何参数类型 |
### Service代码
- 创建`TestAopServiceImpl`实现类和`ITestAopService`接口。
```java
package com.zzq.core.test.service;
public interface ITestAopService {
	  public int select(int id);
}
```

```java
package com.zzq.core.test.service.impl;
import com.zzq.core.test.service.ITestAopService;
public class TestAopServiceImpl implements ITestAopService {
	  		@Override
	     public int select(int id) {
	         System.out.println("Enter DaoImpl.select() " + id);
	          return 1;
	  	}
}
```
### 执行目标方法之前要执行的方法
- 创建AOP相关的类`OperatorLogs`，声明在执行真正方法前执行一段逻辑。

```java
package com.zzq.core.test.aop;
import org.aspectj.lang.JoinPoint;
public class OperatorLogs {
	private int order = 0;
    public void doBefore(JoinPoint joinPoint){ // 满足切面表达式的方法，执行前要执行的逻辑
        System.out.println("AOP Before Advice..." +(order++));
    }
}
```
### 启动类
- 创建启动类`BootStrap`。

```java
package com.zzq.core.test;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import com.zzq.core.test.entity.MyTestBean;
import com.zzq.core.test.service.ITestAopService;
public class BootStrap {
	public static void main(String[] args) throws Exception {	 
		ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("spring-base.xml");
		System.out.println(context.getBean("myTestBean") + "--" + ((MyTestBean) context.getBean("myTestBean")).getName());
		System.out.println("aop: " + context.getBean("testAopServiceImpl"));
		ITestAopService iTestAopService = (ITestAopService) context.getBean("testAopServiceImpl");
		System.out.println("====================开始调用select方法==================");
		@SuppressWarnings("unused")
		Integer a = iTestAopService.select(3);

	}
}
```
### 运行结果
- 运行测试类，结果如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a54595514b1917ad9f6c3ecae8373211.png#pic_center)
调用`TestAopServiceImpl#select`方法时首先执行的是`OperatorLogs#doBefore`方法。
## 四、源码分析
- 先来说一下AOP实现的基本流程：
	- 1、AOP非Spring默认标签，那么解析时会交给对应的NamespaceHandler处理，这个NamespaceHandler是AopNamespaceHandler。
	- 2、然后初始化解析器，解析阶段找到Advice（before、after之类的增强器）增强器注册到容器中。
	- 3、创建Bean时会判断是否满足切面表达式，如果满足会创建代理，寻找合适的Advice（增强器），构建执行器链。
	- 4、如果Bean是一个代理对象，在执行内部方法时，会先执行Advice（增强器）链，执行完后再执行真正的方法。

- 下面就来看这一切代码是如何实现的。
- 之前写过一篇文章，是[Spring自定义标签](https://blog.csdn.net/baidu_19473529/article/details/96509442)，AOP的功能实现并不是默认标签，而是使用自定义标签。
### Spring AOP的NamespaceHandler
- 从`spring-aop`的源码包中可以找到`spring.handlers`文件。内容如下所示。

```java
http\://www.springframework.org/schema/aop=org.springframework.aop.config.AopNamespaceHandler
```
- `AopNamespaceHandler`类代码如下所示。

```java
public class AopNamespaceHandler extends NamespaceHandlerSupport {

	/**
	 * Register the {@link BeanDefinitionParser BeanDefinitionParsers} for the
	 * '{@code config}', '{@code spring-configured}', '{@code aspectj-autoproxy}'
	 * and '{@code scoped-proxy}' tags.
	 */
	public void init() {
		//注册对应标签的处理类
		// In 2.0 XSD as well as in 2.1 XSD.
		//解析aop配置的类
		registerBeanDefinitionParser("config", new ConfigBeanDefinitionParser());
		// 支持注解aop
		registerBeanDefinitionParser("aspectj-autoproxy", new AspectJAutoProxyBeanDefinitionParser());
		registerBeanDefinitionDecorator("scoped-proxy", new ScopedProxyBeanDefinitionDecorator());
		// Only in 2.0 XSD: moved to context namespace as of 2.1
		registerBeanDefinitionParser("spring-configured", new SpringConfiguredBeanDefinitionParser());
	}
}
```
### 解析AOP标签
那么当遇到AOP标签（<aop:config >之类的）那么就会调用到`AopNamespaceHandler#init`初始化方法。随后会调用`BeanDefinitionParser#parse`方法（ConfigBeanDefinitionParser等实现了BeanDefinitionParser接口）。 
- 本例中，使用的是xml的方式，所以主要的类就是`ConfigBeanDefinitionParser`类，进入`parse`方法。代码如下所示。

```java
public BeanDefinition parse(Element element, ParserContext parserContext) {
		CompositeComponentDefinition compositeDef =
				new CompositeComponentDefinition(element.getTagName(), parserContext.extractSource(element));
		parserContext.pushContainingComponent(compositeDef);

		/*  
		 * 向Spring容器注册了一个BeanName为org.springframework.aop.config.internalAutoProxyCreator的Bean定义，可以自定义也可以使用Spring提供的（根据优先级来）
		Spring默认提供的是org.springframework.aop.aspectj.autoproxy.AspectJAwareAdvisorAutoProxyCreator，这个类是AOP的核心类
		在这个方法里面也会根据配置proxy-target-class和expose-proxy，设置是否使用CGLIB进行代理以及是否暴露最终的代理。
		* 
		*/
		configureAutoProxyCreator(parserContext, element);

		List<Element> childElts = DomUtils.getChildElements(element);
		for (Element elt: childElts) {
			String localName = parserContext.getDelegate().getLocalName(elt);
			if (POINTCUT.equals(localName)) {
				parsePointcut(elt, parserContext);
			}
			else if (ADVISOR.equals(localName)) {
				parseAdvisor(elt, parserContext);
			}
			else if (ASPECT.equals(localName)) {
 				// 解析 <aop:aspect>标签
				parseAspect(elt, parserContext);
			}
		}

		parserContext.popAndRegisterContainingComponent();
		return null;
	}

```
>向Spring容器注册了一个BeanName为org.springframework.aop.config.internalAutoProxyCreator的Bean定义，可以自定义也可以使用Spring提供的（根据优先级来）。
Spring默认提供的org.springframework.aop.aspectj.autoproxy.AspectJAwareAdvisorAutoProxyCreator，这个类是AOP的核心类
- 进入解析`<aop:aspect>`标签的代码，`parseAspect`方法代码如下所示。

```java
	private void parseAspect(Element aspectElement, ParserContext parserContext) {
		String aspectId = aspectElement.getAttribute(ID);
		String aspectName = aspectElement.getAttribute(REF);

		try {
			this.parseState.push(new AspectEntry(aspectId, aspectName));
			List<BeanDefinition> beanDefinitions = new ArrayList<BeanDefinition>();
			List<BeanReference> beanReferences = new ArrayList<BeanReference>();

			List<Element> declareParents = DomUtils.getChildElementsByTagName(aspectElement, DECLARE_PARENTS);
			for (int i = METHOD_INDEX; i < declareParents.size(); i++) {
				Element declareParentsElement = declareParents.get(i);
				beanDefinitions.add(parseDeclareParents(declareParentsElement, parserContext));
			}

			// We have to parse "advice" and all the advice kinds in one loop, to get the
			// ordering semantics right.
			NodeList nodeList = aspectElement.getChildNodes();
			boolean adviceFoundAlready = false;
			//即这个for循环只用来处理<aop:aspect>标签下的<aop:before>、<aop:after>、<aop:after-returning>、<aop:after-throwing method="">、<aop:around method="">这五个标签的。
			for (int i = 0; i < nodeList.getLength(); i++) {
				Node node = nodeList.item(i);
				if (isAdviceNode(node, parserContext)) {
					if (!adviceFoundAlready) {
						adviceFoundAlready = true;
						if (!StringUtils.hasText(aspectName)) {
							parserContext.getReaderContext().error(
									"<aspect> tag needs aspect bean reference via 'ref' attribute when declaring advices.",
									aspectElement, this.parseState.snapshot());
							return;
						}
						beanReferences.add(new RuntimeBeanReference(aspectName));
					}
					// 解析增强器
					AbstractBeanDefinition advisorDefinition = parseAdvice(
							aspectName, i, aspectElement, (Element) node, parserContext, beanDefinitions, beanReferences);
					beanDefinitions.add(advisorDefinition);
				}
			}

			AspectComponentDefinition aspectComponentDefinition = createAspectComponentDefinition(
					aspectElement, aspectId, beanDefinitions, beanReferences, parserContext);
			//构建了一个Aspect标签组件定义，并将Apsect标签组件定义推到ParseContext即解析工具上下文中，这部分代码不是关键
			parserContext.pushContainingComponent(aspectComponentDefinition);

			//拿到所有<aop:aspect>下的pointcut标签，进行遍历，由parsePointcut方法进行处理
			List<Element> pointcuts = DomUtils.getChildElementsByTagName(aspectElement, POINTCUT);
			for (Element pointcutElement : pointcuts) {
				parsePointcut(pointcutElement, parserContext);
			}
			parserContext.popAndRegisterContainingComponent();
		}
		finally {
			this.parseState.pop();
		}
	}

```
### 解析和注册Advice
- 解析增强器`parseAdvice`。

```java
	private AbstractBeanDefinition parseAdvice(
			String aspectName, int order, Element aspectElement, Element adviceElement, ParserContext parserContext,
			List<BeanDefinition> beanDefinitions, List<BeanReference> beanReferences) {

		try {
			this.parseState.push(new AdviceEntry(parserContext.getDelegate().getLocalName(adviceElement)));

			// create the method factory bean
			RootBeanDefinition methodDefinition = new RootBeanDefinition(MethodLocatingFactoryBean.class);
			methodDefinition.getPropertyValues().add("targetBeanName", aspectName);
			methodDefinition.getPropertyValues().add("methodName", adviceElement.getAttribute("method"));
			methodDefinition.setSynthetic(true);

			// create instance factory definition
			RootBeanDefinition aspectFactoryDef =
					new RootBeanDefinition(SimpleBeanFactoryAwareAspectInstanceFactory.class);
			aspectFactoryDef.getPropertyValues().add("aspectBeanName", aspectName);
			aspectFactoryDef.setSynthetic(true);

			// register the pointcut
			AbstractBeanDefinition adviceDef = createAdviceDefinition(
					adviceElement, parserContext, aspectName, order, methodDefinition, aspectFactoryDef,
					beanDefinitions, beanReferences);

			// configure the advisor
			// new一个新的RootBeanDefinition出来，Class类型是org.springframework.aop.aspectj.AspectJPointcutAdvisor
			RootBeanDefinition advisorDefinition = new RootBeanDefinition(AspectJPointcutAdvisor.class);
			advisorDefinition.setSource(parserContext.extractSource(adviceElement));
			advisorDefinition.getConstructorArgumentValues().addGenericArgumentValue(adviceDef);
			//用于判断<aop:aspect>标签中有没有"order"属性的，有就设置一下，"order"属性是用来控制切入方法优先级的。
			if (aspectElement.hasAttribute(ORDER_PROPERTY)) {
				advisorDefinition.getPropertyValues().add(
						ORDER_PROPERTY, aspectElement.getAttribute(ORDER_PROPERTY));
			}

			// register the final advisor
			//将BeanDefinition注册到DefaultListableBeanFactory中
			parserContext.getReaderContext().registerWithGeneratedName(advisorDefinition);

			return advisorDefinition;
		}
		finally {
			this.parseState.pop();
		}
	}
```
 
>1.根据织入方式（before、after这些）创建RootBeanDefinition，名为adviceDef即advice定义
2.将上一步创建的RootBeanDefinition写入一个新的RootBeanDefinition，构造一个新的对象，名为advisorDefinition，即advisor定义
3.将advisorDefinition注册到DefaultListableBeanFactory中

- 创建Advice的bean定义，`createAdviceDefinition`方法代码如下所示。

```java
private AbstractBeanDefinition createAdviceDefinition(
			Element adviceElement, ParserContext parserContext, String aspectName, int order,
			RootBeanDefinition methodDef, RootBeanDefinition aspectFactoryDef,
			List<BeanDefinition> beanDefinitions, List<BeanReference> beanReferences) {
		//创建的AbstractBeanDefinition实例是RootBeanDefinition，这和普通Bean创建的实例为GenericBeanDefinition不同。然后进入 getAdviceClass方法看一下
		
		RootBeanDefinition adviceDefinition = new RootBeanDefinition(getAdviceClass(adviceElement, parserContext));
		adviceDefinition.setSource(parserContext.extractSource(adviceElement));

		adviceDefinition.getPropertyValues().add(ASPECT_NAME_PROPERTY, aspectName);
		adviceDefinition.getPropertyValues().add(DECLARATION_ORDER_PROPERTY, order);

		if (adviceElement.hasAttribute(RETURNING)) {
			adviceDefinition.getPropertyValues().add(
					RETURNING_PROPERTY, adviceElement.getAttribute(RETURNING));
		}
		if (adviceElement.hasAttribute(THROWING)) {
			adviceDefinition.getPropertyValues().add(
					THROWING_PROPERTY, adviceElement.getAttribute(THROWING));
		}
		if (adviceElement.hasAttribute(ARG_NAMES)) {
			adviceDefinition.getPropertyValues().add(
					ARG_NAMES_PROPERTY, adviceElement.getAttribute(ARG_NAMES));
		}

		ConstructorArgumentValues cav = adviceDefinition.getConstructorArgumentValues();
		cav.addIndexedArgumentValue(METHOD_INDEX, methodDef);

		Object pointcut = parsePointcutProperty(adviceElement, parserContext);
		if (pointcut instanceof BeanDefinition) {
			cav.addIndexedArgumentValue(POINTCUT_INDEX, pointcut);
			beanDefinitions.add((BeanDefinition) pointcut);
		}
		else if (pointcut instanceof String) {
			RuntimeBeanReference pointcutRef = new RuntimeBeanReference((String) pointcut);
			cav.addIndexedArgumentValue(POINTCUT_INDEX, pointcutRef);
			beanReferences.add(pointcutRef);
		}

		cav.addIndexedArgumentValue(ASPECT_INSTANCE_FACTORY_INDEX, aspectFactoryDef);
		return adviceDefinition;
	}
	//既然创建Bean定义，必然该Bean定义中要对应一个具体的Class，不同的切入方式对应不同的Class：
	/**
	 * 
	 * before对应AspectJMethodBeforeAdvice
	*	After对应AspectJAfterAdvice
	*	after-returning对应AspectJAfterReturningAdvice
	*	after-throwing对应AspectJAfterThrowingAdvice
	*	around对应AspectJAroundAdvice
	 * */
	private Class getAdviceClass(Element adviceElement, ParserContext parserContext) {
		String elementName = parserContext.getDelegate().getLocalName(adviceElement);
		if (BEFORE.equals(elementName)) {
			return AspectJMethodBeforeAdvice.class;
		}
		else if (AFTER.equals(elementName)) {
			return AspectJAfterAdvice.class;
		}
		else if (AFTER_RETURNING_ELEMENT.equals(elementName)) {
			return AspectJAfterReturningAdvice.class;
		}
		else if (AFTER_THROWING_ELEMENT.equals(elementName)) {
			return AspectJAfterThrowingAdvice.class;
		}
		else if (AROUND.equals(elementName)) {
			return AspectJAroundAdvice.class;
		}
		else {
			throw new IllegalArgumentException("Unknown advice kind [" + elementName + "].");
		}
	}
```
-	毫无疑问本例得到的class肯定是`AspectJMethodBeforeAdvice`，如下图所示。
`![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0db6c9012440c97bef238a642c79f2f1.png#pic_center)
-	剩下的就是将Advice注册到Spring容器中,本部分完。


- 下一篇：[Spring AOP源码解析(二)](https://blog.csdn.net/baidu_19473529/article/details/124249476)