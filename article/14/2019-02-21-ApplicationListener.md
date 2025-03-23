---
layout:					post
title:					"ApplicationListener"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
#### 一、简介
- ApplicationListener接口是spring框架为开发者提供的一个扩展点。一般来说,一个我们新建一个项目,在启动时就需要初始化一些东西的(比如数据库的数据,一个对象，或者是某些配置)。并且使用ApplicationListener后可以拿到spring容器，功能是异常强大，好用。
#### 二、使用
- ApplicationRefreshedListener.java
```
@Component
public class ApplicationRefreshedListener implements ApplicationListener<ContextRefreshedEvent>{

	@Override
	public void onApplicationEvent(ContextRefreshedEvent event) {

		System.out.println("我的父容器为：" + event.getApplicationContext().getParent());
		 
	      System.out.println("初始化时我被调用了。" + event.getApplicationContext().getDisplayName());
	      //第一个方法 排除子容器 只要老大 没有parent，他就是老大
	      if(null == event.getApplicationContext().getParent()){
		      //TODO 写自己的业务逻辑
		      System.out.println( "---------");
	      }
	}

}
```
#### 三、源码解析
- AbstractApplicationContext#refresh方法

```
public void refresh() throws BeansException, IllegalStateException {
	 			........省略
				// Initialize event multicaster for this context.
				 // 初始化当前 ApplicationContext 的事件广播器 
				initApplicationEventMulticaster();
 	          ......省略
 	          // Last step: publish corresponding event.
				// 最后，广播事件，ApplicationContext 初始化完成
				finishRefresh();
				.......省略
	}
```
- AbstractApplicationContext#finishRefresh

```
protected void finishRefresh() {
		// Initialize lifecycle processor for this context.
		initLifecycleProcessor();

		// Propagate refresh to lifecycle processor first.
		getLifecycleProcessor().onRefresh();

		// Publish the final event.
		//发布ContextRefreshedEvent事件
		publishEvent(new ContextRefreshedEvent(this));

		// Participate in LiveBeansView MBean, if active.
		LiveBeansView.registerApplicationContext(this);
	}
```
- AbstractApplicationContext#publishEvent

```
public void publishEvent(ApplicationEvent event) {
		Assert.notNull(event, "Event must not be null");
		if (logger.isTraceEnabled()) {
			logger.trace("Publishing event in " + getDisplayName() + ": " + event);
		}
		getApplicationEventMulticaster().multicastEvent(event);
		//判断当前ApplicationContext有没有父级 ，如果有执行父级调用publishEvent 所以ApplicationListener被多次执行了
		if (this.parent != null) {
			this.parent.publishEvent(event);
		}
	}
```
- SimpleApplicationEventMulticaster#multicastEvent

```
public void multicastEvent(final ApplicationEvent event) {
      //getApplicationListeners  得到是event这个类型的事件列表,event在这里是ContextRefreshedEvent
		for (final ApplicationListener listener : getApplicationListeners(event)) {
			Executor executor = getTaskExecutor();
			if (executor != null) {
				executor.execute(new Runnable() {
					public void run() {
						//线程池执行onApplicationEvent 方法
						listener.onApplicationEvent(event);
					}
				});
			}
			else {
				//直接执行onApplicationEvent 方法
				listener.onApplicationEvent(event);
			}
		}
	}
```
#### 关于ApplicationListener的类会执行多次的原因
- 我自己测试了下某些情况下会执行多次,如下图
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3902510860c4be8fc7c58e312d29983a.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/42fd95ba2a77df1686490d8e7d834208.png)
- 在之前一篇文件就提过如果使用

> org.springframework.web.context.ContextLoaderListener

会产生2个容器,有父子关系，详情可见[spring报错parsing XML document from ServletContext resource [/WEB-INF/applicationContext.xml]](https://blog.csdn.net/baidu_19473529/article/details/82904301)

- 通过代码也就不难解释了，这里有个递归。

```
//判断当前ApplicationContext有没有父级 ，如果有执行父级调用publishEvent 所以ApplicationListener被多次执行了
		if (this.parent != null) {
			this.parent.publishEvent(event);
		}
```
- 要避免重复调用的问题,上面已经写了,加个判断就可以了。

