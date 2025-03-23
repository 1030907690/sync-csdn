---
layout:					post
title:					"springMVC重定向后中文乱码"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 使用springMVC的redirect然后后面拼接参数重定向到别人的服务里面，昵称传过去的时候发现都是问号?(有几个中文就几个问号)。发现这种情况后在本地测试了下，然后抓包查看到如下图(用百度测了下):
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/2968d0226858cb29c27a988e3a266e06.png)
结果就是url加了中文就会有那个问号。
- 解决方案：
	>-  第一种：
   

```
 @RequestMapping("/getAccessToken")
    public String getAccessToken(HttpServletRequest request,RedirectAttributes attr){
    //参数 这种它自动把参数给你拼了你的url
     attr.addAttribute("name",nickName);
return "redirect:http://xxxxx";
}
```
> - 第二种
	  

```
@RequestMapping("/getAccessToken")
public String getAccessToken(HttpServletRequest request,RedirectAttributes attr){
    //参数 这种页面取值直接用el表达式就能获得到，这里的原理是放到session中，session在跳到页面后马上移除对象。所以你刷新一下后这个值就会丢掉。
     attr.addFlashAttribute("name",nickName);
return "redirect:http://xxxxx";
}
```