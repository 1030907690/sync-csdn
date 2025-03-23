---
layout:					post
title:					"Transaction rolled back because it has been marked as rollback-only"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 业务要求即使内层代码有报错，也要执行外层代码，保存数据，代码案例如下所示。


```java
// TestServiceImpl：
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void testInsert() {
        Users entity = new Users();
        entity.setName("张三啊");
        usersMapper.insert(entity);
        System.out.println(entity.getId());
        try {
            testExceptionService.test();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
```

```java
//TestExceptionServiceImpl
 @Override
    @Transactional(rollbackFor = Exception.class)
    public void test() {
        Users entity = new Users();
        entity.setName("李四啊");
        usersMapper.insert(entity);
        System.out.println(entity.getId());
        if (true){
            throw new RuntimeException("测试事务回滚");
        }
    }
```
- 按照我们主观认知，`try catch`捕获异常后，事务不会回滚。
- 我们来执行一下。
- 此时`testExceptionService.test()`报错，就会抛出`Transaction rolled back because it has been marked as rollback-only`，外层的代码也会回滚。如下图所示。

 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cea37d669e082c9c97650aeb02fc1171.png#pic_center)

- 同样的数据全回滚了，张三啊，李四啊都不会保存，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7d1c3d69fc129951584c6736c18284cb.png)
## 问题分析
- 首先`@Transactional`的属性`propagation`是默认的`Propagation.REQUIRED`。
- 此时外层有事务，那么`testExceptionService.test()`是不会新开事务的。
- 也就是说用的是`同一个事务`，肯定有一些事务状态（变量）是共用的，那么`testExceptionService.test()`报错，要回滚，那么就都要回滚。`捕获`是无效的。
## 解决方案
- 问题的关键点就是`同一个事务`。开启另一个事务就可以了，像本例的背景就可以这样操作。使用 `Propagation.REQUIRES_NEW`。如下代码所示。

```java
   @Override
    @Transactional(rollbackFor = Exception.class,propagation = Propagation.REQUIRES_NEW)
    public void test() {
        Users entity = new Users();
        entity.setName("李四啊");
        usersMapper.insert(entity);
        System.out.println(entity.getId());
        if (true){
            throw new RuntimeException("测试事务回滚");
        }
    }
```
- 也可以在controller层调用2个方法，分层2个事务执行。
- 注意：2个事务中，一个事务对数据修改，另一个事务内不可见。如果有依赖另一个事务的数据要处理下。
- 再次测试，外层代码操作保存了。结果如下所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/71c639ed0e9720e83bddd7326d315674.png)

## 案例代码
- 代码地址：[https://gitee.com/apple_1030907690/spring-boot-kubernetes/tree/v1.0.2](https://gitee.com/apple_1030907690/spring-boot-kubernetes/tree/v1.0.2)