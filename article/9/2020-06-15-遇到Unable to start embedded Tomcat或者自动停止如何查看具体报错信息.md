---
layout:					post
title:					"遇到Unable to start embedded Tomcat或者自动停止如何查看具体报错信息"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 本篇可以说是是上篇[spring boot项目打印banner后停止](https://sample.blog.csdn.net/article/details/106763497)的具体操作
- 遇到`org.springframework.context.ApplicationContextException: Unable to start web server; nested exception is org.springframework.boot.web.server.WebServerException: Unable to start embedded Tomcat`问题原因很多，网上说的一般情况不一样。
- 所谓“授人以鱼不如授人以渔”，本篇要给大家带来的就是自己如何debug程序去找症结所在。
- 首先找到spring boot创建web服务的地方`ServletWebServerApplicationContext#onRefresh`方法(当然这是web应用所以是这个类)

```java
protected void onRefresh() {
		super.onRefresh();
		try {
    		 // 很明显就是这个方法
			createWebServer();
		}
		catch (Throwable ex) {
			throw new ApplicationContextException("Unable to start web server", ex);
		}
	}
```

```java
private void createWebServer() {
		WebServer webServer = this.webServer;
		ServletContext servletContext = getServletContext();
		if (webServer == null && servletContext == null) {
			ServletWebServerFactory factory = getWebServerFactory();
			// 重点进入getWebServer方法
			this.webServer = factory.getWebServer(getSelfInitializer());
		}
		else if (servletContext != null) {
			try {
				getSelfInitializer().onStartup(servletContext);
			}
			catch (ServletException ex) {
				throw new ApplicationContextException("Cannot initialize servlet context",
						ex);
			}
		}
		initPropertySources();
	}
```
- 再进入`TomcatServletWebServerFactory#getWebServer`->`getTomcatWebServer`->`TomcatWebServer#TomcatWebServer(Tomcat tomcat, boolean autoStart)TomcatWebServer的构造方法`->`initialize`

```java
	private void initialize() throws WebServerException {
		TomcatWebServer.logger
				.info("Tomcat initialized with port(s): " + getPortsDescription(false));
		synchronized (this.monitor) {
			try {
				addInstanceIdToEngineName();

				Context context = findContext();
				context.addLifecycleListener((event) -> {
					if (context.equals(event.getSource())
							&& Lifecycle.START_EVENT.equals(event.getType())) {
						// Remove service connectors so that protocol binding doesn't
						// happen when the service is started.
						removeServiceConnectors();
					}
				});

				// Start the server to trigger initialization listeners
				this.tomcat.start();

				// We can re-throw failure exception directly in the main thread
				// 重点是这个，按照我的理解这个方法会收集启动时的异常并抛出
				rethrowDeferredStartupExceptions();

				try {
					ContextBindings.bindClassLoader(context, context.getNamingToken(),
							getClass().getClassLoader());
				}
				catch (NamingException ex) {
					// Naming is not enabled. Continue
				}

				// Unlike Jetty, all Tomcat threads are daemon threads. We create a
				// blocking non-daemon to stop immediate shutdown
				startDaemonAwaitThread();
			}
			catch (Exception ex) {
				stopSilently();
				throw new WebServerException("Unable to start embedded Tomcat", ex);
			}
		}
	}
```
- `TomcatWebServer#rethrowDeferredStartupExceptions` 重点是这个，按照我的理解这个方法会收集启动时的异常并抛出。
- 我在这里debug下就明了了，具体异常就有了。
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4659541a219947aad4cbce49802f740e.png)
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/80d8519f94666d21da566360a2d80d16.png)![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/95f2f58ae7c0214d6e5a6041e1d6d159.png)
- 第一个阻塞点的异常我处理完了，遇到第二个问题依然是自动停止的情况，于是我又在`AbstractApplicationContext#refresh`打断点，看具体是什么异常
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/960c5c3cd8d1cfe9cfc87d08ceebd783.png)
- 最后一个问题我发现居然还没有选择环境，只读取到默认的`default`，该断点在`ConfigFileApplicationListener#load`方法；目前看到该类是一个`EnvironmentPostProcessor`，主要功能就把它看成是处理处理文件的吧(环境事件的后处理器,不知道对不对，如果不对的话，请在评论下方指正，感谢您)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dc7b065a63a5bb9b99b6ee0e2dd9c08c.png)
- 在外层debug的时候看到的确只读了`application.properties`配置文件，该断点位置在`SpringApplication#run`方法
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/983fa7cefa3d4dcf565fe1184bd54dad.png)
- 于是我在`application.properties`(猜想他们可能是-D参数启动的吧)文件加入 `spring.profiles.active=dev`终于可以启动了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5fd16aa27c20439a4c4861c99ad18a5d.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ba0e551197b857763c28ceb8cde91d6d.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ed1ca113d9e6359d123e36b88667e3f9.png)
 - 主要根据错误信息把错误一一解决了改改配置就能启动了
- 本人水平有限，如果文章有误的地方，希望批评指正，感谢您的观看。


