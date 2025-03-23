---
layout:					post
title:					"加了@RequestBody注解到底干了啥？@RequestBody源码分析"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 简介
- 一句话概括：`@RequestBody注解标记接收前端传递给后端的json数据，然后转成对象`。
- 我们有时会这样去写一个`controller`的方法，代码如下所示。

```
	@RequestMapping(value ="/test7")
	@ResponseBody
	public String test7(@RequestBody com.zzq.core.dto.TestReq testReq){
		System.out.println("test7 controller " + testReq.getUserId());
		return "test7 result :";
	}
```
- 这里加了`@RequestBody`注解后，就能接收前端传递给后端的json数据，然后将数据转为具体对象。下面就是我们扒下它的“底裤”，露出真相的时刻。
## 请求入口DispatcherServlet
- 我们知道`servlet`就是接收用户请求的。
- 在Spring MVC项目的时候，会写一个web.xml文件，而文件内容必定有关于`DispatcherServlet`的配置。如下配置。

```
...省略...
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
    ...省略...
```

- 即便是Spring Boot项目，向Tomcat(亦或者是Jetty、Undertow等)注册的`servlet`依然是`DispatcherServlet`。
- 所以我们找的入口类就是`DispatcherServlet`。
- 熟悉`servlet`都知道，有几个重要方法，比如`doGet，doPost,service`等等，这些方法都会调用`FrameworkServlet#processRequest`方法，然后`依次到DispatcherServlet的doService和doDispatch`方法。所以我们主要定位到doDispatch方法，代码如下所示。

```
protected void doDispatch(HttpServletRequest request, HttpServletResponse response) throws Exception {
		HttpServletRequest processedRequest = request;
		HandlerExecutionChain mappedHandler = null;
		boolean multipartRequestParsed = false;

		WebAsyncManager asyncManager = WebAsyncUtils.getAsyncManager(request);

		try {
			ModelAndView mv = null;
			Exception dispatchException = null;

			try {
				//检测是否有上传的头信息
				processedRequest = checkMultipart(request);
				multipartRequestParsed = (processedRequest != request);

				// Determine handler for the current request.
				//找出处理这个请求的handler链
				mappedHandler = getHandler(processedRequest, false);
				if (mappedHandler == null || mappedHandler.getHandler() == null) {
					noHandlerFound(processedRequest, response);
					return;
				}

				// Determine handler adapter for the current request.
				//根据handler得到adapter
				HandlerAdapter ha = getHandlerAdapter(mappedHandler.getHandler());

				// Process last-modified header, if supported by the handler.
				String method = request.getMethod();
				boolean isGet = "GET".equals(method);
				if (isGet || "HEAD".equals(method)) {
					//RequestMappingHandlerAdapter#getLastModified返回-1
					long lastModified = ha.getLastModified(request, mappedHandler.getHandler());
					if (logger.isDebugEnabled()) {
						logger.debug("Last-Modified value for [" + getRequestUri(request) + "] is: " + lastModified);
					}
					// 检测是否未改变 并且 是get请求
					if (new ServletWebRequest(request, response).checkNotModified(lastModified) && isGet) {
						return;
					}
				}
				
				//拦截器
				if (!mappedHandler.applyPreHandle(processedRequest, response)) { 
					//不为true则return
					return;
				}

				//如果是注解方式使用的是RequestMappingHandlerAdapter然后到父类AbstractHandlerMethodAdapter#handle方法
				// Actually invoke the handler.
				mv = ha.handle(processedRequest, response, mappedHandler.getHandler());

				if (asyncManager.isConcurrentHandlingStarted()) {
					return;
				}
				
				//mv不为null并且view不存在则应用默认的viewName
				applyDefaultViewName(request, mv);
				//主要执行拦截器postHandle方法
				mappedHandler.applyPostHandle(processedRequest, response, mv);
			}
			catch (Exception ex) {
				dispatchException = ex;
			}
			//处理处理程序选择和处理程序调用的结果，即要解析为ModelAndView或异常。
			processDispatchResult(processedRequest, response, mappedHandler, mv, dispatchException);
		}
		catch (Exception ex) {
			//主要是发生异常时执行拦截器afterCompletion方法
			triggerAfterCompletion(processedRequest, response, mappedHandler, ex);
		}
		catch (Error err) {
			triggerAfterCompletionWithError(processedRequest, response, mappedHandler, err);
		}
		finally {
			if (asyncManager.isConcurrentHandlingStarted()) {
				// Instead of postHandle and afterCompletion
				if (mappedHandler != null) {
					mappedHandler.applyAfterConcurrentHandlingStarted(processedRequest, response);
				}
			}
			else {
				// Clean up any resources used by a multipart request.
				if (multipartRequestParsed) {
					cleanupMultipart(processedRequest);
				}
			}
		}
	}
```

## HandlerMapping和HandlerAdapter
- 在DispatcherServlet#initStrategies方法中我们能看到如下代码。
```
	protected void initStrategies(ApplicationContext context) {
	  ...省略...
		//初始化HandlerMappings
		initHandlerMappings(context);
		//初始化HandlerAdapters
		initHandlerAdapters(context);
	...省略...
	}
```
- HandlerMapping和HandlerAdapter是可以多个的，Spring默认会注册几个`HandlerMapping`（如`BeanNameUrlHandlerMapping`、`SimpleUrlHandlerMapping`），有请求来的时候，去匹配到合适的那个。
- 在Spring MVC时代，我们通常会显式去注册一个HandlerMapping和HandlerAdapter，分别是`RequestMappingHandlerMapping`和`RequestMappingHandlerAdapter`。代码如下所示。

```
   <bean id="defaultAnnotationHandlerMapping" class="org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping"/>
    <bean id="annotationMethodHandlerAdapter" class="org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter">
        <property name="messageConverters">  
            <list>
                <ref bean="jacksonMessageConverter"/><!--  接收 application/json请求所需要的转换器  -->
            </list>
        </property>
    </bean>
    <!-- Jackson(JSON配置) -->
     <bean name="jacksonMessageConverter" class="org.springframework.http.converter.json.MappingJackson2HttpMessageConverter">
        <property name="supportedMediaTypes">
            <list>
                <value>application/json;charset=UTF-8</value>
            </list>
        </property>
        <property name="objectMapper">
            <bean class="com.fasterxml.jackson.databind.ObjectMapper">
                <property name="dateFormat">
                    <bean class="java.text.SimpleDateFormat">
                        <constructor-arg type="java.lang.String" value="yyyy-MM-dd HH:mm:ss"/>
                    </bean>
                </property>
            </bean>
        </property>
    </bean> 
```
- 当然要使用`MappingJackson2HttpMessageConverter`转换器还需要`jackson-databind、jackson-core、jackson-mapper-lgpl、jackson-mapper-asl、jackson-core-lgpl、jackson-core-asl`这些Jar包。
### HandlerMapping
- 我们注册的`RequestMappingHandlerMapping`，在初始化的时候会将`url的mapping`和`controller处理方法`存到`handlerMethods`变量中。`url`和`mapping`存在`urlMap`变量中。

```
private final Map<T, HandlerMethod> handlerMethods = new LinkedHashMap<T, HandlerMethod>();
private final MultiValueMap<String, T> urlMap = new LinkedMultiValueMap<String, T>();
```
- 在`DispatcherServlet.getHandler#getHandler`方法时，循环handlerMappings匹配。

```
 protected HandlerExecutionChain getHandler(HttpServletRequest request) throws Exception {
		//对应的不同实现controller的方式 使用不同的handlerMapping  (有实现 Controller接口 、 实现HttpRequestHandler、 使用注解@Controller)
		//handlerMappings 是DispatcherServlet.properties文件配置的org.springframework.web.servlet.HandlerMapping
		//注解使用DefaultAnnotationHandlerMapping  高版本的使用RequestMappingHandlerMapping
		//xml配置的controller使用BeanNameUrlHandlerMapping
		for (HandlerMapping hm : this.handlerMappings) {
			if (logger.isTraceEnabled()) {
				logger.trace(
						"Testing handler map [" + hm + "] in DispatcherServlet with name '" + getServletName() + "'");
			}
			HandlerExecutionChain handler = hm.getHandler(request);
			if (handler != null) {
				return handler;
			}
		}
		return null;
	}
```

- 一步步进去，当有请求来的时候根据url取出mapping。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8a7e487a5b72a0ca7b54b11854b422e8.png)
- 然后通过handlerMethods得到HandlerMethod，构建Match集合。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e0e7a57de94bc451606db0a226263343.png)
- 通过url，一步步匹配到handlerMethod，但是并不是返回handlerMethod，而是又包装一层，返回HandlerExecutionChain对象，代码如下所示。

```
	public final HandlerExecutionChain getHandler(HttpServletRequest request) throws Exception {
		Object handler = getHandlerInternal(request);
		if (handler == null) {
			handler = getDefaultHandler();
		}
		if (handler == null) {
			return null;
		}
		// Bean name or resolved handler?
		if (handler instanceof String) {
			String handlerName = (String) handler;
			handler = getApplicationContext().getBean(handlerName);
		}
		return getHandlerExecutionChain(handler, request);
	}
```
- getHandlerExecutionChain方法里面还会设置拦截器。
- 最后在循环到`RequestMappingHandlerMapping`的时候，能够匹配到，返回出HandlerExecutionChain对象。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5d8bbb750db545be4a00da877b5724e0.png)
### HandlerAdapter
- `HandlerAdapter`和`HandlerMapping`也是类似的逻辑，一样是支持多个。默认注册`HttpRequestHandlerAdapter`、`SimpleControllerHandlerAdapter`。
- 通过循环匹配，`DispatcherServlet#getHandlerAdapter`方法代码如下所示。

```
protected HandlerAdapter getHandlerAdapter(Object handler) throws ServletException {
		//遍历所有handlerAdapters 选择合适的handlerAdapters
		for (HandlerAdapter ha : this.handlerAdapters) {
			if (logger.isTraceEnabled()) {
				logger.trace("Testing handler adapter [" + ha + "]");
			}
			//判断这个adapter是否支持这个handler
			if (ha.supports(handler)) {
				return ha;
			}
		}
		throw new ServletException("No adapter for handler [" + handler +
				"]: The DispatcherServlet configuration needs to include a HandlerAdapter that supports this handler");
	}

```
- `AbstractHandlerMethodAdapter#supports`方法的逻辑。

```
 	public final boolean supports(Object handler) {
		//判断handler是否属于HandlerMethod  并且 supportsInternal 为true
		return (handler instanceof HandlerMethod && supportsInternal((HandlerMethod) handler));
	}
```

- 会匹配到`RequestMappingHandlerAdapter`，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/476ca4fbeb887611508422d0bb611d5c.png)
- 此时已经得到`HandlerAdapter`，然后经过，得到请求方式，执行拦截器的逻辑，再到`handle`方法逻辑。RequestMappingHandlerAdapter没有handle方法，所以进入父类，AbstractHandlerMethodAdapter#handle代码如下所示。

```
public final ModelAndView handle(HttpServletRequest request, HttpServletResponse response, Object handler)
			throws Exception {
		return handleInternal(request, response, (HandlerMethod) handler);
	}
```
- 然后RequestMappingHandlerAdapter#invokeHandleMethod -> ServletInvocableHandlerMethod#invokeAndHandle 不是本次重点，略过。
- 进入InvocableHandlerMethod#invokeForRequest代码如下所示。

```
	public final Object invokeForRequest(NativeWebRequest request, ModelAndViewContainer mavContainer,
			Object... providedArgs) throws Exception {
		// 得到参数
		Object[] args = getMethodArgumentValues(request, mavContainer, providedArgs);
		if (logger.isTraceEnabled()) {
			StringBuilder sb = new StringBuilder("Invoking [");
			sb.append(getBeanType().getSimpleName()).append(".");
			sb.append(getMethod().getName()).append("] method with arguments ");
			sb.append(Arrays.asList(args));
			logger.trace(sb.toString());
		}
		//此处执行反射调用controller的方法
		Object returnValue = doInvoke(args);
		if (logger.isTraceEnabled()) {
			logger.trace("Method [" + getMethod().getName() + "] returned [" + returnValue + "]");
		}
		return returnValue;
	}
```

## 参数解析
- 其实`getMethodArgumentValues`就是我们要找的方法。代码如下所示。

```
//获取当前请求的方法参数值
	private Object[] getMethodArgumentValues(NativeWebRequest request, ModelAndViewContainer mavContainer,
			Object... providedArgs) throws Exception {

		MethodParameter[] parameters = getMethodParameters();
		Object[] args = new Object[parameters.length];
		for (int i = 0; i < parameters.length; i++) {
			MethodParameter parameter = parameters[i];
			parameter.initParameterNameDiscovery(this.parameterNameDiscoverer);
			GenericTypeResolver.resolveParameterType(parameter, getBean().getClass());
			args[i] = resolveProvidedArgument(parameter, providedArgs);
			if (args[i] != null) {
				continue;
			}
			// 判断是否支持解析这个参数，如果支持会把参数解析器加入到缓存中
			if (this.argumentResolvers.supportsParameter(parameter)) {
				try {
					//解析请求参数
					args[i] = this.argumentResolvers.resolveArgument(
							parameter, mavContainer, request, this.dataBinderFactory);
					continue;
				}
				catch (Exception ex) {
					// 自己新增的打印异常
					ex.printStackTrace();
					if (logger.isDebugEnabled()) {
						logger.debug(getArgumentResolutionErrorMessage("Error resolving argument", i), ex);
					}
					throw ex;
				}
			}
			if (args[i] == null) {
				String msg = getArgumentResolutionErrorMessage("No suitable resolver for argument", i);
				throw new IllegalStateException(msg);
			}
		}
		return args;
	}
```
- `this.argumentResolvers.supportsParameter(parameter)`这段代码会判断是否支持这个参数，`这里其实又是一个适配器的套路(适配器模式)，Spring为我们提供了多种场景的支持`，如果支持会把参数解析器放到argumentResolverCache缓存中，代码如下所示。

```
private HandlerMethodArgumentResolver getArgumentResolver(MethodParameter parameter) {
		HandlerMethodArgumentResolver result = this.argumentResolverCache.get(parameter);
		if (result == null) {
			//遍历所有解析器，得到支持它的那个
			for (HandlerMethodArgumentResolver methodArgumentResolver : this.argumentResolvers) {
				if (logger.isTraceEnabled()) {
					logger.trace("Testing if argument resolver [" + methodArgumentResolver + "] supports [" +
							parameter.getGenericParameterType() + "]");
				}
				//判断methodArgumentResolver是否支持 
				if (methodArgumentResolver.supportsParameter(parameter)) {
					result = methodArgumentResolver;
					this.argumentResolverCache.put(parameter, result);
					break;
				}
			}
		}
		return result;
	}
```

- `args[i] = this.argumentResolvers.resolveArgument(parameter, mavContainer, request, this.dataBinderFactory); ` 真正解析请求参数。代码如下所示。

```
	public Object resolveArgument(
			MethodParameter parameter, ModelAndViewContainer mavContainer,
			NativeWebRequest webRequest, WebDataBinderFactory binderFactory)
			throws Exception {

		HandlerMethodArgumentResolver resolver = getArgumentResolver(parameter);
		Assert.notNull(resolver, "Unknown parameter type [" + parameter.getParameterType().getName() + "]");
		//如果使用RequestBody注解的,resolver一般为RequestResponseBodyMethodProcessor
		return resolver.resolveArgument(parameter, mavContainer, webRequest, binderFactory);
	}
```
- 这个解析器是`RequestResponseBodyMethodProcessor`，一步步跟进会进入RequestResponseBodyMethodProcessor#readWithMessageConverters方法，代码如下所示。

```
protected <T> Object readWithMessageConverters(NativeWebRequest webRequest, MethodParameter methodParam,
			Type paramType) throws IOException, HttpMediaTypeNotSupportedException {

		HttpServletRequest servletRequest = webRequest.getNativeRequest(HttpServletRequest.class);
		HttpInputMessage inputMessage = new ServletServerHttpRequest(servletRequest);
		// 得到注解
		RequestBody ann = methodParam.getParameterAnnotation(RequestBody.class);
		// 一般是true
		if (!ann.required()) {
			InputStream inputStream = inputMessage.getBody();
			if (inputStream == null) {
				return null;
			}
			else if (inputStream.markSupported()) {
				inputStream.mark(1);
				if (inputStream.read() == -1) {
					return null;
				}
				inputStream.reset();
			}
			else {
				final PushbackInputStream pushbackInputStream = new PushbackInputStream(inputStream);
				int b = pushbackInputStream.read();
				if (b == -1) {
					return null;
				}
				else {
					pushbackInputStream.unread(b);
				}
				inputMessage = new ServletServerHttpRequest(servletRequest) {
					@Override
					public InputStream getBody() {
						// Form POST should not get here
						return pushbackInputStream;
					}
				};
			}
		}
	 //一般会走到这里
		return super.readWithMessageConverters(inputMessage, methodParam, paramType);
	}
```
- AbstractMessageConverterMethodArgumentResolver#readWithMessageConverters代码如下所示。

```
protected <T> Object readWithMessageConverters(HttpInputMessage inputMessage,
			MethodParameter methodParam, Type targetType) throws IOException, HttpMediaTypeNotSupportedException {
	... 省略...
		for (HttpMessageConverter<?> converter : this.messageConverters) {
			if (converter instanceof GenericHttpMessageConverter) {
				GenericHttpMessageConverter genericConverter = (GenericHttpMessageConverter) converter;
				if (genericConverter.canRead(targetType, contextClass, contentType)) {
					if (logger.isDebugEnabled()) {
						logger.debug("Reading [" + targetType + "] as \"" +
								contentType + "\" using [" + converter + "]");
					}
					//json数据转为对象
					return genericConverter.read(targetType, contextClass, inputMessage);
				}
			} 
		...省略...
		throw new HttpMediaTypeNotSupportedException(contentType, this.allSupportedMediaTypes);
	}
```
- 这里的messageConverters变量的值就是我们前面注册的，`MappingJackson2HttpMessageConverter`，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2a18af39606ffea6bc8ae1a4f7a480db.png)
- 然后从MappingJackson2HttpMessageConverter#read调用到readJavaType方法,`this.objectMapper.readValue(inputMessage.getBody(), javaType);`是Jsckson的API,把InputStream转对象，代码如下所示。

```
private Object readJavaType(JavaType javaType, HttpInputMessage inputMessage) {
		try {
			//请求的InputStream流转为对象
			// 如果json数据是空的，此处会抛出 Could not read JSON: No content to map due to end-of-input
			return this.objectMapper.readValue(inputMessage.getBody(), javaType);
		}
		catch (IOException ex) {
			throw new HttpMessageNotReadableException("Could not read JSON: " + ex.getMessage(), ex);
		}
	}
```
- inputMessage.getBody()是InputStream对象，转为实体类。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/be2867f9247a3ab1bf7a7a83dbec515a.png)
## 执行controller的方法
- 当getMethodArgumentValues方法执行完成后，就能得到方法参数，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/32e5193f579bfa2f901bca92a8ebdb68.png)

- 得到方法参数后，就是执行controller中的方法，InvocableHandlerMethod#doInvoke代码如下所示。

```
	protected Object doInvoke(Object... args) throws Exception {
		ReflectionUtils.makeAccessible(getBridgedMethod());
		try {
			//此处执行反射调用controller的方法
			return getBridgedMethod().invoke(getBean(), args);
		}
		 ...省略...
	}
```
## 总结
- 本篇源码分析总结。
- 1、`HandlerMapping`阶段，匹配到一个`HandlerMapping`，通过Url找到某个controller的某个方法。返回`HandlerExecutionChain` 对象。
- 2、根据`HandlerMethod`匹配到某个HandlerAdapter，也就是我们的RequestMappingHandlerAdapter。
- 3、`this.argumentResolvers.supportsParameter(parameter)`匹配参数处理器，这里会匹配到`RequestResponseBodyMethodProcessor`。
- 4、从`messageConverters`集合中匹配出参数转换器，这里是`MappingJackson2HttpMessageConverter`。调用Jackson API转换成对象。
- 5、得到参数后，利用反射执行某个controller中某个方法。
- 从这里我们可以看出，Spring框架是相当灵活的，适配器模式是被其发挥得淋漓尽致。支持我们自定义`HandlerMapping`、`HandlerAdapter`、`messageConverters`等等，以适应更多的应用场景