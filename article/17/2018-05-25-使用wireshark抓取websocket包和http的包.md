---
layout:					post
title:					"使用wireshark抓取websocket包和http的包"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
> 由于我的是android手机,我这里就写的利用wireshark抓android手机websocket的包(目前不知道ios是不是一样的)

#### 一、共享一个WiFi
- 电脑需要共享一个WiFi出去,保证手机连的是电脑的网,我这里使用的是360免费WiFi(当然也可以使用其他同类似功能的软件,还有如果你不是真机用电脑安个android模拟器也是可以的。比如夜神模拟器等等)
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/7d2a8d2c6d1d2e2e2841241c15183303.png)


#### 二、安装和使用wireshark
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/baa7f81e42792241de6ee00618bc0f88.png)

- WebSocket ：
  - 我们要去监听的就是这个本地连接(这块网卡),点进去,在上边的输入框输入`websocket`关键字。
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/c2c53277736c0838dde0ad3f5f010867.png)

- source是代表来源ip，destination是代表接收人。

- http
     - http也是一样的在上面输入框输入`http`过滤下结果,得到http的结果。如果只想看某个ip的结果`http && ip.src == 192.168.0.134`,一个还有好多过滤结果的关键字。






- wireshark着实很强大,肯定还有好多功能我还没探索到,这里我只列举了其中的一点皮毛而已,文章如有不正之处,希望能批评指出。