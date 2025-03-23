---
layout:					post
title:					"从spring、spring boot中找到解析properties、xml、yml、yaml文件的方法"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录) 
#### 一、解析properties和xml
- 这里使用了`FileSystemResource`，spring的`Resource`继承于`InputStreamSource`，也就是spring封装了`InputStreamSource`；可以从spring源码看到除了`FileSystemResource`还有其他的实现，比如可以不用绝对路径用`ClassPath`，对应的实现类就是`ClassPathResource`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9a258bd41a8c787eec400e6c288f3cd5.png)
```java
/***
	 * 解析Properties 、xml
	 * */
	public static void loadProperties(){

		// 第一种
		Properties props = new Properties();
		//查找配置文件的属性 并且都合并到props
		FileSystemResource location = new FileSystemResource(new File("F:\\work\\unknown\\unknown-admin\\config\\application.properties"));
		try {
			PropertiesLoaderUtils.fillProperties(props, new EncodedResource(location, (String) null));
			System.out.println(props.getProperty("zookeeper.address"));
		} catch (IOException e) {
			e.printStackTrace();
		}

		//第二种 spring boot的
		try {
			List<PropertySource<?>>  propertySourceList = new PropertiesPropertySourceLoader().load("app",new FileSystemResource("F:\\work\\unknown\\unknown-admin\\config\\application.properties"));
			System.out.println(propertySourceList.get(0).getProperty("zookeeper.address"));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
```

#### 二、解析yml和yaml
- 这里我就使用的`ClassPathResource`实现，根据自己实际情况选择用哪个具体实现。
```java
	/***
	 * 目前从源码中找到的读取yml、yaml文件的两种方式
	 * */
	public static void loadYml(){
		// 第一种  spring boot解析yml
		YamlPropertiesFactoryBean yaml = new YamlPropertiesFactoryBean();
		//yaml.setResources(new FileSystemResource("config.yml"));//File引入
		yaml.setResources(new ClassPathResource("/application-dev.yml"));//classPath引入
		System.out.println(yaml.getObject().get("spring.data.mongodb.uri"));



		//第二种  YamlPropertySourceLoader
		Resource resource = new ClassPathResource("/application-dev.yml");
		//List<Map<String, Object>> loaded = new OriginTrackedYamlLoader(resource).load();
		try {
			List<PropertySource<?>>  propertySourceList = new YamlPropertySourceLoader().load("/application.yml",resource);
			System.out.println(propertySourceList.get(0).getProperty("spring.data.mongodb.uri"));
		} catch (IOException e) {
			e.printStackTrace();
		}

	}
```
#### 三、总结和运行效果
- 用spring源码里解析配置文件的方法还是挺方便的，一、两行代码就搞定了,也不用去关流之类的，spring里面已经做了。
- 下面看下总体运行效果
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ad7287821840082e4841cf42bad23c92.png)
- 本篇到此结束，我再捋一捋后续有时间会出解析配置文件的源码分析，感谢您的观看，如果文章有问题，希望您能指正。
- [spring读取配置文件原理解析](https://blog.csdn.net/baidu_19473529/article/details/106850436)已经写了，欢迎大家观看和提意见- 2020年6月22日11:08:11
