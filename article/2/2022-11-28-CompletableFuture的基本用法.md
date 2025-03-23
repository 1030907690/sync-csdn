---
layout:					post
title:					"CompletableFuture的基本用法"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言 
-  `CompletableFuture`是Java8新增的一个功能十分强大的工具类，它一方面实现了`Future`接口，另一方面也实现了`CompletionStage`接口，`CompletionStage`接口多达40中方法，为我们函数式编程
流式调用提供支持。相较于`FutureTask`来做多任务更简洁了。

## 使用
### 完成了就通知我

- 核心代码

```java

    /**
     * 完成了就通知我 ，手动
     *
     * @return
     */
    public String completeNotify() {
        CompletableFuture<Integer> future = new CompletableFuture<>();
        threadPoolTaskExecutor.execute(new AskThread(future));
        try {
            Integer result = future.get();
            System.out.println("result " + result);
            return result.toString();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } catch (ExecutionException e) {
            throw new RuntimeException(e);
        }
    }

    class AskThread implements Runnable {
        CompletableFuture<Integer> future;

        public AskThread(CompletableFuture<Integer> future) {
            this.future = future;
        }

        @Override
        public void run() {
            int res = 0;
            try {
                // 模拟长时间计算过程
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }

            res = 100;
            // 通知完成
            future.complete(res);

        }
    }

```
-  之前我利用这个功能完成了 [高并发场景下请求合并(批量)
](https://blog.csdn.net/baidu_19473529/article/details/124092081)的功能，可以参考下。

### 异步执行任务
- 核心代码

```java
     public String asyncTask() {
        StopWatch stopWatch = new StopWatch("asyncTask");
        stopWatch.start("task");
        // 如果是runAsync 没有返回值
        CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> calc(50), threadPoolTaskExecutor);

        CompletableFuture<Integer> futureTwo = CompletableFuture.supplyAsync(() -> calc(60), threadPoolTaskExecutor);
        int result = 0;
        int res = 0;
        try {
            result = future.get();
            res = futureTwo.get();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } catch (ExecutionException e) {
            throw new RuntimeException(e);
        }


        System.out.println(result + " " + res);
        stopWatch.stop();
        System.out.println(stopWatch.prettyPrint());
        System.out.println(stopWatch.getLastTaskTimeMillis());

        return result + " " + res;
    }
       public int calc(int param) {


        try {
            // 模拟耗时
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }

        if (EXCEPTION_PARAM == param){
            throw new RuntimeException("传了异常参数 "+param);
        }
        return param * 2;
    }

```
### 流式调用

```java
    public String stream() {

        CompletableFuture<Void> future = CompletableFuture.supplyAsync(() -> calc(50), threadPoolTaskExecutor).
                thenApply((i) -> Integer.toString(i)).
                thenApply((str) -> "res " + str).
                thenAccept(System.out::println);
        try {
            future.get();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } catch (ExecutionException e) {
            throw new RuntimeException(e);
        }
        return "done";
    }
```
### 异常处理

```java
     public String exception() {

        CompletableFuture<Void> future = CompletableFuture.supplyAsync(() -> calc(10))
                .exceptionally(ex -> {
                    System.out.println("异常信息 " + ex.toString());
                    return 0;
                })
                .thenApply((i) -> Integer.toString(i)).
                thenApply((str) -> "res " + str).
                thenAccept(System.out::println);
        try {
            future.get();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } catch (ExecutionException e) {
            throw new RuntimeException(e);
        }


        return "done";
    }
```

### 组合多个CompletableFuture

```java
   public String compose(){

        CompletableFuture future = CompletableFuture.supplyAsync(()->calc(50),threadPoolTaskExecutor)
                .thenCompose((i)->CompletableFuture.supplyAsync(()->calc(i),threadPoolTaskExecutor))
                .thenApply((str)->"res " + str)
                .thenAccept(System.out::println);
        try {
            future.get();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } catch (ExecutionException e) {
            throw new RuntimeException(e);
        }
        return "done";
    }
```


## 小结
- `CompletableFuture`很强大，如果写异步任务相比`FutureTask`更简洁。
- 源码地址：[https://github.com/1030907690/CompletableFuture-Sample](https://github.com/1030907690/CompletableFuture-Sample)
- 视频地址：[https://www.bilibili.com/video/BV1B24y1C7bT/](https://www.bilibili.com/video/BV1B24y1C7bT/)