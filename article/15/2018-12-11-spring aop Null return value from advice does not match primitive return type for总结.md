---
layout:					post
title:					"spring aop Null return value from advice does not match primitive return type for总结"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- Null return value from advice does not match primitive return type for这个一般都是发生在代码做了环绕后。
- 找到源码抛出这个异常的位置（我是全局搜索的我使用的cglib动态代理的代码）CglibAopProxy#processReturnType:

```
 private static Object processReturnType(Object proxy, Object target, Method method, Object retVal) {
		// Massage return value if necessary
		if (retVal != null && retVal == target && !RawTargetAccess.class.isAssignableFrom(method.getDeclaringClass())) {
			// Special case: it returned "this". Note that we can't help
			// if the target sets a reference to itself in another returned object.
			retVal = proxy;
		}
		Class<?> returnType = method.getReturnType();
		//isPrimitive 此方法主要用来判断Class是否为原始类型（boolean、char、byte、short、int、long、float、double）。   returnType != Void.TYPE  是否是无返回值类型
		if (retVal == null && returnType != Void.TYPE && returnType.isPrimitive()) {
			throw new AopInvocationException(
					"Null return value from advice does not match primitive return type for: " + method);
		}
		return retVal;
	}

```

- 出现异常情况的第一种情况:
比如我的环绕代码是这样的:

```
//环绕service里的方法
  @Around("execution(* com.zzq.core.test.service..*.*(..))")
    public void around(ProceedingJoinPoint pjp ){
        System.out.println("AOP Aronud before...");
       Object result = null;
         try {
            result = pjp.proceed();
            System.out.println("result : "+ result);
        } catch (Throwable e) {
            e.printStackTrace();
        }
        System.out.println("AOP Aronud after...");
        }
```
service是这样的:

```
	@Override
	       public int select(int id) {
	            System.out.println("Enter DaoImpl.select() " + id);
	            return 1;
	  	   }
```
此时抛出异常:

```
Exception in thread "main" org.springframework.aop.AopInvocationException: Null return value from advice does not match primitive return type for: public int com.zzq.core.test.service.impl.TestAopServiceImpl.select(int)
	at org.springframework.aop.framework.CglibAopProxy.processReturnType(CglibAopProxy.java:351)
	at org.springframework.aop.framework.CglibAopProxy.access$0(CglibAopProxy.java:341)
	at org.springframework.aop.framework.CglibAopProxy$DynamicAdvisedInterceptor.intercept(CglibAopProxy.java:636)
	at com.zzq.core.test.service.impl.TestAopServiceImpl$$EnhancerBySpringCGLIB$$1f185468.select(<generated>)
	at com.zzq.core.test.BootStrap.main(BootStrap.java:18)
```
因为`环绕没有返回值为null`，`select方法返回类型不是void` ，`而是int`,刚好满足条件,抛出此异常。`int是无法匹配null的`（`除非是包装类型Integer,不过接到的一直是null`）。
还是需要改环绕,加上返回值就不报错了:

```
  @Around("execution(* com.zzq.core.test.service..*.*(..))")
    public Object around(ProceedingJoinPoint pjp ){
        System.out.println("AOP Aronud before...");
       Object result = null;
         try {
            result = pjp.proceed();
            System.out.println("result : "+ result);
        } catch (Throwable e) {
            e.printStackTrace();
        }
        System.out.println("AOP Aronud after...");
        return result;
        }
```

- 报错情况二、
结合上面的加上返回值还是报错,那么应该是代理的方法报错了,比如上面的select方法报错了也会报` Null return value from advice does not match primitive return type for`
比如这样的:
```
@Override
	       public int select(int id) {
	  			int a = 1 / 0;
	            System.out.println("Enter DaoImpl.select() " + id);
	            return 1;
	  	   }
```
代理的方法select方法肯定报错,执行被代理方法try catch了,`报错后没接收到代理方法的返回值也属正常,返回null,抛出异常`。


目前我对aop了解的还不是很透彻,如果文章有误的地方，还请指出,感激不尽。