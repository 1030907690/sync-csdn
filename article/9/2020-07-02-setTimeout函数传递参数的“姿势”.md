---
layout:					post
title:					"setTimeout函数传递参数的“姿势”"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- setTimeout传参，我主要是做一个发送完验证码倒计时的功能，下面贴代码:
```javascript
 var timeout = 60;
 function changeSendSmsButtonSecond(buttonId) {
            timeout--;
            if(timeout <= 0 ){
                timeout = 60;
                $(buttonId).text("获取验证码")
            }else{
                $(buttonId).text("重发(" + timeout + ")")
                setTimeout(changeSendSmsButtonSecond, 1000,buttonId)
            }

        }

        function changeSendSmsButton(buttonId) {
            $(buttonId).text("重发(" + timeout + ")")
            setTimeout(changeSendSmsButtonSecond, 1000,buttonId)
        }
```
- 我用的语法是这样的 `setTimeout(function, milliseconds, param1, param2, ...)`