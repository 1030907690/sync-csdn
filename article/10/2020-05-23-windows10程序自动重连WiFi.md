---
layout:					post
title:					"windows10程序自动重连WiFi"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
### 背景
- 我不知道是我的路由器有问题么，还是windows10系统，老是过一会儿就没网了![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0296c166c11b04d3943f117467f84665.png)，然后重连又会好一会儿，为此我找了点资料，去做自动重连的脚本。

### 基本命令
- 查看周围可用 wifi 

```bash
 netsh wlan show networks mode=bssid
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bf8bf5720eb8359b6a3f6fa4d15bfe59.png)
- 连接过的wifi（已经配置过的）
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/08b9961f18730a0606c15d30dd00494d.png)
- 断开连接

```bash
netsh wlan disconnect
```

- 指定所需配置文件及 ssid 连接；我连接的是`ChinaNet-efCC`

```bash
netsh wlan connect ssid=ChinaNet-efCC name=ChinaNet-efCC
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/50fb69ea850341d928c23f807eeecd65.png)
- 有了基础命令就可以做很多操作了

### 写自动脚本
- 因为我对bat还不算太熟，所以我用python写的；有了基础命令也可以用其他语言写；下面是python代码;`大概思路就是ping一个域名像百度，如果不通就重连WiFi`。
- auto-reconnect-wifi.py  源码地址:[https://github.com/1030907690/public-script/blob/master/generic/auto-reconnect-wifi.py](https://github.com/1030907690/public-script/blob/master/generic/auto-reconnect-wifi.py)

```bash
# -*- coding: utf-8 -*-
'''
zzq
重连WiFi
2020年5月22日23:56:24
'''
import subprocess
import time
import os
from time import strftime, localtime

ssid = "ChinaNet-efCC"


def reconnect():
    '''
    重连
    '''
    print("%s 正在重连WiFi" % strftime("%Y-%m-%d %H:%M:%S", localtime()))
    os.system("netsh wlan disconnect")
    os.system("netsh wlan connect ssid=%s name=%s" % (ssid, ssid))


def check_wifi():
   
    subp = subprocess.Popen("ping baidu.com", stdout=subprocess.PIPE)
    while subp.poll() is None:
        text = str(subp.stdout.readline(), encoding='utf=8')
        print(" %s" % text)
        if match(text):
            reconnect()
            break
       


def match(text):
    '''
    匹配
    '''
    # 如果匹配到failure就认为是没网了   我这系统是英文版  其他的可以改下匹配规则
    if text:
        if text.find('failure') >= 0 or text.find('could not find host') >= 0:
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    while True:
        check_wifi()
        time.sleep(20)


```

- 我这里是windows10英文版本，如果没网会是这样的结果；我去匹配了字符串，判断要不要重连。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e8f72c12f997244ffda34967dfb19238.png)

- 为了测试，我中途断网，看下效果是成功的
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/52f1946c7834925665d318e980436232.png)