---
layout:					post
title:					"scrapy splash模拟点击"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
### 背景
- 遇到的问题：在做爬虫时遇到用js跳转链接的
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/86b17534af961e9337f93fff77284430.png)
- 并且跳转的链接是加了密的，不好做拼接，这个时候一般解决办法就是`模拟点击`了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2b7e621b05d11623e9ef2042a7d13d61.png)
- scrapy模拟点击的话一般是用`selenium`或者`splash`，我这里使用的是`splash`，貌似官方也是推荐用`splash`

### 使用splash
#### 文档
- github [https://github.com/scrapy-plugins/scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash)
- 文档 [https://splash.readthedocs.io/en/latest/install.html](https://splash.readthedocs.io/en/latest/install.html)

#### 安装
- 安装依赖库

```bash
 pip install scrapy-splash
```
- splash需要用docker启一个服务
- 安装docker文档 [https://docs.docker.com/v17.12/install/#supported-platforms](https://docs.docker.com/v17.12/install/#supported-platforms)，我这里写了一键安装docker脚本 `wget https://github.com/1030907690/public-script/raw/master/docker/install-docker.sh && sh install-docker.sh` 适用于`centos`
 
```bash
docker run --name splash-standard -d -p 8050:8050 scrapinghub/splash
```

- 修改`settings.py`文件，按照上面文档来
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2a3e11c91d3f451e8a02f367666a3c98.png)

```bash
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawlerScrapy.middlewares.CrawlerscrapyDownloaderMiddleware': 543,
#}

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPLASH_URL = 'http://192.168.0.188:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'crawlerScrapy.pipelines.CrawlerscrapyPipeline': 300,
    'crawlerScrapy.pipelines.MongoPipeline': 300,
    'crawlerScrapy.pipelines.CustomImagesPipeline': 300,
    'crawlerScrapy.pipelines.CustomFilesPipeline': 300,
}
```

- `SPLASH_URL = 'http://192.168.0.188:8050'`是刚刚启动的docker服务
- 先写lua脚本，写了可以在splash的web页面测试是否成功，如下:
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1e5fb1c3e4ff96780850fe82c798b01c.png)
- 具体`spiders`代码

```bash
import scrapy
from ..items import *
import os
import requests
from scrapy_splash import SplashRequest

#..........省略..........
class AbcComic(scrapy.Spider):
    # 运行 scrapy crawl 800cms
    name = "abc_comic"
    allowed_domains = [host_name]
    # 自定义配置
    custom_settings = {
        "USER_AGENT": PC_USER_AGENT,
    }

    start_urls = [base_url]

    # 模拟点击采用js的方式
    lua_script = """
       function main(splash, args)
          assert(splash:go(args.url))
          assert(splash:wait(0.5))
          splash:runjs(args.script)
          assert(splash:wait(0.5))
          return splash:html()
        end
       """

    # 进入章节内容
    def chapter_info(self, response):
        '''
           章节详情
           :param response:
           :return:
           '''
        print(str(response.body, 'utf-8'))

    def info(self, response):
        '''
        漫画详情
        :param response:
        :return:
        '''

        element_book_header = response.xpath("//div[@class='book-header']")
        photo = element_book_header.xpath("p[1]/img[1]/@src").extract_first()
        name = element_book_header.xpath("h1[1]/text()").extract_first()
        author = element_book_header.xpath("p[2]/text()").extract_first()
        if author:
            author = author.replace("作者: ", "")
        url = response.meta['relative_path']
        status = 0
        if name and name.find('完结') >= 0:
            status = 1  # 表示完结

        

        element_chapter_list = response.xpath("//div[@class='list-left']/div[@class='list-item']")

        for chapter_item in element_chapter_list:
            element_a = chapter_item.xpath("a[1]/@onclick").extract_first()
            print(element_a)
            yield SplashRequest(response.url,headers={"User-Agent": PC_USER_AGENT}, callback=self.chapter_info,
                                endpoint='execute',
                                args={'lua_source': self.lua_script, 'url': response.url,'script': element_a})

        print(name + " " + base_url + photo)

    def parse(self, response):
        # print(str(response.body,'utf-8'))
        element_book_list = response.xpath("//div[@id='booklist']/div")
        for book_item in element_book_list:
            book_click = book_item.xpath("div[1]/@onclick").extract_first()
            book_url = book_click[book_click.find("'") + 1:book_click.rfind("'")]
            if book_url:
                yield response.follow(book_url, headers={"User-Agent": PC_USER_AGENT}, meta={"relative_path": book_url},
                                      callback=self.info)

```
- 我省略了很多代码，重要的代码就是

```bash
yield SplashRequest(response.url,headers={"User-Agent": PC_USER_AGENT}, callback=self.chapter_info,
                                endpoint='execute',
                                args={'lua_source': self.lua_script, 'url': response.url,'script': element_a})
```
- lua脚本的意思很简单访问`args.url`页面，然后执行这个页面上的脚本`args.script`，变量是`yield SplashRequest`的时候传过去的；把这个url传进去，然后就是发起点击事件，也就是执行这个页面的js`getInfo('1454','51001')`之类的；element_a的值就是`getInfo('1454','51001')`这些。

- 代码运行效果，已经能执行js到下一个页面了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/be8fd76fca33e910dd0e59555dc9f8d9.png)
- 文章到这儿已经结束了，感谢您的观看，如果有任何问题，请批评指出，感激不尽。