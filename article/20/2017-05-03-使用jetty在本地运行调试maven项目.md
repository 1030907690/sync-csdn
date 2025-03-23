---
layout:					post
title:					"使用jetty在本地运行调试maven项目"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
pom.xml

<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>
    <groupId>com.zzq.main</groupId>
    <artifactId>zzq-main</artifactId>
    <version>0.0.1.RELEASE</version>
    <packaging>war</packaging>
    <name>zzq-main</name>
 

    <properties>
		<httpclient.version>4.4</httpclient.version>
		<base-modules.version>0.0.1.RELEASE</base-modules.version>
		<spring.version>4.1.8.RELEASE</spring.version>
		<hibernate.version>4.3.11.Final</hibernate.version>
		<validation.version>1.1.0.Final</validation.version>
		<spring-data-jpa.version>1.8.2.RELEASE</spring-data-jpa.version>
		<spring-data-redis.version>1.6.0.RELEASE</spring-data-redis.version>
		<druid.version>1.0.16</druid.version>
		<mysql.version>5.1.18</mysql.version>
		<sitemesh.version>2.4.2</sitemesh.version>
		<freemarker.version>2.3.23</freemarker.version>
		<aspectj.version>1.8.7</aspectj.version>
		<quartz.version>2.2.1</quartz.version>
		<shiro.version>1.2.4</shiro.version>

		<servlet.version>3.1.0</servlet.version>
		<jsp.version>2.0</jsp.version>
		<jstl.version>1.2</jstl.version>

		<commons-lang3.version>3.4</commons-lang3.version>
		<commons-io.version>2.4</commons-io.version>
		<commons-collections.version>3.2.1</commons-collections.version>
		<commons-fileupload.version>1.3.1</commons-fileupload.version>
		<commons-codec.version>1.9</commons-codec.version>
		<commons-beanutils.version>1.9.2</commons-beanutils.version>
		<commons-httpclient.version>3.1</commons-httpclient.version>
		<guava.version>18.0</guava.version>
		<jackson.version>2.6.3</jackson.version>
		<joda-time.version>2.8.2</joda-time.version>
		<hibernate-validator.version>5.2.2.Final</hibernate-validator.version>
		<poi.version>3.13</poi.version>
		<kaptcha.version>0.0.9</kaptcha.version>

		<slf4j.version>1.7.12</slf4j.version>
		<logback.version>1.1.3</logback.version>
		<log4jdbc.version>1.2</log4jdbc.version>

		<junit.version>4.12</junit.version>
		<assertj.version>1.7.1</assertj.version>
		<mockito.version>1.10.19</mockito.version>
		<powermock.version>1.6.3</powermock.version>
		<jedis.version>2.7.3</jedis.version>
		<!-- Update. -->
		<jetty.version>7.6.18.v20150929</jetty.version>
		<tomcat.version>7.0.65</tomcat.version>
		<!-- <tomcat.version>8.0.30</tomcat.version> -->
		<h2.version>1.4.190</h2.version>

		<thumbnailator.version>0.4.7</thumbnailator.version>
		<gif4j.version>1.0</gif4j.version>
		<aliyun-openservices.version>1.2.3</aliyun-openservices.version>

		<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
		<java.version>1.7</java.version>
		<!-- lombok -->
	</properties>


    <dependencies>
        <!-- ###### Modules begin ###### -->
        
        <!-- fastjson start -->
			<dependency>
				<groupId>com.alibaba</groupId>
				<artifactId>fastjson</artifactId>
				<version>1.2.7</version>
			</dependency>
       <!-- fastjson end -->  
        
        <!-- commons start -->
        <!-- https://mvnrepository.com/artifact/commons-lang/commons-lang -->
		<dependency>
		    <groupId>commons-lang</groupId>
		    <artifactId>commons-lang</artifactId>
		    <version>2.6</version>
		</dependency>
        <!-- commons end -->
        <!-- mybatis start-->
			<dependency>
				<groupId>org.mybatis</groupId>
				<artifactId>mybatis</artifactId>
				<version>3.3.0</version>
			</dependency>
			<dependency>
				<groupId>org.mybatis</groupId>
				<artifactId>mybatis-spring</artifactId>
				<version>1.2.2</version>
			</dependency>
			<!-- mybatis generator -->
			<dependency>
				<groupId>org.mybatis.generator</groupId>
				<artifactId>mybatis-generator-core</artifactId>
				<version>1.3.2</version>
			</dependency>
			  <!-- mybatis end-->
        
        <!-- 数据库配置start -->
        	<!-- Druid. -->
			<dependency>
				<groupId>com.alibaba</groupId>
				<artifactId>druid</artifactId>
				<version>${druid.version}</version>
			</dependency>

			<!-- MySQL. -->
			<dependency>
				<groupId>mysql</groupId>
				<artifactId>mysql-connector-java</artifactId>
				<version>${mysql.version}</version>
				<scope>runtime</scope>
			</dependency>
			
			<!-- 数据库配置end -->
        	
        	<!-- pagehelper. Mybatis通用分页插件  start-->
			<dependency>
				<groupId>com.github.pagehelper</groupId>
				<artifactId>pagehelper</artifactId>
				<version>4.0.1</version>
			</dependency>
				<!-- pagehelper. Mybatis通用分页插件  end-->
		<!-- 使用jetty大概需要的包 start -->
			<!-- ###### GENERAL UTILS begin ###### -->
		<!-- Apache. -->
		<dependency>
			<groupId>org.apache.commons</groupId>
			<artifactId>commons-compress</artifactId>
			<version>1.4.1</version>
		</dependency>
		<dependency>
			<groupId>org.apache.commons</groupId>
			<artifactId>commons-lang3</artifactId>
			<version>${commons-lang3.version}</version>
		</dependency>
		<dependency>
			<groupId>commons-io</groupId>
			<artifactId>commons-io</artifactId>
			<version>${commons-io.version}</version>
		</dependency>
		<dependency>
			<groupId>commons-collections</groupId>
			<artifactId>commons-collections</artifactId>
			<version>${commons-io.version}</version>
		</dependency>
 
		<dependency>
			<groupId>commons-beanutils</groupId>
			<artifactId>commons-beanutils</artifactId>
			<version>${commons-beanutils.version}</version>
		</dependency>

		<!-- ###### Logging begin ###### -->
		<!-- log4j -->
		<dependency>
			<groupId>log4j</groupId>
			<artifactId>log4j</artifactId>
			<version>1.2.16</version>
		</dependency>
		<!-- Logback. -->
		<dependency>
			<groupId>ch.qos.logback</groupId>
			<artifactId>logback-core</artifactId>
			<version>${logback.version}</version>
		</dependency>
		<dependency>
			<groupId>ch.qos.logback</groupId>
			<artifactId>logback-classic</artifactId>
			<version>${logback.version}</version>
				<exclusions>
					<exclusion>
						<groupId>org.slf4j</groupId>
						<artifactId>slf4j-api</artifactId>
					</exclusion>
				</exclusions>
		</dependency>
		<dependency>
			<groupId>ch.qos.logback</groupId>
			<artifactId>logback-access</artifactId>
			<version>${logback.version}</version>
		</dependency>
		
		
			<!-- ###### Logging begin ###### -->
			<!-- Logback. -->
			<dependency>
				<groupId>ch.qos.logback</groupId>
				<artifactId>logback-core</artifactId>
				<version>${logback.version}</version>
			</dependency>
			<dependency>
				<groupId>ch.qos.logback</groupId>
				<artifactId>logback-classic</artifactId>
				<version>${logback.version}</version>
				<exclusions>
					<exclusion>
						<groupId>org.slf4j</groupId>
						<artifactId>slf4j-api</artifactId>
					</exclusion>
				</exclusions>
			</dependency>
			<dependency>
				<groupId>ch.qos.logback</groupId>
				<artifactId>logback-access</artifactId>
				<version>${logback.version}</version>
			</dependency>

			<!-- Slf4j. -->
			<dependency>
				<groupId>org.slf4j</groupId>
				<artifactId>slf4j-api</artifactId>
				<version>${slf4j.version}</version>
			</dependency>


			<!-- Slf4j-simple -->
			<dependency>
				<groupId>org.slf4j</groupId>
				<artifactId>slf4j-simple</artifactId>
				<version>${slf4j.version}</version>
			</dependency>


			<!-- log4j桥接到slf4j. -->
			<dependency>
				<groupId>org.slf4j</groupId>
				<artifactId>log4j-over-slf4j</artifactId>
				<version>${slf4j.version}</version>
			</dependency>


			<!-- commons-logging桥接到slf4j. -->
			<dependency>
				<groupId>org.slf4j</groupId>
				<artifactId>jcl-over-slf4j</artifactId>
				<version>${slf4j.version}</version>
			</dependency>


			<!-- java.util.logging桥接到slf4j. -->
			<dependency>
				<groupId>org.slf4j</groupId>
				<artifactId>jul-to-slf4j</artifactId>
				<version>${slf4j.version}</version>
			</dependency>


			<!-- log4jdbc. -->
			<dependency>
				<groupId>com.googlecode.log4jdbc</groupId>
				<artifactId>log4jdbc</artifactId>
				<version>${log4jdbc.version}</version>
				<scope>runtime</scope>
			</dependency>

			<!-- ###### Logging end ###### -->
	   <dependency>
			<groupId>commons-logging</groupId>
			<artifactId>commons-logging</artifactId>
			<version>1.2</version>
		</dependency>
		
		
 
		<dependency>
		    <groupId>dom4j</groupId>
		    <artifactId>dom4j</artifactId>
		    <version>1.6.1</version>
		</dependency>


		<dependency>
			<groupId>commons-collections</groupId>
			<artifactId>commons-collections</artifactId>
			<version>${commons-collections.version}</version>
		</dependency>

		<dependency>
			<groupId>org.apache.commons</groupId>
			<artifactId>commons-lang3</artifactId>
			<version>${commons-lang3.version}</version>
		</dependency>
		
		<dependency>
			<groupId>com.google.guava</groupId>
			<artifactId>guava</artifactId>
			<version>${guava.version}</version>
		</dependency>



        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>jstl</artifactId>
            <version>${jstl.version}</version>
        </dependency>

    

        <!-- ###### Modules end ###### -->
        <!-- Servlet. -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>${servlet.version}</version>
			<scope>provided</scope>
        </dependency>
        
        
          <!-- Jetty. -->
        <dependency>
            <groupId>org.eclipse.jetty.aggregate</groupId>
            <artifactId>jetty-webapp</artifactId>
            <version>${jetty.version}</version>
        </dependency>
        <dependency>
            <groupId>org.eclipse.jetty</groupId>
            <artifactId>jetty-jsp</artifactId>
            <version>${jetty.version}</version>
        </dependency>
        
		<!-- 使用jetty大概需要的包 end -->
		
		
        <!-- Spring web.start -->
	
		
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-web</artifactId>
            <version>${spring.version}</version>
        </dependency>
        
        <dependency>
				<groupId>org.springframework</groupId>
				<artifactId>spring-webmvc</artifactId>
				<version>${spring.version}</version>
		</dependency>
		<dependency>
				<groupId>org.springframework</groupId>
				<artifactId>spring-webmvc-portlet</artifactId>
				<version>${spring.version}</version>
		</dependency>
        
        
        <!-- Spring beans. -->
			<dependency>
				<groupId>org.springframework</groupId>
				<artifactId>spring-beans</artifactId>
				<version>${spring.version}</version>
			</dependency>
        <!-- Spring web.end -->
        
		<!-- 上传 start -->
		 <dependency>
				<groupId>commons-fileupload</groupId>
				<artifactId>commons-fileupload</artifactId>
				<version>${commons-fileupload.version}</version>
		</dependency>
        
      <!-- 上传 end -->
      
      
        
    </dependencies>
    
 <build>
    <finalName>zzq-main</finalName>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-war-plugin</artifactId>
        <configuration>
          <failOnMissingWebXml>false</failOnMissingWebXml>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>


jetty封装的util

JettyBootstrap.java

package  com.zzq.main.jetty;

import java.io.FileInputStream;
import java.io.InputStream;
import java.nio.charset.Charset;
import java.util.Iterator;

import org.dom4j.Document;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import org.eclipse.jetty.server.Server;

import com.zzq.main.spring.Profiles;

/**
 * Jetty启动类.
 *
 * @author zhouzhongqing
 * @date 2017年5月2日14:55:30
 */
public class JettyBootstrap {
	
	public static void start( int port, String profile ) throws Exception {
		String projectPath =System.getProperty("user.dir")+"/pom.xml";
		StringBuilder strBuffer = new StringBuilder();
		InputStream _input = new FileInputStream(projectPath);
		int buffer = 1024;
		byte[] bys = new byte[buffer];
		int byteReade = 0;
		while ((byteReade = _input.read(bys, 0, buffer)) != -1) {
			strBuffer.append(new String(bys, 0, byteReade, Charset
					.forName("UTF-8")));
		}
		_input.close();
		String xmlString = strBuffer.toString();
		Document doc = null;
		doc = DocumentHelper.parseText(xmlString);
		Element root = doc.getRootElement();
		Iterator artifactId = root.elementIterator("artifactId");
		Element entry = (Element) artifactId.next();
		String projectname = entry.getText();
		start(port,profile,"/"+projectname);
	}

	/**
	 * 启动.
	 */
	public static void start( int port, String profile , String contextPath ) throws Exception {
		long beginTime = System.currentTimeMillis();

		// 设定Spring的profile.
		Profiles.setProfileAsSystemProperty( profile );
		System.setProperty( "org.apache.jasper.compiler.disablejsr199", "true" );

		Server server = JettyFactory.createServerInSource( port, contextPath );

		try {
			server.start();

			long endTime = System.currentTimeMillis();

			System.err.println( "[INFO] 程序运行服务地址             http://localhost:" + port + contextPath);
			System.err.println( "[INFO] 程序运行耗时: " + ( endTime - beginTime ) + "ms" );
			System.err.println( "[HINT] 回车快速重新启动应用程序" );

			// 等待用户输入回车重载应用.
			while( true ) {
				char c = ( char ) System.in.read();
				if( c == '\n' ) {
					beginTime = System.currentTimeMillis();

					// 重启.
					JettyFactory.reloadContext( server );

					endTime = System.currentTimeMillis();

					System.err.println( "[INFO] 程序运行服务地址  /t http://localhost:" + port + contextPath );
					System.err.println( "[INFO] 程序运行耗时: " + ( endTime - beginTime ) + "ms" );
					System.err.println( "[HINT] 回车快速重新启动应用程序" );
				}
			}
		} catch( Exception e ) {
			e.printStackTrace();
			System.exit( -1 );
		}
	}

}
JettyFactory.java

package com.zzq.main.jetty;

import org.apache.commons.collections.MapUtils;
import org.eclipse.jetty.server.Connector;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.nio.SelectChannelConnector;
import org.eclipse.jetty.webapp.WebAppClassLoader;
import org.eclipse.jetty.webapp.WebAppContext;

import java.util.Map;

/**
 * 创建Jetty Server的工厂类.
 *
 * @author zhouzhongqing
 * @date 2017年5月3日11:31:49
 */
public class JettyFactory {

	private static final String DEFAULT_WEBAPP_PATH = "src/main/webapp";
	private static final String WINDOWS_WEBDEFAULT_PATH = "jetty/webdefault-windows.xml";

	/**
	 * 创建用于开发运行调试的Jetty Server, 以src/main/webapp为Web应用目录.
	 */
	public static Server createServerInSource( int port, String contextPath ) {

		return createServerInSource( port, contextPath, null );
	}

	/**
	 * 创建用于开发运行调试的Jetty Server, 以src/main/webapp为Web应用目录.
	 */
	public static Server createServerInSource( int port, String contextPath, Map<String, String> initParameter ) {
		Server server = new Server();
		// 设置在JVM退出时关闭Jetty的钩子.
		server.setStopAtShutdown( true );

		SelectChannelConnector connector = new SelectChannelConnector();
		connector.setPort( port );
		// 解决Windows下重复启动Jetty居然不报告端口冲突的问题.
		connector.setReuseAddress( false );
		server.setConnectors( new Connector[]{ connector } );

		WebAppContext webContext = new WebAppContext( DEFAULT_WEBAPP_PATH, contextPath );
		// 修改webdefault.xml, 解决Windows下Jetty Lock住静态文件的问题.
		webContext.setDefaultsDescriptor( WINDOWS_WEBDEFAULT_PATH );
		// Struts2 Annotation需要加改句, 否则不能映射Action.
		webContext.setClassLoader( Thread.currentThread().getContextClassLoader() );
		//webContext.setResourceBase("D:/dev/wxspace/tzyun/application/application-shop/src/main/webapp");
		// 设置启动参数.
		if( MapUtils.isNotEmpty( initParameter ) ) {
			for( Map.Entry<String, String> entry : initParameter.entrySet() ) {
				webContext.setInitParameter( entry.getKey(), entry.getValue() );
			}
		}

		server.setHandler( webContext );

		return server;
	}

//	/**
//	 * 设置除jstl-*.jar外其他含tld文件的jar包的名称. jar名称不需要版本号，如sitemesh, shiro-web.
//	 */
//	public static void setTldJarNames( Server server, String... jarNames ) {
//		WebAppContext context = ( WebAppContext ) server.getHandler();
//		List<String> jarNameExprssions = Lists.newArrayList( ".*/jstl-[^/]*\\.jar$", ".*/.*taglibs[^/]*\\.jar$" );
//		for( String jarName : jarNames ) {
//			jarNameExprssions.add( ".*/" + jarName + "-[^/]*\\.jar$" );
//		}
//
//		context.setAttribute( "org.eclipse.jetty.server.webapp.ContainerIncludeJarPattern",
//				StringUtils.join( jarNameExprssions, '|' ) );
//
//	}

	/**
	 * 快速重新启动application, 重载target/classes与target/test-classes.
	 */
	public static void reloadContext( Server server ) throws Exception {
		WebAppContext context = ( WebAppContext ) server.getHandler();

	//	System.out.println( "[INFO] Application reloading" );
		context.stop();

		WebAppClassLoader classLoader = new WebAppClassLoader( context );
		classLoader.addClassPath( "target/classes" );
		classLoader.addClassPath( "target/test-classes" );
		context.setClassLoader( classLoader );

		context.start();

	//	System.out.println( "[INFO] Application reloaded" );
	}

}

Profiles.java

package com.zzq.main.spring;

/**
 * Spring profile常用方法与profile名称.
 *
 * @author zhouzhongqing
 * @date 2017年5月2日14:55:56
 */
public class Profiles {

	public static final String ACTIVE_PROFILE = "spring.profiles.active";
	public static final String DEFAULT_PROFILE = "spring.profiles.default";

	public static final String LOCAL = "local";
	public static final String PRODUCTION = "production";
	public static final String DEVELOPMENT = "development";
	public static final String TEST = "test";

	public static final String UNIT_TEST = "test";
	public static final String FUNCTIONAL_TEST = "functional";

	/**
	 * 在Spring启动前, 设置profile的环境变量.
	 */
	public static void setProfileAsSystemProperty( String profile ) {
		System.setProperty( ACTIVE_PROFILE, profile );
	}

}

web.xml配置

<?xml version="1.0" encoding="UTF-8"?>
 <web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://java.sun.com/xml/ns/javaee"
	xmlns:web="http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd" 
	xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd"
	version="3.0">
  <display-name>Archetype Created Web Application</display-name>
  
   <welcome-file-list>
    <welcome-file>index.html</welcome-file>
    <welcome-file>index.htm</welcome-file>
    <welcome-file>index.jsp</welcome-file>
    <welcome-file>default.html</welcome-file>
    <welcome-file>default.htm</welcome-file>
    <welcome-file>default.jsp</welcome-file>
  </welcome-file-list>
  
  <!-- log4j的配置相关  start-->  
    <context-param>  
        <param-name>log4jConfigLocation</param-name>  
        <param-value>classpath:config/log4j/log4j.properties</param-value>  
    </context-param>
    <context-param> 
    	<param-name>webAppRootKey</param-name>
    	<param-value>webApp.root</param-value>
    </context-param>
    <context-param>  
        <param-name>log4jRefreshInterval</param-name>  
        <param-value>6000000</param-value>  
    </context-param> 
    <listener>  
        <listener-class>  
            org.springframework.web.util.Log4jConfigListener
        </listener-class>  
    </listener>
    
      <!-- log4j的配置相关  end-->  
      
      
      <context-param>
	    <param-name>contextConfigLocation</param-name>
	    <param-value>classpath*:config/spring/ApplicationContext.xml</param-value>
	  </context-param>
	  
 	  <listener>
	    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
	  </listener> 
	  
	  
	  
	 <servlet>
	    <servlet-name>springMVC</servlet-name>
	    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
	    <init-param>
	      <param-name>contextConfigLocation</param-name>
	      <param-value>classpath*:config/spring/ApplicationContext-MVC.xml</param-value>
	    </init-param>
	    <load-on-startup>1</load-on-startup>
	  </servlet>
	  
	  
	  
	  
	  
	  
	  <servlet-mapping>
	    <servlet-name>springMVC</servlet-name>
	    <url-pattern>*.tz</url-pattern>
	  </servlet-mapping>
	  
	  
	  	<!-- 设置session超时时间，1小时 -->
	<session-config>
		<session-timeout>60</session-timeout>
	</session-config>

	<error-page>
		<exception-type>java.lang.Throwable</exception-type>
		<location>/WEB-INF/views/error/500.jsp</location>
	</error-page>
	<error-page>
		<error-code>500</error-code>
		<location>/WEB-INF/views/error/500.jsp</location>
	</error-page>
	<error-page>
		<error-code>404</error-code>
		<location>/WEB-INF/views/error/404.jsp</location>
	</error-page>
	  
	<listener> 
	<listener-class>org.springframework.web.util.IntrospectorCleanupListener</listener-class> 
	</listener>
</web-app>

启动项目StartServer.java

package com.zit.main;

import com.zzq.main.jetty.JettyBootstrap;
import com.zzq.main.spring.Profiles;

/**
 * @author zhouzhongqing
 * 2017-5-2 15:00:45
 */
public class StartServer {

		public static void main( String[] args ) throws Exception {
			JettyBootstrap.start( 6113, Profiles.LOCAL );

	}
}
目录结构图



附上源代码

http://download.csdn.net/detail/baidu_19473529/9831996

​