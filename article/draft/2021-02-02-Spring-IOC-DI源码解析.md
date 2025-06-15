
## 一切从Bean开始
- 早在1996年，Java还是一门新兴的、初出茅庐的编程语言。人们之所以关注它，仅仅是因为它可以使用Java的Applet来开发Web应用，并作为浏览器组件。但开发者发现这门新兴的语言还能做更多的事情。
- 与之前所有语言不同的是，Java让模块化构建复杂的系统成为可能。
- 当时开发软件一般使用传统的面向过程开发思想，但随着业务复杂性的增加，单纯的面向过程开发使得软件开发的效率并不高；20世纪80年代面向对象思想逐渐被人们熟知。
- 1996年12月，Sun公司发布了JavaBean 1.00-A规范，这套规范规定了一系列编码策略，使简单的Java对象不仅可以重用，还可以很轻松地构建更为复杂的应用。虽然JavaBean的设计能重用组件，但并没有因此而在逐渐兴起的软件行业崭露头角。毕竟相比于当时用C++等做出来的程序还是太简易了。
- 复杂的应用程序通常需要事物、安全、分布式等的支持。但JavaBean并未直接通过这些支持。后续到了1998年3月，Sun公司发布了EJB1.0（企业级JavaBean）规范，该规范把Java组件设计理念延伸服务器端，提供了许多企业级服务。实际上EJB（企业级JavaBean）除了名称和JavaBean有些雷同外，实际上和JavaBean关系不大。
- 然而EJB一直没能实现简化开发的目标，例如事物和安全，在部署描述符和配套代码实现等变得异常复杂，随着时间的推移，许多开始开发者寻找更简洁有效的方法。
- 新的编程技术DI和AOP的出现，Spring框架就是在这样的大环境应运而生，为简化开发的目标迎来了曙光，使Java组件开发理念重回正轨，能为JavaBen提供和之前EJB一样强大的功能。并且没有引入EJB那样的复杂性。
## Spring的设计初衷
- Spring是为降低企业级应用开发复杂性而设计的，最根本的使命是：简化开发。主要包括以下4个方面：
  - （1）基于POJO的轻量级和最小侵入性编程。
  - （2）通过依赖注入和面向接口实现松耦合。
  - （3）基于切面和惯性进行声明式编程。
  - （4）通过切面和模板减少样板代码。

## IOC/DI的概念
- IOC(Inversion of Control,控制反转)：是一种面向对象编程中通用的设计原则，可以用来减低计算机代码之间的耦合度，通过控制反转，对象在被创建的时候，由一个调控系统内所有对象的外界实体，将其所依赖的对象的引用传递(注入)给它。

> 早在2004年，马丁·福勒（Martin Fowler）就提出了“哪些方面的控制被反转了？”这个问题。他总结出是依赖对象的获得被反转了。控制被反转之后，获得依赖对象的过程由自身管理变为了由IOC容器主动注入。于是他给“控制反转”取了一个更适合的名字叫做“依赖注入”。

- “控制反转”其主要实现方式是“依赖注入”（Dependency Injection，简称DI）和“依赖查找”（Dependency Lookup）。
- 技术描述
 - A对象中用到了B的对象，一般情况下，需要在A类的代码中显式的new一个B对象。采用依赖注入技术之后，A的代码只需要定义一个B对象，不需要直接new来获得这个对象，而是通过相关的容器控制程序来将B对象在外部new出来并注入到A类里的引用中。而具体获取的方法、对象被获取时的状态由配置文件（如XML）来指定。
- 依赖注入
 - 基于接口。实现特定接口以供外部容器注入所依赖类型的对象。
 - 基于set方法。实现特定属性的public set方法，来让外部容器调用传入所依赖类型的对象。
 - 基于构造函数。实现特定参数的构造函数，在新建对象时传入所依赖类型的对象。
 - 基于注解声明。
- 依赖查找
 - 依赖查找更加主动，在需要的时候通过调用框架提供的方法来获取对象，获取时需要提供相关的配置文件路径、key等信息来确定获取对象的状态。
- 依赖注入和依赖查找的区别
 - 前者是被动的接收对象，在类A的实例创建过程中即创建了依赖的B对象，通过类型或名称来判断将不同的对象注入到不同的属性中，而后者是主动索取相应类型的对象，获得依赖对象的时间也可以在代码中自由控制。
## Spring系统架构
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-6nMWeOO4-1612231737688)(https://wparticle.sourceforge.io/wp-content/uploads/2021/01/20180505214030958.png)]
 
- 核心容器
 - 由spring-beans、spring-core、spring-context、spring-expression（Spring表达式语言）这4个模块组成。
 - spring-beans、spring-core是Spring的核心模块，BeanFactory使用控制反转对应用程序配置和依赖规范与实际程序业务代码进行分离。但BeanFactory并不会自动实例化Bean，只有当Bean被使用时才会进行实例化和依赖关系的装配。
 - spring-context模块在此基础上，扩展了BeanFactory，添加了Bean生命周期控制、事件监听器等功能。此外，还提供了许多企业级支持，如邮件、远程访问、任务调度等。ApplicationContext是该模块的核心接口，超类即BeanFactory。与之较大不同的是ApplicationContext会提前实例化所有单例Bean并装配好Bean的依赖关系。
- AOP和设备支持
 - AOP支持由spring-aop、spring-aspects、spring-instrument这3个模块组成。
 - spring-aop是AOP主要实现模块，AOP极大扩展了人们的编程思路。Spring以动态代理技术为基础，设计出一系列AOP横切实现（如：前置通知、返回通知、异常通知等）。
 - spring-aspects模块对AspectJ框架集成。Spring AOP使用了AspectJ注解。
 - spring-instrument提供了用于某些应用程序服务器的类工具支持和类加载器实现。
- 数据访问与集成
 - 由spring-jdbc、spring-tx、spring-orm、spring-oxm、spring-jms这5个模块组成。
 - spring-jdbc提供JDBC模板方式，用于简化对数据库的增删改查代码，减少样板代码。
 - spring-tx是对事物做了很好的封装，利用AOP实现，可以在任意一层配置，满足绝大部分本地事物的需求。
 - spring-orm提供了对流行的对象关系映射API的集成，包括JPA、JDO和Hibernate等。
 - spring-oxm可以将Java对象转换为一个xml文档。或者反过来，将一个XML文档转换为一个简单 Java对象。
 - spring-jms模块包含生产（produce）和消费（consume）消息的功能。可以集成一些消息中间件（如ActiveMq等）。
- Web组件
 - 由spring-web、spring-webmvc、spring-websocket、spring-webflux组成。
 - spring-web提供最基础的Web应用支持，通过Servlet或Listener初始化IOC容器。
 - spring-webmvc实现了Spring MVC的应用。
 - spring-websock实现与Web前端进行全双工协议（ws）。
 - spring-webflux是一个新的非阻塞函数式Reactive Web框架。
- 消息通信
 - spring-messaging是Spring 4新加入的模块，集成了基础的报文传输应用。
- 集成测试
 - spring-test模块提供测试支持，使本地调试更方便。
- 集成兼容
 - spring-framework-bom模块姐姐不同模块依赖版本问题。
## Spring核心类
- BeanFactory
 - BeanFactory（Bean工厂）是Spring IOC容器的基础。是Spring最高级抽象接口，它是工厂模式的实现，允许通过名称或类型等参数创建和得到对象，对IOC容器的基本行为做了定义。
![BeanFactory](https://i-blog.csdnimg.cn/blog_migrate/4ea6aa443253a1ef06c262badd963b73.png)
 - BeanFactory由三个重要的子类，分别是ListableBeanFactory、HierarchicalBeanFactory、AutowireCapableBeanFactory。默认实现类是DefaultListableBeanFactory，它实现了很多接口。ListableBeanFactory代表可列表化，HierarchicalBeanFactory表示继承关系，AutowireCapableBeanFactory定义装配规则。
- ApplicationContext
![ApplicationContext](https://i-blog.csdnimg.cn/blog_migrate/5724e41bb537ad03151c2e19efa35834.png)
 - 扩展了BeanFactory基本功能，提供了更多的附加服务（如：支持国际化、访问资源、支持事件）。
- BeanDefinition
![BeanDefinition](https://i-blog.csdnimg.cn/blog_migrate/e41c585fec32946ad5ee308c1bf55d4e.png)
 - IOC容器管理着各种各样的Bean、以及对象所需各种依赖，在Spring中是以BeanDefinition来描述每个Bean的。
- BeanDefinitionReader
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-cXHlVQEs-1612231737696)(https://wparticle.sourceforge.io/wp-content/uploads/2021/01/a28f1ef5b7db3a41ca841d1f919a1837.png)]
 - BeanDefinitionReader主管读取解析工作，将开发者的声明的对象配置解析成BeanDefinition。读取解析工作分得很细，因为声明方式有xml、Java Config的方式，xml解析的实现类就是XmlBeanDefinitionReader。
## 入口类
- XmlBeanFactory
- ClassPathXmlApplicationContext
- AnnotationConfigApplicationContext
- DispatcherServlet(如果是Spring MVC)
.....
## 源码分析
### 1、预刷新，记录下容器的启动时间、标记启动状态等
- AbstractApplicationContext#prepareRefresh
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-zWnXWMO4-1612231737698)(https://wparticle.sourceforge.io/wp-content/uploads/2021/02/103d8f32a8a9f86501c3e23d3c061a4e.png)]
### 2、创建BeanFactory实现类DefaultListableBeanFactory
- AbstractRefreshableApplicationContext#refreshBeanFactory
![](https://i-blog.csdnimg.cn/blog_migrate/226e0bcf97f1e6b9df763c70e01e6b8b.png)
### 3、加载Bean到BeanFactory中，扫描(scan)/xml声明/注解声明等方式通过一步步解析过程构建BeanDefinition集合
- 载入Bean定义AbstractXmlApplicationContext#loadBeanDefinitions
![](https://i-blog.csdnimg.cn/blog_migrate/23c705031d6c03a8e6f5b1f89abae19e.png)
- 这里会有处理默认标签和自定义标签（Spring扩展点之一）。
 - 默认标签的逻辑很简单，把Element封装成BeanDefinitionHolder对象，然后得到BeanDefinition注册到BeanFactory。
 ![](https://i-blog.csdnimg.cn/blog_migrate/158ab5b474a73c8d0d75e2a0028e1a0a.png)
 - 处理自定义标签，<context:component-scan>就属于自定义标签，先通过xml的文件头再找对应的NamespaceHandler
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-0HdPhHHh-1612231737703)(https://wparticle.sourceforge.io/wp-content/uploads/2021/02/302e09b4acb8bb49442ff14803390144.png)]
### 4、设置BeanFactory类加载器和设置几个特殊的Bean，AbstractApplicationContext#prepareBeanFactory
- 特殊的Bean直接从DefaultListableBeanFactory类resolvableDependencies属性寻找。
### 5、模板方法(钩子)，AbstractApplicationContext#postProcessBeanFactory
### 6、执行某些后置处理器（Spring扩展点之一，允许用户干预Bean的产生）
- AbstractApplicationContext#invokeBeanFactoryPostProcessors
- 将在此处执行BeanDefinitionRegistryPostProcessor、BeanFactoryPostProcessor后置处理器
### 7、向BeanFactory注册后置处理器（Spring扩展点之一，允许用户干预Bean的产生）
- AbstractApplicationContext#registerBeanPostProcessors
### 7、国际化AbstractApplicationContext#initMessageSource
### 8、初始化事件广播器AbstractApplicationContext#initApplicationEventMulticaster，默认实现类是SimpleApplicationEventMulticaster
### 9、模板方法（钩子）AbstractApplicationContext#onRefresh
- 例如Spring Boot在此处内嵌Web服务器
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-Hx074E04-1612231737704)(https://wparticle.sourceforge.io/wp-content/uploads/2021/02/e474d981898fae5b37265e6dd5602e46.png)]
### 10、注册事件监听器AbstractApplicationContext#registerListeners，添加ApplicationListener的实现类到事件广播器
### 11、初始化非懒加载的Bean,AbstractApplicationContext#finishBeanFactoryInitialization
##### 1、遍历BeanDefinition集合
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-usJSzWgu-1612231737705)(https://wparticle.sourceforge.io/wp-content/uploads/2021/02/997aa5a86f4dde4258661f60b396157c.png)]
##### 2、合并Bean定义，因为有可能Bean定义有更新，所以要合并，AbstractBeanFactory#getMergedLocalBeanDefinition
##### 3、验证BeanDefinition及覆盖， 处理lookup-method和replace-method配置，AbstractBeanFactory#checkMergedBeanDefinition
##### 4、通过BeanDefinition得到class，AbstractBeanFactory#resolveBeanClass
##### 5、推断构造方法（推断构造方法，使用后置处理器。如果没有覆盖默认的构造方法，使用默认的构造方法）
##### 6、实例化对象，大部分情况都是默认的构造方法，走AbstractAutowireCapableBeanFactory#instantiateBean
##### 7、缓存一个工厂,解决循环依赖：先从单例池拿，如果没有再到二级缓存，如果还没有到三级缓存拿（依靠提前暴露工厂）
- AbstractAutowireCapableBeanFactory#doCreateBean

`
addSingletonFactory(beanName, new ObjectFactory<Object>() {
				public Object getObject() throws BeansException {
					return getEarlyBeanReference(beanName, mbd, bean);
				}
			});
`

##### 9、填充Bean，注入依赖的属性，AbstractAutowireCapableBeanFactory#populateBean
- 使用后置处理器设置依赖的对象，如属性使用@Resource注解标记，则后置处理器是使用CommonAnnotationBeanPostProcessor。
- 先查找出依赖的属性
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-zrEenYHG-1612231737706)(https://wparticle.sourceforge.io/wp-content/uploads/2021/02/82571d9b64bf914074efc7e9413ea584.png)]
- 随后利用反射设置值
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-Xtwav78w-1612231737707)(https://wparticle.sourceforge.io/wp-content/uploads/2021/02/ae6e8e251750cfa040190d343774965c.png)]
##### 10、执行一部分Aware的接口
- AbstractAutowireCapableBeanFactory#invokeAwareMethods（执行BeanNameAware、BeanClassLoaderAware、BeanFactoryAware接口回调方法）
##### 11、执行生命周期初始化回调方法，一部分Aware的接口
- ApplicationContextAwareProcessor#postProcessBeforeInitialization，执行EnvironmentAware、EmbeddedValueResolverAware、ResourceLoaderAware、ApplicationEventPublisherAware、MessageSourceAware、ApplicationContextAware接口回调方法
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-odJ7O6GI-1612231737708)(https://wparticle.sourceforge.io/wp-content/uploads/2021/02/35026677960863ac6569580043bab3a4.png)]
- CommonAnnotationBeanPostProcessor#postProcessBeforeInitialization（实际上是进入父类InitDestroyAnnotationBeanPostProcessor#postProcessBeforeInitialization）
![](https://i-blog.csdnimg.cn/blog_migrate/82e380f89c42d51c60da5bef3ab8d823.png)
##### 12、接口生命周期的回调方法
- AbstractAutowireCapableBeanFactory#invokeInitMethods
- 执行InitializingBean接口的afterPropertiesSet方法和执行bean标签里init-method配置里的方法（如果同时有InitializingBean接口和init-method，都指向afterPropertiesSet方法，init-method的逻辑不会执行）
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-FU1A21lL-1612231737710)(https://wparticle.sourceforge.io/wp-content/uploads/2021/02/5412d60429d08994cc4d24d267a65476.png)]
##### 13、执行后置处理器postProcessAfterInitialization方法，如果满足条件此处会创建Aop代理，返回代理对象，AbstractAutowireCapableBeanFactory#applyBeanPostProcessorsAfterInitialization
##### 14、添加到单例池中
- DefaultSingletonBeanRegistry#getSingleton
![](https://i-blog.csdnimg.cn/blog_migrate/2fd7ec1abf6ac5a4a7f51262e579dc0e.png)
### 12、广播事件AbstractApplicationContext#finishRefresh
![](https://i-blog.csdnimg.cn/blog_migrate/87d9afaadc1e1c939ea2c8ba5bede7ef.png)