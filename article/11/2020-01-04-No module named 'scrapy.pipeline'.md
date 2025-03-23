---
layout:					post
title:					"No module named 'scrapy.pipeline'"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 做scrapy爬虫的时候导入下载的`Pipeline`报错

```bash
2020-01-04 20:45:21 [twisted] CRITICAL: 
Traceback (most recent call last):
  File "D:\software\Python35\lib\site-packages\twisted\internet\defer.py", line 1386, in _inlineCallbacks
    result = g.send(result)
  File "D:\software\Python35\lib\site-packages\scrapy-1.5.0-py3.5.egg\scrapy\crawler.py", line 80, in crawl
    self.engine = self._create_engine()
  File "D:\software\Python35\lib\site-packages\scrapy-1.5.0-py3.5.egg\scrapy\crawler.py", line 105, in _create_engine
    return ExecutionEngine(self, lambda _: self.stop())
  File "D:\software\Python35\lib\site-packages\scrapy-1.5.0-py3.5.egg\scrapy\core\engine.py", line 70, in __init__
    self.scraper = Scraper(crawler)
  File "D:\software\Python35\lib\site-packages\scrapy-1.5.0-py3.5.egg\scrapy\core\scraper.py", line 71, in __init__
    self.itemproc = itemproc_cls.from_crawler(crawler)
  File "D:\software\Python35\lib\site-packages\scrapy-1.5.0-py3.5.egg\scrapy\middleware.py", line 58, in from_crawler
    return cls.from_settings(crawler.settings, crawler)
  File "D:\software\Python35\lib\site-packages\scrapy-1.5.0-py3.5.egg\scrapy\middleware.py", line 34, in from_settings
    mwcls = load_object(clspath)
  File "D:\software\Python35\lib\site-packages\scrapy-1.5.0-py3.5.egg\scrapy\utils\misc.py", line 44, in load_object
    mod = import_module(module)
  File "D:\software\Python35\lib\importlib\__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 986, in _gcd_import
  File "<frozen importlib._bootstrap>", line 969, in _find_and_load
  File "<frozen importlib._bootstrap>", line 944, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 222, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 986, in _gcd_import
  File "<frozen importlib._bootstrap>", line 969, in _find_and_load
  File "<frozen importlib._bootstrap>", line 956, in _find_and_load_unlocked
ImportError: No module named 'scrapy.pipeline'

```
- 在python文件导入了下看有没有这个路径，路径是这样的
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d54b90737789d47d75afdacfc950b7f8.png)
- 对比了下配置感觉有问题 
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c487f6f8f2d1895dd4da3522a1d696ea.png)
- 万万没想到这中文文档有问题
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7b8f41118c4dcdcdf6cbc4308143d27b.png)
- 回头看英文文档是对的
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/85836bd66f29fecab9599e006e13a584.png)
- 看来以后还得多看英文文档对照着看了。