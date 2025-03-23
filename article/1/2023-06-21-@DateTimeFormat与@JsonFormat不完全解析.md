---
layout:					post
title:					"@DateTimeFormat与@JsonFormat不完全解析"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)

## 前言
- 一直以来对`@DateTimeFormat`与`@JsonFormat` 比较模糊，容易搞忘，今天就做个笔记，由于不涉及原理，源码所以是不完全解析，有时间再看下源码。
- 如果时间急的，可以不看验证过程，直接看`结论`。

## 测试代码
- 下面是基本代码：
- 实体类

```java
public class User {

    public final static String YYYY_MM_DD_HH_MM_SS = "yyyy-MM-dd HH:mm:ss";

    private String name;

    private Date birthday;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Date getBirthday() {
        return birthday;
    }

    public void setBirthday(Date birthday) {
        this.birthday = birthday;
    }
}

```

- controller

```java
@RestController
public class TestController {

    @RequestMapping("/test")
    public User test(User user){
        return user;
    }
}

```


## @DateTimeFormat
### 不加任何注解的情况


- 我使用postman传递`birthday`参数不成功。


![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6dee4574c373db04d27a3898bcee27bd.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/64a3366edfaad5e390ee42827240e91d.png)
- 取消`birthday`正常。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/520cd8c9b4d2843f21b7b49f53332c38.png)

### 普通请求
- 那我们加上`@DateTimeFormat`看看。

```java
   @DateTimeFormat(pattern = YYYY_MM_DD_HH_MM_SS)
    private Date birthday;
```
- 加入之后`GET/POST都成功`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/66e42b445ba60162c86a964472518dce.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/459d19af75d06ca38434993c104b5dc1.png)

### JSON请求

- 再来测试请求参数是json的情况。

```java
   @RequestMapping("/test")
    public User test(@RequestBody User user){
        return user;
    }
```

- 先单独尝试name参数，以免干扰。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1377ccf09732c67c3e1315c077abda21.png)
- name参数成功，再加上birthday参数,有异常，传JSON不行。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2e4833d9a85e0965ec922487ec1b1214.png)



## @JsonFormat
### 普通请求
- 代码

```java
 @JsonFormat(pattern = YYYY_MM_DD_HH_MM_SS)
    private Date birthday;
```
- 普通请求报错

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cf3b172b3e0421c60478e6ea6390b216.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/066120e9588c79348c9ae9aa551ce3b7.png)


### JSON请求
- 改下controller
```java
   @RequestMapping("/test")
    public User test(@RequestBody User user){
        return user;
    }
```

- 测试结果正常
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/649af56595ae08672a7ba2776e5a353a.png)
- 注意：`Spring框架默认序列化框架用Jackson，所以你没改序列化框架的话，加了@JsonFormat还具备格式化返回值的能力`。

## 其他方式（@InitBinder）
- 新增一个`BaseController`，TestController 继承`BaseController`

```java
public class BaseController {

    /**
     * 将前台传递过来的日期格式的字符串，自动转化为Date类型
     */
    @InitBinder
    public void initBinder(WebDataBinder binder)
    {
        // Date 类型转换
        binder.registerCustomEditor(Date.class, new PropertyEditorSupport()
        {
            @Override
            public void setAsText(String text)
            {
                setValue(DateUtils.parseDate(text));
            }
        });


    }

}



@RestController
public class TestController extends BaseController {

    @RequestMapping("/test")
    public User test(User user){
        return user;
    }
}

```

- 这样它也能获得普通请求接收时间的能力。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9c21ece6e01a864d7fc6d87d384146cf.png)
- 不过JSON请求报错。
- ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e1e4d968eaf4ad2d0ae21d5ece61c082.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/defc934a0137712a458149f70888ce43.png)


## 结论
- `@DateTimeFormat`适用于普通请求方式，JSON请求方式报错。
- `@JsonFormat `适用于JSON请求方式，普通请求报错。
>- 注意：`Spring框架默认序列化框架用Jackson，所以你没改序列化框架的话，加了@JsonFormat还具备格式化返回值的能力`。
- `@InitBinder`这种方式需要自己写点代码，效果与 `@DateTimeFormat`雷同，适用于普通请求方式，JSON请求方式报错。
## 源码地址
- [https://github.com/1030907690/spring-boot-kubernetes/tree/v1.0.3](https://github.com/1030907690/spring-boot-kubernetes/tree/v1.0.3)  @DateTimeFormat与@JsonFormat 测试