---
layout:					post
title:					"spring mvc处理json文件静态资源文件报错Request method 'POST' not supported"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
使用spring mvc框架在页面直接请求json静态文件时报错：

```
Request method 'POST' not supported
```
目录结构是这样的：
![这里写图片描述](https://img-blog.csdn.net/20171031213813073?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
然后我想应该是被拦截了，所以我在 spring配置文件中加入：

```
<mvc:resources mapping="/json/**" location="/json/" />  
```
但是加入了忽略拦截后依然没有解决掉问题，他被当成了一个controller请求
于是换了一种写法：

```
 <bean class="org.springframework.web.servlet.handler.SimpleUrlHandlerMapping">
        <property name="urlMap">
            <map>
                <entry key="/json/**" value="myResourceHandler" />
            </map>
        </property>
        <property name="order" value="100000" />
    </bean>


    <bean id="myResourceHandler" name="myResourceHandler"
          class="org.springframework.web.servlet.resource.ResourceHttpRequestHandler">
        <property name="locations" value="/json/" />
        <property name="supportedMethods">
            <list>
                <value>GET</value>
                <value>HEAD</value>
                <value>POST</value>
            </list>
        </property>

    </bean>
```
这样终于解决了问题。
![这里写图片描述](https://img-blog.csdn.net/20171031214207701?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)