---
layout:					post
title:					"手写精简版的springMVC框架"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
###整个设计流程图
![这里写图片描述](https://img-blog.csdn.net/20180304155006759?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)


一、web.xml配置servlet（启动时运行级别的servlet）

```
<!DOCTYPE web-app PUBLIC
 "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd" >

<web-app>
  <display-name>Archetype Created Web Application</display-name>
	<!-- 自定义spring mvc配置项目启动时加载 start -->
   <servlet>
   		<servlet-name>dispatcher</servlet-name>
   		<servlet-class>com.zzq.servlet.CustomDispatchrServlet</servlet-class>
		
		<init-param>
			<param-name>contextConfigLocation</param-name>
			<param-value>application.properties</param-value>
		</init-param>
		<load-on-startup>1</load-on-startup>
   </servlet> 
   <!-- 自定义spring mvc配置项目启动时加载 end -->

	<servlet-mapping>
		<servlet-name>dispatcher</servlet-name>
		<url-pattern>*.do</url-pattern>
	</servlet-mapping>
</web-app>

```

- 实现几个必须的自定义注解
CustomAutowired.java

```
package com.zzq.annotation;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface CustomAutowired {
	String value() default "";
}

```

CustomController.java

```
package com.zzq.annotation;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface CustomController {
	String value() default "";
}

```
CustomRequestMapping.java

```
package com.zzq.annotation;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target({ElementType.TYPE,ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface CustomRequestMapping {
	String value() default "";
}

```
CustomRequestParam.java

```
package com.zzq.annotation;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.PARAMETER)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface CustomRequestParam {
	String value() default "";
	
	boolean required() default true;
}

```

CustomService.java

```
package com.zzq.annotation;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface CustomService {
	String value() default "";
}

```

- 再写service以及实现类

```
package com.zzq.core.service;

public interface DemoService {
	public void test();
}

```

```
package com.zzq.core.service;

import com.zzq.annotation.CustomService;

@CustomService
public class DemoServiceImpl implements DemoService{

	@Override
	public void test() {
		// TODO Auto-generated method stub
		System.out.println("进入DemoServiceImpl test 方法");
		
	}
}

```

- 这是controller

```
package com.zzq.core.controller;


import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.zzq.annotation.CustomAutowired;
import com.zzq.annotation.CustomController;
import com.zzq.annotation.CustomRequestMapping;
import com.zzq.annotation.CustomRequestParam;
import com.zzq.core.service.DemoService;

/**
 * zhouzhongqing
 * 2017年11月29日22:11:56
 * 示例controller 
 * */
@CustomController
@CustomRequestMapping("/demo")
public class DemoController {

	@CustomAutowired
	private DemoService demoService;
	
	@CustomRequestMapping("/test.do") 
	public void test(HttpServletRequest request ,HttpServletResponse response ,@CustomRequestParam("password")String password) throws Exception{
		response.setContentType("text/html;charset=utf-8");
		response. setCharacterEncoding("UTF-8");
		String name = request.getParameter("name");
		 /*
		  * 如果没有配server.xml 的URIEncoding="UTF-8" 
		  * <Connector connectionTimeout="20000" port="8080" protocol="HTTP/1.1"  redirectPort="8443" URIEncoding="UTF-8" />
		 出现乱码就可以用这个转为中文String resultName = new String(name.getBytes("ISO-8859-1"),"utf-8"); */
		String resultName = new String(name.getBytes("ISO-8859-1"),"utf-8");
		System.out.println(demoService+"进入/demo/test方法--"+name +"----------"+resultName  +  " password ： " + password);
		demoService.test();
		// response.getWriter().write(resultName); // 返回到页面字符串
		 
		request.getRequestDispatcher("/index.jsp").forward(request, response);
	}
	
	
}

```


###二、写一个自定义的CustomDispatchrServlet.java

- 重写HttpServlet的init(ServletConfig config)方法， 读取配置文件application.properties，application.properties里配的是需要扫描的包的路径
```
scannerPackage=com.zzq.core
```

```
private Properties pro = new Properties();

		//加载配置文件
		initLoadConfig(config.getInitParameter("contextConfigLocation"));
		//扫描类
		scanner(pro.getProperty("scannerPackage"));
	
```

```
	private void initLoadConfig(String location) {
		InputStream is = this.getClass().getClassLoader().getResourceAsStream(location);
		try {
			pro.load(is);
		} catch (IOException e) {
			e.printStackTrace();
		}
		try {
			is.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
/**
	 * zhouzhongqing
	 * 2017年12月8日21:23:55
	 * 将全部的class添加到classs集合中
	 * */
	private void scanner(String scannerPackage) {
		URL url = this.getClass().getClassLoader().getResource("/"+scannerPackage.replaceAll("\\.", "/"));
		File  dir = new File(url.getFile());
		for (File file : dir.listFiles()) {
			if(file.isDirectory()){
				scanner(scannerPackage+"."+file.getName());
			}else{
				String calssName= scannerPackage + "." + file.getName().replace(".class", "");
				classs.add(calssName);
			}
		}
	}

```


 - 类初始化,并装载到ioc容器中

```
private Map<String,Object> ioc = new HashMap<>();
//类初始化,并装载到ioc容器中
instance();
```

/**
	 * Controller注解和Service注解保存到ioc中建立对应关系
	 * */
	private void instance() {
		if(null == classs || classs.size() <= 0){
			return;
		}
		try {
		for (String className : classs) {
			
				Class<?> clazz = Class.forName(className);
				if(clazz.isAnnotationPresent(CustomController.class)){
					//保存到ioc中
					String beanName = lowerFirst(clazz.getSimpleName());
					ioc.put(beanName, clazz.newInstance());
				}else if(clazz.isAnnotationPresent(CustomService.class)){
					CustomService service = clazz.getAnnotation(CustomService.class);
					String beanName = service.value();
					if(null != beanName && !"".equals(beanName.trim())){
						//如果是自定义了名称
						ioc.put(beanName,clazz.newInstance());
					}else{
						//如果没有定义名称就根据类名首字母小写命名
						beanName = lowerFirst(clazz.getSimpleName());
						ioc.put(beanName, clazz.newInstance());
					}
					//接口
					Class<?> [] interfaces = clazz.getInterfaces();
					for (Class<?> clz : interfaces) {
						//clz.getName() : 接口的名称    clazz.newInstance() ： 接口的实现类实例
						ioc.put(clz.getName(), clazz.newInstance());
					}
					
				}
		}
		} catch (Exception e) {
			e.printStackTrace();
		}
		
	}


- 依赖注入，给加了Autowired注解的属性设置对应的值

```
//注入值
autowired();
```

```
/**
	 * 给加了Autowired注解的属性设置对应的值
	 * **/
	private void autowired() {

		if(null == ioc ||  ioc.size() <= 0){
			return;
		}
		
		for (Map.Entry<String, Object> entry : ioc.entrySet()) {
			Field [] fields = entry.getValue().getClass().getDeclaredFields();
			for (Field field : fields) {
				//判断这个类的属性是否加了CustomAutowired注解
				if(!field.isAnnotationPresent(CustomAutowired.class)){
					continue;
				}
				CustomAutowired autowired = field.getAnnotation(CustomAutowired.class);
				String beanName = autowired.value();
				if(null == beanName || "".equals(beanName.trim()) ){
					//如果没有自定义命名 给加了CustomAutowired注解设置它类型名称默认值
					beanName = field.getType().getName();
				}
				
				//即使是私有对象也要注入值
				field.setAccessible(true);
				try {
					//利用反射给这个类 entry.getValue()的field属性设置这个值 ioc.get(beanName)
					field.set(entry.getValue(), ioc.get(beanName));
				} catch (IllegalArgumentException | IllegalAccessException e) {
					//e.printStackTrace();
					System.err.println("注入异常--"+entry.getValue());
				}
				
			}
		}
	}
```

- 映射，将一个url映射到项目类的某个方法,建立url和method直接的关系

```
//映射，将一个url映射到项目类的某个方法
		initHandelMapping();
```

```
/**
	 * 初始化加Controller注解的类,把地址和方法添加到handlerMapping映射中
	 * **/
	private void initHandelMapping() {
		if(null == ioc ||  ioc.size() <= 0){
			return;
		}
		for (Map.Entry<String, Object> entry : ioc.entrySet()) {
			Class<?> clazz = entry.getValue().getClass();
			//判断是否加了CustomController注解
			if(!clazz.isAnnotationPresent(CustomController.class)){
				continue;
			}

			String  url = "";
			if(clazz.isAnnotationPresent(CustomRequestMapping.class)){
				CustomRequestMapping requestMapping = clazz.getAnnotation(CustomRequestMapping.class);
				url = requestMapping.value();
			
			}
			
			//得到这个类里面的所以方法
			Method [] methods = clazz.getMethods();
			for (Method method : methods) {
				//判断方法是否加了CustomRequestMapping注解
				if(!method.isAnnotationPresent(CustomRequestMapping.class)){
					continue;
				}
				
				CustomRequestMapping requestMapping = method.getAnnotation(CustomRequestMapping.class);
				//String mUrl = ("/"+url+ requestMapping.value()).replaceAll("/+", "/");
				//handlerMapping.put(mUrl, method);
				//地址
				String regex = ("/"+url+ requestMapping.value()).replaceAll("/+", "/");
				//pattern() 返回正则表达式的字符串形式,其实就是返回Pattern.complile(String regex)的regex参数
				Pattern pattern = Pattern.compile(regex);
				//地址和方法建立对应关系
				handlerMapping.add(new Handler(pattern, entry.getValue(), method));
				System.out.println("mapping : "+ regex + "  method: " + method );
				
				
			}
			

		}
	}
		
```
每一个步骤已经写完了。运行结果展示:

![这里写图片描述](https://img-blog.csdn.net/20180304161359344?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

![这里写图片描述](https://img-blog.csdn.net/20180304161410292?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
###完整的CustomDispatchrServlet.java源码

```
package com.zzq.servlet;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.lang.annotation.Annotation;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.URL;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Properties;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.zzq.annotation.CustomAutowired;
import com.zzq.annotation.CustomController;
import com.zzq.annotation.CustomRequestMapping;
import com.zzq.annotation.CustomRequestParam;
import com.zzq.annotation.CustomService;

/***
 * zhouzhongqing
 * 2017年11月29日22:24:14
 * 自定义的DispatchrServlet
 * */
public class CustomDispatchrServlet extends HttpServlet {

	
	private Properties pro = new Properties();
	
	private List<String> classs = new LinkedList<>();
	
	private Map<String,Object> ioc = new HashMap<>();

//	private Map<String,Method> handlerMapping = new HashMap<>();
	
	private List<Handler> handlerMapping = new LinkedList<>();

	@Override  
	public void init(ServletConfig config) throws ServletException {
		System.out.println("/************************* dispatchrServlet  init start *************************/");
		
		//加载配置文件
		initLoadConfig(config.getInitParameter("contextConfigLocation"));
		//扫描类
		scanner(pro.getProperty("scannerPackage"));
		//类初始化,并装载到ioc容器中
		instance();
		
		//依赖注入
		autowired();
		
		//映射，将一个url映射到项目类的某个方法
		initHandelMapping();
		
		System.out.println("/************************* dispatchrServlet init end *************************/");
	}
	
	/**
	 * 初始化加Controller注解的类,把地址和方法添加到handlerMapping映射中
	 * **/
	private void initHandelMapping() {
		if(null == ioc ||  ioc.size() <= 0){
			return;
		}
		for (Map.Entry<String, Object> entry : ioc.entrySet()) {
			Class<?> clazz = entry.getValue().getClass();
			//判断是否加了CustomController注解
			if(!clazz.isAnnotationPresent(CustomController.class)){
				continue;
			}

			String  url = "";
			if(clazz.isAnnotationPresent(CustomRequestMapping.class)){
				CustomRequestMapping requestMapping = clazz.getAnnotation(CustomRequestMapping.class);
				url = requestMapping.value();
			
			}
			
			//得到这个类里面的所以方法
			Method [] methods = clazz.getMethods();
			for (Method method : methods) {
				//判断方法是否加了CustomRequestMapping注解
				if(!method.isAnnotationPresent(CustomRequestMapping.class)){
					continue;
				}
				
				CustomRequestMapping requestMapping = method.getAnnotation(CustomRequestMapping.class);
				//String mUrl = ("/"+url+ requestMapping.value()).replaceAll("/+", "/");
				//handlerMapping.put(mUrl, method);
				//地址
				String regex = ("/"+url+ requestMapping.value()).replaceAll("/+", "/");
				//pattern() 返回正则表达式的字符串形式,其实就是返回Pattern.complile(String regex)的regex参数
				Pattern pattern = Pattern.compile(regex);
				//地址和方法建立对应关系
				handlerMapping.add(new Handler(pattern, entry.getValue(), method));
				System.out.println("mapping : "+ regex + "  method: " + method );
				
				
			}
			

		}
	}
		
	
	/**
	 * 给加了Autowired注解的属性设置对应的值
	 * **/
	private void autowired() {

		if(null == ioc ||  ioc.size() <= 0){
			return;
		}
		
		for (Map.Entry<String, Object> entry : ioc.entrySet()) {
			Field [] fields = entry.getValue().getClass().getDeclaredFields();
			for (Field field : fields) {
				//判断这个类的属性是否加了CustomAutowired注解
				if(!field.isAnnotationPresent(CustomAutowired.class)){
					continue;
				}
				CustomAutowired autowired = field.getAnnotation(CustomAutowired.class);
				String beanName = autowired.value();
				if(null == beanName || "".equals(beanName.trim()) ){
					//如果没有自定义命名 给加了CustomAutowired注解设置它类型名称默认值
					beanName = field.getType().getName();
				}
				
				//即使是私有对象也要注入值
				field.setAccessible(true);
				try {
					//利用反射给这个类 entry.getValue()的field属性设置这个值 ioc.get(beanName)
					field.set(entry.getValue(), ioc.get(beanName));
				} catch (IllegalArgumentException | IllegalAccessException e) {
					//e.printStackTrace();
					System.err.println("注入异常--"+entry.getValue());
				}
				
			}
		}
	}

	/**
	 * Controller注解和Service注解保存到ioc中建立对应关系
	 * */
	private void instance() {
		if(null == classs || classs.size() <= 0){
			return;
		}
		try {
		for (String className : classs) {
			
				Class<?> clazz = Class.forName(className);
				if(clazz.isAnnotationPresent(CustomController.class)){
					//保存到ioc中
					String beanName = lowerFirst(clazz.getSimpleName());
					ioc.put(beanName, clazz.newInstance());
				}else if(clazz.isAnnotationPresent(CustomService.class)){
					CustomService service = clazz.getAnnotation(CustomService.class);
					String beanName = service.value();
					if(null != beanName && !"".equals(beanName.trim())){
						//如果是自定义了名称
						ioc.put(beanName,clazz.newInstance());
					}else{
						//如果没有定义名称就根据类名首字母小写命名
						beanName = lowerFirst(clazz.getSimpleName());
						ioc.put(beanName, clazz.newInstance());
					}
					//接口
					Class<?> [] interfaces = clazz.getInterfaces();
					for (Class<?> clz : interfaces) {
						//clz.getName() : 接口的名称    clazz.newInstance() ： 接口的实现类实例
						ioc.put(clz.getName(), clazz.newInstance());
					}
					
				}
		}
		} catch (Exception e) {
			e.printStackTrace();
		}
		
	}
	
	public static void main(String[] args) {
		String a = "";
		if(null != a && !"".equals(a.trim())){
			System.out.println(a);
			//自定义了名称
		}
	}

	
	/**
	 * zhouzhongqing
	 * 2017年12月8日21:23:55
	 * 将全部的class添加到classs集合中
	 * */
	private void scanner(String scannerPackage) {
		URL url = this.getClass().getClassLoader().getResource("/"+scannerPackage.replaceAll("\\.", "/"));
		File  dir = new File(url.getFile());
		for (File file : dir.listFiles()) {
			if(file.isDirectory()){
				scanner(scannerPackage+"."+file.getName());
			}else{
				String calssName= scannerPackage + "." + file.getName().replace(".class", "");
				classs.add(calssName);
			}
		}
	}

	private void initLoadConfig(String location) {
		InputStream is = this.getClass().getClassLoader().getResourceAsStream(location);
		try {
			pro.load(is);
		} catch (IOException e) {
			e.printStackTrace();
		}
		try {
			is.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		doPost(req, resp);
	}
	
	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		System.out.println("doPost");
		dispatchr(req, resp);
		resp.getWriter().flush();
	}
	
	
	
	
	private void dispatchr(HttpServletRequest req, HttpServletResponse resp) {
		
		/*try {
			if(null == handlerMapping ||handlerMapping.size() <= 0){
				resp.getWriter().write("404 Not Found");	
			}
			boolean isPattern = false;
			String url =  req.getRequestURI();
			String contextPath = req.getContextPath();
			System.out.println(contextPath + "----"+url + handlerMapping);
			url = url.replace(contextPath, "").replaceAll("/+", "/");
			for (Entry<String, Method> mapping: handlerMapping.entrySet()) {
				System.out.println("mapping映射 "+mapping.getKey()+"------"+url );
				if(mapping.getKey().equals(url)){
					System.out.println(mapping.getValue());
					isPattern = true;
					mapping.getValue();
					break;
				}
			}
			
			if(!isPattern){
				System.err.println("404");
				resp.getWriter().write("404 Not Found");
			}
			
		} catch (Exception e) {
			try {
				resp.getWriter().write("404" + Arrays.toString(e.getStackTrace()));
			} catch (IOException e1) {
				e1.printStackTrace();
			}
		}
		*/
		try {
			Handler handler = getHandler(req);
			if(null == handler){
				resp.getWriter().write("404 Not Found");
			}
			
			//得到全部的参数类型
			Class<?> [] paramTypes = handler.method.getParameterTypes();
			
			Object [] paramValues = new Object[paramTypes.length];
			
			//得到所有的请求参数
			Map<String, String[]> params = req.getParameterMap();
			for (Entry<String, String[]> param : params.entrySet()) {
				String value = Arrays.toString(param.getValue()).replaceAll("\\[|\\]", "").replaceAll(",\\s", ",");
				//判断传过来的参数名是否是加了CustomRequestParam自定义参数注解的
				if(!handler.paramIndexMapping.containsKey(param.getKey())){
					continue;
				}
				//得到这个参数的位置
				int index = handler.paramIndexMapping.get(param.getKey());
				//转换成对应的参数类型 ,保存到paramValues数组中
				paramValues[index] = convert(paramTypes[index],value);
				
			}
			
			//获取方法参数中HttpServletRequest.class.getName()的位置
			int reqIndex = null == handler.paramIndexMapping.get(HttpServletRequest.class.getName()) ? -1 :  handler.paramIndexMapping.get(HttpServletRequest.class.getName());
			if(-1 != reqIndex){
				paramValues[reqIndex] = req;
			}
			
			//获取方法参数中HttpServletResponse.class.getName()的位置
			int respIndex = null == handler.paramIndexMapping.get(HttpServletResponse.class.getName()) ? -1 : handler.paramIndexMapping.get(HttpServletResponse.class.getName());
			if(-1 != respIndex){
				paramValues[respIndex] = resp;
			}
			//反射调用controller中的方法
			handler.method.invoke(handler.controller, paramValues);
		} catch (Exception e) {
			try {
				resp.getWriter().write(" error " +e);
				e.printStackTrace();
			} catch (IOException e1) {
				e1.printStackTrace();
			}
		}
		
	}

	private Object convert(Class<?> type, String value) {
		if( type == Integer.class){
			return Integer.valueOf(value);
		}
		return value;
	}

	private Handler getHandler(HttpServletRequest req) {

		if(handlerMapping.isEmpty()){
			return null;
		}
		String url = req.getRequestURI();
		String contextPath = req.getContextPath();
		url = url.replace(contextPath, "").replaceAll("/+", "/");
		for (Handler handler : handlerMapping) {
			Matcher matcher = handler.pattern.matcher(url);
			//判断是否有这个url
			if(!matcher.matches()){
				continue;
			}
			return handler;
		}
		
		return null;
	}

	private String lowerFirst(String str){
		char [] chars = str.toCharArray();
		chars[0] += 32;
		return String.valueOf(chars);
	}
	
	
	private class Handler{
		
		protected Object controller;//保存方法实例
		protected Method method; //保存映射方法
		protected Pattern pattern;
		protected Map<String,Integer> paramIndexMapping;//方法的参数
		
		protected Handler(Pattern pattern,Object controller,Method method){
			this.controller = controller;
			this.method = method;
			this.pattern = pattern;
			paramIndexMapping = new HashMap<>();
			putParamIndexMapping(method);
		}
			
		private void putParamIndexMapping(Method method) {
			
			Annotation [] [] pa = method.getParameterAnnotations();
			for (int i = 0; i < pa.length; i++) {
				for (Annotation a : pa[i]) {
					//保存使用CustomRequestParam注解的参数
					if(a instanceof CustomRequestParam){
						String paramName = ((CustomRequestParam)a).value();
						//System.out.println("paramName ：" + paramName + " i : " +i );
						if(null != paramName && !"".equals(paramName.trim())){
							paramIndexMapping.put(paramName, i);
						}
					}
				}
				
			}
			
			//保存HttpServletRequest和HttpServletResponse 参数
			Class<?> [] paramsTypes = method.getParameterTypes();
			for (int i = 0; i < pa.length; i++) {
				Class<?> type = paramsTypes[i];
				if(type == HttpServletRequest.class || type == HttpServletResponse.class){
					paramIndexMapping.put(type.getName(), i);
				}
			}
		}
		
		
		
		
	}
}

```

源码下载地址：http://download.csdn.net/download/baidu_19473529/10268616