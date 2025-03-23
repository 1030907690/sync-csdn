---
layout:					post
title:					"@EventListener注解使用及源码解析"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
##### 一、简介
- @EventListener是一种事件驱动编程在spring4.2的时候开始有的，早期可以实现ApplicationListener接口, 想了解下ApplicationListener的可以参考下这篇文章[https://blog.csdn.net/baidu_19473529/article/details/86683365](https://blog.csdn.net/baidu_19473529/article/details/86683365)Spring为我们提供的一个事件监听、订阅的实现，内部实现原理是观察者设计模式；为的就是业务系统逻辑的解耦,提高可扩展性以及可维护性。事件发布者并不需要考虑谁去监听，监听具体的实现内容是什么，发布者的工作只是为了发布事件而已。
- 比如我们做一个电商系统,用户下单支付成功后，我们一般要发短信或者邮箱给用户提示什么的,这时候就可以把这个通知业务做成一个单独事件监听,等待通知就可以了；把它解耦处理。
##### 二、使用@EventListener注解
- 建立事件对象，当调用publishEvent方法是会通过这个bean对象找对应事件的监听。AddDataEvent.java

```
package com.rw.article.pay.event.bean;

import org.springframework.context.ApplicationEvent;

/**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: 新增mongodb数据事件
 * @date 2018/10/18 16:26
 */
public class AddDataEvent extends ApplicationEvent {

    public AddDataEvent(Object source) {
        super(source);
    }
    public AddDataEvent(Object source, Class clz, Object data) {
        super(source);
        this.clz = clz;
        this.data = data;
    }

    public AddDataEvent(Object source, Class clz, Object data, String modelName, String userAgent) {
        super(source);
        this.clz = clz;
        this.data = data;
        this.modelName = modelName;
        this.userAgent = userAgent;
    }



    /** 要更新的表对象 **/
    private Class clz;

    /** 操作的数据**/
    private Object data;


    /** 模块名称**/
    private String modelName;

    /** 浏览器标识 **/
    private String userAgent;


    public Class getClz() {
        return clz;
    }

    public void setClz(Class clz) {
        this.clz = clz;
    }

    public Object getData() {
        return data;
    }

    public void setData(Object data) {
        this.data = data;
    }

    public String getModelName() {
        return modelName;
    }

    public void setModelName(String modelName) {
        this.modelName = modelName;
    }

    public String getUserAgent() {
        return userAgent;
    }

    public void setUserAgent(String userAgent) {
        this.userAgent = userAgent;
    }
}

```

- 对应的监听AddDataEventListener .java

```
package com.rw.article.pay.event.listener;
import com.alibaba.fastjson.JSON;
import com.rw.article.pay.event.bean.AddDataEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

/**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: 新增数据的事件监听
 * @date 2018/10/18 16:29
 */
@Component
public class AddDataEventListener {
    private static Logger log = LoggerFactory.getLogger(AddDataEventListener.class);

    /*
    * 在AnnotationConfigUtils#registerAnnotationConfigProcessors注册了BeanDefinition 对应的是EventListenerMethodProcessor对象   ， AnnotationConfigUtils在AnnotationConfigServletWebServerApplicationContext构造方法里被加载
    * */

 	/**
	 * DefaultListableBeanFactory#中preInstantiateSingletons -> (beanName为org.springframework.context.event.internalEventListenerProcessor时得到EventListenerMethodProcessor)EventListenerMethodProcessor#afterSingletonsInstantiated this.processBean(factories, beanName, type)
	 * 然后把要执行的方法封装为ApplicationListenerMethodAdapter -> 添加到listener中 AbstractApplicationEventMulticaster#addApplicationListener
	 * */
 	// 该方法在 ApplicationListenerMethodAdapter 利用反射执行
    /**
     * 处理新增数据的事件
     **/
    @EventListener
    public void handleAddEvent(AddDataEvent event) {
        log.info("发布的data为:{}  ", JSON.toJSONString(event));
        
    }
}
```
- 建立测试类

```
package com.rw.article.pay.action;

import com.rw.article.pay.event.bean.AddDataEvent;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.annotation.Resource;

/**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: 测试的controller
 * @date 2019/7/24 17:13
 */
@Controller
@RequestMapping("/test")
public class TestController {


   @Resource
   private ApplicationContext applicationContext;


   @ResponseBody
   @RequestMapping("/testListener")
   public String testListener(){
      applicationContext.publishEvent(new AddDataEvent(this,TestController.class,"test"));
      return "success";
   }
}
```
- 结果是能够监听到的
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/14b33004aad38fabf00fd506e9cf8005.png)
- 如果要使用异步加上`@EnableAsync`注解，方法上加`@Async`注解，如下spring boot项目配置

```bash
@SpringBootApplication
@EnableAsync
public class XApplication{
    public static void main(String[] args) {
        ConfigurableApplicationContext run = new SpringApplicationBuilder(XApplication.class).web(true).run(args);
        run.publishEvent("test");
    }
}
```

```bash
    @Async
    @EventListener
    public void test(String wrapped){
        System.out.println("当前线程 "+Thread.currentThread().getName());
        System.out.println(wrapped);
    }
```
- 还可以配置线程池`taskExecutor`

```bash
@Configuration
public class GenericConfiguration {

    @Bean
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        //核心线程数：线程池创建时候初始化的线程数
        //最大线程数：线程池最大的线程数，只有在缓冲队列满了之后才会申请超过核心线程数的线程
        //缓冲队列：用来缓冲执行任务的队列
        //允许线程的空闲时间60秒：当超过了核心线程出之外的线程在空闲时间到达之后会被销毁
        //线程池名的前缀：设置好了之后可以方便我们定位处理任务所在的线程池
        //线程池对拒绝任务的处理策略：这里采用了CallerRunsPolicy策略，当线程池没有处理能力的时候，该策略会直接在 execute 方法的调用线程中运行被拒绝的任务；如果执行程序已关闭，则会丢弃该任务
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(20);
        executor.setKeepAliveSeconds(60);
        executor.setThreadNamePrefix("taskExecutor-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        return executor;
    }
}

```


##### 三、源码解析
- 原理还得从org.springframework.context.event.internalEventListenerProcessor
说起。
- 在AnnotationConfigUtils#registerAnnotationConfigProcessors注册了BeanDefinition 对应的是EventListenerMethodProcessor对象   ， 而AnnotationConfigUtils是在AnnotationConfigServletWebServerApplicationContext构造方法里被加载。这里要提一下AnnotationConfigServletWebServerApplicationContext，他是spring boot启动入口的重要类(我这里用的是spring boot所以是这个类),可以相当于以前用xml的ClassPathXmlApplicationContext。

```
 public static final String EVENT_LISTENER_PROCESSOR_BEAN_NAME =
      "org.springframework.context.event.internalEventListenerProcessor";

public static Set<BeanDefinitionHolder> registerAnnotationConfigProcessors(
			BeanDefinitionRegistry registry, @Nullable Object source) {

		 ................... 

		// 注册EventListenerMethodProcessor对象
		if (!registry.containsBeanDefinition(EVENT_LISTENER_PROCESSOR_BEAN_NAME)) {
			RootBeanDefinition def = new RootBeanDefinition(EventListenerMethodProcessor.class);
			def.setSource(source);
			beanDefs.add(registerPostProcessor(registry, def, EVENT_LISTENER_PROCESSOR_BEAN_NAME));
		}
		...........................

		return beanDefs;
	}
```

- 注册的EventListenerMethodProcessor对象会在初始化非懒加载对象的时候运行它的afterSingletonsInstantiated方法。
AbstractApplicationContext#finishBeanFactoryInitialization

```
 protected void finishBeanFactoryInitialization(ConfigurableListableBeanFactory beanFactory) {
 
   ............. 
   // 初始化非懒加载对象
   beanFactory.preInstantiateSingletons();
}
```
- DefaultListableBeanFactory#preInstantiateSingletons

```
 @Override
public void preInstantiateSingletons() throws BeansException {
    ..................

   // 触发所有适用bean的初始化后回调 主要是afterSingletonsInstantiated方法
   for (String beanName : beanNames) {
//如果beanName传入org.springframework.context.event.internalEventListenerProcessor 因为已经上面代码已经初始化，将从缓存中得到一个EventListenerMethodProcessor对象
      Object singletonInstance = getSingleton(beanName);
      if (singletonInstance instanceof SmartInitializingSingleton) {
         final SmartInitializingSingleton smartSingleton = (SmartInitializingSingleton) singletonInstance;
         if (System.getSecurityManager() != null) {
            AccessController.doPrivileged((PrivilegedAction<Object>) () -> {
               smartSingleton.afterSingletonsInstantiated();
               return null;
            }, getAccessControlContext());
         }
         else {
// 调用其afterSingletonsInstantiated方法
            smartSingleton.afterSingletonsInstantiated();
         }
      }
   }
}
```
- EventListenerMethodProcessor#afterSingletonsInstantiated

```
 @Override
public void afterSingletonsInstantiated() {
   List<EventListenerFactory> factories = getEventListenerFactories();
   ConfigurableApplicationContext context = getApplicationContext();
   String[] beanNames = context.getBeanNamesForType(Object.class);
   for (String beanName : beanNames) {
      if (!ScopedProxyUtils.isScopedTarget(beanName)) {
         Class<?> type = null;
         try {
            type = AutoProxyUtils.determineTargetClass(context.getBeanFactory(), beanName);
         }
         catch (Throwable ex) {
            // An unresolvable bean type, probably from a lazy bean - let's ignore it.
            if (logger.isDebugEnabled()) {
               logger.debug("Could not resolve target class for bean with name '" + beanName + "'", ex);
            }
         }
         if (type != null) {
            if (ScopedObject.class.isAssignableFrom(type)) {
               try {
                  Class<?> targetClass = AutoProxyUtils.determineTargetClass(
                        context.getBeanFactory(), ScopedProxyUtils.getTargetBeanName(beanName));
                  if (targetClass != null) {
                     type = targetClass;
                  }
               }
               catch (Throwable ex) {
                  // An invalid scoped proxy arrangement - let's ignore it.
                  if (logger.isDebugEnabled()) {
                     logger.debug("Could not resolve target bean for scoped proxy '" + beanName + "'", ex);
                  }
               }
            }
            try {
		// 重点是这个方法 处理bean
               processBean(factories, beanName, type);
            }
            catch (Throwable ex) {
               throw new BeanInitializationException("Failed to process @EventListener " +
                     "annotation on bean with name '" + beanName + "'", ex);
            }
         }
      }
   }
}
```
- <font color="red">EventListenerMethodProcessor#processBean;这里有一个重要的类就是ApplicationListenerMethodAdapter,spring把加入了@EventListener注解的方法封装进ApplicationListenerMethodAdapter对象里,然后我们publishEvent方法是,其实是调用的对应的ApplicationListenerMethodAdapter,然后里面是执行这个方法,这里可以看下ApplicationListenerMethodAdapter类的属性。</font>

```
public class ApplicationListenerMethodAdapter implements GenericApplicationListener {

   protected final Log logger = LogFactory.getLog(getClass());

   private final String beanName;

   private final Method method;

   private final Method targetMethod;

   private final AnnotatedElementKey methodKey;

   private final List<ResolvableType> declaredEventTypes;

   @Nullable
   private final String condition;

   private final int order;

   @Nullable
   private ApplicationContext applicationContext;

   @Nullable
   private EventExpressionEvaluator evaluator;
	..................................
}
```

```
protected void processBean(
      final List<EventListenerFactory> factories, final String beanName, final Class<?> targetType) {

   if (!this.nonAnnotatedClasses.contains(targetType)) {
      Map<Method, EventListener> annotatedMethods = null;
      try {
         // 拿到使用了@EventListener注解的方法
         annotatedMethods = MethodIntrospector.selectMethods(targetType,
               (MethodIntrospector.MetadataLookup<EventListener>) method ->
                     AnnotatedElementUtils.findMergedAnnotation(method, EventListener.class));
      }
      catch (Throwable ex) {
         // An unresolvable type in a method signature, probably from a lazy bean - let's ignore it.
         if (logger.isDebugEnabled()) {
            logger.debug("Could not resolve methods for bean with name '" + beanName + "'", ex);
         }
      }
      if (CollectionUtils.isEmpty(annotatedMethods)) {
         this.nonAnnotatedClasses.add(targetType);
         if (logger.isTraceEnabled()) {
            logger.trace("No @EventListener annotations found on bean class: " + targetType.getName());
         }
      }
      else {
         // Non-empty set of methods
         ConfigurableApplicationContext context = getApplicationContext();
         for (Method method : annotatedMethods.keySet()) {
            for (EventListenerFactory factory : factories) {
               // 判断是否支持该方法  这里用的DefaultEventListenerFactory spring5.0.8 写死的返回true
               if (factory.supportsMethod(method)) {
                  //选择方法  beanName 这里是AddDataEventListener的beanName 默认是addDataEventListener
                  Method methodToUse = AopUtils.selectInvocableMethod(method, context.getType(beanName));
                  // 这里是创建一个ApplicationListenerMethodAdapter对象
                  ApplicationListener<?> applicationListener =
                        factory.createApplicationListener(beanName, targetType, methodToUse);
                  if (applicationListener instanceof ApplicationListenerMethodAdapter) {
                     // 如果是ApplicationListenerMethodAdapter对象 就把context和evaluator传进去
                     ((ApplicationListenerMethodAdapter) applicationListener).init(context, this.evaluator);
                  }

                  // 添加到ApplicationListener事件Set集合中去
                  context.addApplicationListener(applicationListener);
                  break;
               }
            }
         }
         if (logger.isDebugEnabled()) {
            logger.debug(annotatedMethods.size() + " @EventListener methods processed on bean '" +
                  beanName + "': " + annotatedMethods);
         }
      }
   }
}
```

- 后面就是触发事件监听了AbstractApplicationContext#publishEvent

```
 @Override
public void publishEvent(ApplicationEvent event) {
   publishEvent(event, null);
}


protected void publishEvent(Object event, @Nullable ResolvableType eventType) {
	 
			..............................
		// Multicast right now if possible - or lazily once the multicaster is initialized
		if (this.earlyApplicationEvents != null) {
			this.earlyApplicationEvents.add(applicationEvent);
		}
		else {
		    // 进入multicastEvent
			getApplicationEventMulticaster().multicastEvent(applicationEvent, eventType);
		}

		// Publish event via parent context as well...
		if (this.parent != null) {
			if (this.parent instanceof AbstractApplicationContext) {
				((AbstractApplicationContext) this.parent).publishEvent(event, eventType);
			}
			else {
				this.parent.publishEvent(event);
			}
		}
	}

```
- SimpleApplicationEventMulticaster#multicastEvent->invokeListener->doInvokeListener

```
private void doInvokeListener(ApplicationListener listener, ApplicationEvent event) {
   try {
      listener.onApplicationEvent(event);
   }
   catch (ClassCastException ex) {
      String msg = ex.getMessage();
      if (msg == null || matchesClassCastMessage(msg, event.getClass().getName())) {
         // Possibly a lambda-defined listener which we could not resolve the generic event type for
         // -> let's suppress the exception and just log a debug message.
         Log logger = LogFactory.getLog(getClass());
         if (logger.isDebugEnabled()) {
            logger.debug("Non-matching event type for listener: " + listener, ex);
         }
      }
      else {
         throw ex;
      }
   }
}
```

- ApplicationListenerMethodAdapter#onApplicationEvent

```
@Override
public void onApplicationEvent(ApplicationEvent event) {
   processEvent(event);
}
ApplicationListenerMethodAdapter#processEvent
 public void processEvent(ApplicationEvent event) {
   Object[] args = resolveArguments(event);
   if (shouldHandle(event, args)) {
      // 执行真正的方法
      Object result = doInvoke(args);
      if (result != null) {
         handleResult(result);
      }
      else {
         logger.trace("No result object given - no result to handle");
      }
   }
}
```
- ApplicationListenerMethodAdapter#doInvoke

```
 protected Object doInvoke(Object... args) {
   Object bean = getTargetBean();
   ReflectionUtils.makeAccessible(this.method);
   try {
      return this.method.invoke(bean, args);
   }
   catch (IllegalArgumentException ex) {
      assertTargetBean(this.method, bean, args);
      throw new IllegalStateException(getInvocationErrorMessage(bean, ex.getMessage(), args), ex);
   }
   catch (IllegalAccessException ex) {
      throw new IllegalStateException(getInvocationErrorMessage(bean, ex.getMessage(), args), ex);
   }
   catch (InvocationTargetException ex) {
      // Throw underlying exception
      Throwable targetException = ex.getTargetException();
      if (targetException instanceof RuntimeException) {
         throw (RuntimeException) targetException;
      }
      else {
         String msg = getInvocationErrorMessage(bean, "Failed to invoke event listener method", args);
         throw new UndeclaredThrowableException(targetException, msg);
      }
   }
}
```

- ApplicationListenerMethodAdapter#getTargetBean

```
 protected Object getTargetBean() {
   Assert.notNull(this.applicationContext, "ApplicationContext must no be null");
   return this.applicationContext.getBean(this.beanName);
}
```
- 至此执行这个事件监听的方法执行完毕。如果文字有误的地方，希望批评指正，感谢您的观看。
