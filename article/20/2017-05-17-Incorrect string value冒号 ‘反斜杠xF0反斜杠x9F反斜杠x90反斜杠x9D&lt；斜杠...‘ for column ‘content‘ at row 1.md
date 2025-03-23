---
layout:					post
title:					"Incorrect string value: ‘\xF0\x9F\x90\x9D&lt；/...‘ for column ‘content‘ at row 1"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
报错信息

Incorrect string value: '\xF0\x9F\x90\x9D</...' for column 'content' at row 1
	at org.springframework.jdbc.support.AbstractFallbackSQLExceptionTranslator.translate(AbstractFallbackSQLExceptionTranslator.java:83)
	at org.springframework.orm.hibernate3.HibernateTransactionManager.convertJdbcAccessException(HibernateTransactionManager.java:801)
	at org.springframework.orm.hibernate3.HibernateTransactionManager.convertHibernateAccessException(HibernateTransactionManager.java:787)
	at org.springframework.orm.hibernate3.HibernateTransactionManager.doCommit(HibernateTransactionManager.java:663)
	at org.springframework.transaction.support.AbstractPlatformTransactionManager.processCommit(AbstractPlatformTransactionManager.java:732)
	at org.springframework.transaction.support.AbstractPlatformTransactionManager.commit(AbstractPlatformTransactionManager.java:701)
	at org.springframework.transaction.interceptor.TransactionAspectSupport.commitTransactionAfterReturning(TransactionAspectSupport.java:321)
	at org.springframework.transaction.interceptor.TransactionInterceptor.invoke(TransactionInterceptor.java:116)
	at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:171)
	at org.springframework.aop.framework.JdkDynamicAopProxy.invoke(JdkDynamicAopProxy.java:204)

报错是因为utf8不能容纳超过3个字节的emoji表情，需要使用utf8mb4字符集

解决办法：

第一步、在每个保存的前面执行一次

SET NAMES utf8mb4
这条语句



第二步、把相应的保存文本的字段的字符集和排序规则改成utf8mb4、utf8mb4_unicode_ci



这样就能保存4个字符集的emoji表情了。

​