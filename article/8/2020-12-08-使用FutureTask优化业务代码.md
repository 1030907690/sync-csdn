---
layout:					post
title:					"使用FutureTask优化业务代码"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 简介
- `FutureTask`：**一个可取消的异步计算**。
- `FutureTask`提供了对Future的基本实现，可以使用`FutureTask`异步执行任务，调用其`get`方法获取返回结果。
## 本章目标
- 演示一般情况下分页查询用户的代码。
- 使用`FutureTask`优化分页查询用户的代码，提高效率。
## 分页查询用户案例
### 创建UserService类
- 通常分页查询数据，会分成以下2部分。
	- （1）查询数据总条数。
	- （2）分页查询数据，sql使用offset，limit参数。
- 下面分成2个方法（总条数、分页数据），为了模拟查询数据的效果，固定要耗时2毫秒。代码如下所示。
```java
    /***
     * 查询用户条数
     * */
    private int userCount() {
        try {
            //模拟这里查询数据库耗时2毫秒
            Thread.sleep(2L);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return 10;
    }
    /***
     * 根据页数查询用户具体数据
     * @param currentPage 页数
     * */
    private List userData(int currentPage) {
        try {
            //模拟这里查询数据库耗时2毫秒
            Thread.sleep(2L);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return new ArrayList<>();
    }
```
- 调用这2个方法，计算查询耗时，代码如下所示。

```java
    public Object findUserPageList() {
        long startTime = System.currentTimeMillis();
        //1、查询用户条数
        int userCount = userCount();
        System.out.println(userCount);
        //2、分页查询用户数据
        List list = userData(1);
        System.out.println(list);
        long endTime = System.currentTimeMillis();
        // 相差时间，耗时
        long diffTime = endTime - startTime;
        System.out.println("总共耗时：" + diffTime);
        return null;
    }
```
### 创建UserController类
- 声明controller层调用service层方法，代码如下所示。

```java
@RestController
public class UserController {
    @Resource
    private UserService userService;
    @RequestMapping("/findUserPageList")
    public Object findUserPageList(){
        return userService.findUserPageList();
    }
}
```
### 查询效果
- 调用/findUserPageList接口3次效果如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3e2846d0d18b4c9b206ed4bf47f46c6a.png)
## 使用FutureTask优化业务代码
- 从上图可以看出，最长的竟然长达6毫秒，那么如何优化呢？
- 答案就是`异步`，但是普通的线程是不行的，因为不能接收到返回值。
- JUC包里就提供了`FutureTask`，供开发者使用。
- 下面开启`FutureTask`之旅，只需要改动`UserService#findUserPageList`方法就可以了。
### 修改UserService代码
- 创建`FutureTask`对象，构造器中传入`Callable`对象，使用`子线程执行`，最后调用`get`方法阻塞得到返回值。代码如下所示。
```java
  public Object findUserPageList() {
        long startTime = System.currentTimeMillis();
        //1、查询用户条数
        // userCount();
        Callable userCountFutureCallable = new Callable() {
            @Override
            public Integer call() throws Exception {
                return userCount();
            }
        };
        FutureTask<Integer> userCountFuture = new FutureTask(userCountFutureCallable);
        //2、分页查询用户数据
        // userData(1);
        Callable userDataFutureCallable = new Callable() {
            @Override
            public List call() throws Exception {
                return userData(1);
            }
        };
        FutureTask<List> userDataFuture = new FutureTask(userDataFutureCallable);
        // 使用子线程执行
        new Thread(userCountFuture).start();
        new Thread(userDataFuture).start();

        Integer userCount = 0;
        try {
            userCount = userCountFuture.get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        System.out.println(userCount);
        List list = null;
        try {
            list = userDataFuture.get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        System.out.println(list);
        long endTime = System.currentTimeMillis();
        // 相差时间，耗时
        long diffTime = endTime - startTime;
        System.out.println("总共耗时：" + diffTime+"毫秒");
        return null;
    }
```
### 修改后的效果
- 依旧是调用/findUserPageList接口3次，结果如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/459a80498faa49a4a7e4808cef59969f.png)
- 从上图可以看出，效率大大提升了。
### 将FutureTask交给线程池执行
- 其实还有待优化的地方，例如现在是每调用一次就创建子线程。我们都知道，`不可能无限创建子线程的，并且线程的创建和销毁也有很大的损耗`。这个时候可以使用线程池，代码如下所示。

```java
    // CPU核数
    private final int processors = Runtime.getRuntime().availableProcessors();
    private final ExecutorService executorService = new ThreadPoolExecutor(processors * 2, processors * 10, 60L, TimeUnit.SECONDS, new ArrayBlockingQueue(processors * 100), Executors.defaultThreadFactory(), new ThreadPoolExecutor.CallerRunsPolicy());
   public Object findUserPageList() {
    	...省略...
        executorService.execute(userCountFuture);
        executorService.execute(userDataFuture);

      	...省略...
        return null;
    }

```
- 本例代码下载地址：[https://github.com/1030907690/futureTaskSample](https://github.com/1030907690/futureTaskSample)

