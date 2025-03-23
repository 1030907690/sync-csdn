---
layout:					post
title:					"shiro异常local class incompatible: stream classdesc serialVersionUID = -3119462103770576445"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
###shiro ehcache报错
```

HTTP Status 500 – Internal Server Error

Type Exception Report

Message Filtered request failed.

Description The server encountered an unexpected condition that prevented it from fulfilling the request.

Exception

javax.servlet.ServletException: Filtered request failed.
	org.apache.shiro.web.servlet.AbstractShiroFilter.doFilterInternal(AbstractShiroFilter.java:384)
	org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)
	org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:357)
	org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:270)
	org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:200)
	org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107)
Root Cause

org.apache.shiro.cache.CacheException: net.sf.ehcache.CacheException: java.io.InvalidClassException: com.xxx.article.entity.TbUser; local class incompatible: stream classdesc serialVersionUID = -3119462103770576445, local class serialVersionUID = -584213288927121417
	org.apache.shiro.cache.ehcache.EhCache.get(EhCache.java:84)
	org.apache.shiro.session.mgt.eis.CachingSessionDAO.getCachedSession(CachingSessionDAO.java:217)
	org.apache.shiro.session.mgt.eis.CachingSessionDAO.getCachedSession(CachingSessionDAO.java:202)
	org.apache.shiro.session.mgt.eis.CachingSessionDAO.readSession(CachingSessionDAO.java:259)
	org.apache.shiro.session.mgt.DefaultSessionManager.retrieveSessionFromDataSource(DefaultSessionManager.java:236)
	org.apache.shiro.session.mgt.DefaultSessionManager.retrieveSession(DefaultSessionManager.java:222)
	org.apache.shiro.session.mgt.AbstractValidatingSessionManager.doGetSession(AbstractValidatingSessionManager.java:118)
	org.apache.shiro.session.mgt.AbstractNativeSessionManager.lookupSession(AbstractNativeSessionManager.java:148)
	org.apache.shiro.session.mgt.AbstractNativeSessionManager.getSession(AbstractNativeSessionManager.java:140)
	org.apache.shiro.mgt.SessionsSecurityManager.getSession(SessionsSecurityManager.java:156)
	org.apache.shiro.mgt.DefaultSecurityManager.resolveContextSession(DefaultSecurityManager.java:460)
	org.apache.shiro.mgt.DefaultSecurityManager.resolveSession(DefaultSecurityManager.java:446)
	org.apache.shiro.mgt.DefaultSecurityManager.createSubject(DefaultSecurityManager.java:342)
	org.apache.shiro.subject.Subject$Builder.buildSubject(Subject.java:845)
	org.apache.shiro.web.subject.WebSubject$Builder.buildWebSubject(WebSubject.java:148)
	org.apache.shiro.web.servlet.AbstractShiroFilter.createSubject(AbstractShiroFilter.java:292)
	org.apache.shiro.web.servlet.AbstractShiroFilter.doFilterInternal(AbstractShiroFilter.java:359)
	org.apache.shiro.web.servlet.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:125)
	org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:357)
	org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:270)
	org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:200)
	org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) 
```
- 原因serialVersionUID不一致
###解决办法
 - 找到ehcache的配置,缓存的位置

```
<diskStore path="java.io.tmpdir/fake-manager" />
```
- 删除缓存，重启再生成一次就好了，我这里的配置是tomcat的temp目录