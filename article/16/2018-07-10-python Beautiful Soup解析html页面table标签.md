---
layout:					post
title:					"python Beautiful Soup解析html页面table标签"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
#### 一、紧接上文[js 判断系统类型和手机型号(厂商)](https://blog.csdn.net/baidu_19473529/article/details/80978590)
> - 上文实现了得到系统类型和手机型号了。现在手机型号有了，那么有一个需求：功能是分辨访问用户的手机类型（安卓、IOS），然后跳转对应页面。最好能分清楚用户的手机厂商型号（华为、小米、oppo、vivo）等，然后分别调各自的应用商店。
- iOS倒也无所谓判断了系统类型后直接到苹果应用商店就行了(反正就一个应用商店)；Android的话就要稍微麻烦一点了，要判断不同厂商跳转不同的应用商店(比如小米的就跳小米的应用商店)。
- 为了实现这一需求我把型号写个model.js存放起来，里面一个Map数据结构，存储每个手机型号要跳转的页面(因为前面我们已经实现了得到手机型号了,所以这样写的)。

```
//省略前面部分
............
if (os == "iOS") {//ios系统的处理
        os = md.os() + md.version("iPhone");
        model = md.mobile();
        window.location.href = iosShop.get('default');
    } else if (os == "AndroidOS") {//Android系统的处理
        os = md.os() + md.version("Android");
        var sss = device_type.split(";");
        var i = sss.contains("Build/");
        if (i > -1) {
            model = sss[i].substring(0, sss[i].indexOf("Build/"));
        }
        var locationHref = "";
        //alert(model + "--" +androidShop.has(model));
        if(null != model && "" != model && "undefined" != typeof(model) &&  androidShop.has(trim(model))){
            locationHref = androidShop.get(trim(model));
        }else {
	        //默认的地址
            locationHref = androidShop.get("default");
        }
        window.location.href = locationHref;
    }
............
//省略后面部分
```

![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/90f8adf4455c14bc966763334f9606ab.png)

- 现在还有一个大问题是没有厂商型号的数据，这是个大问题。好在我百度了下`小米的userAgent`意外的搜索到了这个[ fynas实用小工具](http://www.fynas.com/ua)
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/9a5173a59eb1e1ddcf586e7ae0763569.png)
这里的User-Agent正是我想要的，但是我要是用一个个复制粘贴实在太慢了。还是写点代码，解析html靠谱点。于是就用了Beautiful Soup。

#### 二、Beautiful Soup安装和使用
- 安装，[Beautiful Soup文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#)

```
$ easy_install beautifulsoup4
或者
$ pip install beautifulsoup4
```
另外我这里还用到了requests库,可在这里下载 [requests下载](https://pypi.org/project/requests/#files)，github里面也有的。

- 首先使用requests库访问页面得到html，再用Beautiful Soup去解析html，得到整个table。

```
 headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'};
    result = requests.post(url, data={}, verify=False);
    # print(result.text);

    # 初始化并指定解析器
    soup = BeautifulSoup(result.text, "lxml");
    # 得到table
    table = soup.table;
```
- 然后就是得到全部tr标签，查询所有td，td我们要的是第4列User-Agent字符串,也就是td数组3，然后排除"User-Agent字符串"也就是没页的第一行，最后就是截取字符串得到手机型号的操作了。

```
tr_arr = table.find_all("tr");
    for tr in tr_arr:
        # //查询所有td
        tds = tr.find_all('td');
        # for  td in tds:
        # 得到User-Agent字符串
        # print(tds[3].get_text());
        userAgent = tds[3].get_text();
        if "User-Agent字符串" != userAgent :
            user_agent_build = userAgent.split("Build/")[0];
            user_agent_arr = user_agent_build.split(";");
            phoneModel = user_agent_arr[len(user_agent_arr) - 1];
            print(phoneModel.strip());
```

- 完整的代码(完整代码我把要加的js代码手机型号写入了文件)：

```
# -*- coding: utf-8 -*-

'''
抓取 user-agent
文档 https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id10
zhouzhongqing
2018年7月10日22:06:48
'''

import requests;
from bs4 import BeautifulSoup


# 写入文件
def write_to_file(file_name, txt):
    '''''
        讲txt文本存入到file_name文件中
    '''
    print("正在存储文件" + str(file_name));
    # 1 打开文件
    # w 如果没有这个文件将创建这个文件
    '''
    'r'：读
    
    'w'：写
    
    'a'：追加
    
    'r+' == r+w（可读可写，文件若不存在就报错(IOError)）
    
    'w+' == w+r（可读可写，文件若不存在就创建）
    
    'a+' ==a+r（可追加可写，文件若不存在就创建）
    '''
    f = open(file_name, 'a+', encoding='utf-8');
    # 2 读写文件
    f.write(str(txt));
    # 3 关闭文件
    f.close();


'''
发起请求
@:param url
'''

#为了去重
userAgentList = [];


def requestUserAgent(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'};
    result = requests.post(url, data={}, verify=False);
    # print(result.text);

    # 初始化并指定解析器
    soup = BeautifulSoup(result.text, "lxml");
    # 得到table
    table = soup.table;
    # print(table);
    tr_arr = table.find_all("tr");
    for tr in tr_arr:
        # //查询所有td
        tds = tr.find_all('td');
        # for  td in tds:
        # 得到User-Agent字符串
        # print(tds[3].get_text());
        userAgent = tds[3].get_text();
        if "User-Agent字符串" != userAgent :
            user_agent_build = userAgent.split("Build/")[0];
            user_agent_arr = user_agent_build.split(";");
            phoneModel = user_agent_arr[len(user_agent_arr) - 1];
            print(phoneModel.strip());
            #排重
            if phoneModel.strip() not in userAgentList:
                write_to_file("d:/vivo.txt","androidShop.set(\""+phoneModel.strip()+"\",vivoDownloadAddress);\n")
                userAgentList.append(phoneModel.strip());


if __name__ == '__main__':
    print("start");
    '''
    userAgent = "Mozilla/5.0 (Linux; Android 6.0; vivo Y67A Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/7.4 baiduboxapp/8.5 (Baidu; P1 6.0)";
    user_agent_build = userAgent.split("Build/")[0];
    user_agent_arr = user_agent_build.split(";");
    phoneModel = user_agent_arr[len(user_agent_arr) - 1];
    print(phoneModel.strip())
    '''

    for i in range(1, 83):
         print("这是第"+str(i)+"页");
         #vivo的机型
         requestUserAgent("http://www.fynas.com/ua/search?b=&d=vivo&page="+str(i));

    '''
    for i in range(1, 84):
        print("这是第" + str(i) + "页");
        # 小米的机型
        requestUserAgent("http://www.fynas.com/ua/search?d=%E5%B0%8F%E7%B1%B3&b=&page=" + str(i));
    '''

    print("end");

```
- 得到的vivo的手机型号
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/b1935edbf9a8633e4b6064dd4034e99d.png)
大致就是这样了，要得到其他机型，就再加for循环，拼接URL来做就差不多了。