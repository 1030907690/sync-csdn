---
layout:					post
title:					"python导包问题python Parent module '' not loaded, cannot perform relative import"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- Python导包报错如下:

```csharp
Traceback (most recent call last):
  File "G:\software\JetBrains\PyCharm2017.3.4\helpers\pydev\pydevd.py", line 1668, in <module>
    main()
  File "G:\software\JetBrains\PyCharm2017.3.4\helpers\pydev\pydevd.py", line 1662, in main
    globals = debugger.run(setup['file'], None, None, is_module)
  File "G:\software\JetBrains\PyCharm2017.3.4\helpers\pydev\pydevd.py", line 1072, in run
    pydev_imports.execfile(file, globals, locals)  # execute the script
  File "G:\software\JetBrains\PyCharm2017.3.4\helpers\pydev\_pydev_imps\_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "G:/work/scrapyDemo/parse/parse_file.py", line 7, in <module>
    from  .Video import *
SystemError: Parent module '' not loaded, cannot perform relative import
```
- 定义一个同级目录的对象，导入报错（大意是未加载python父模块“”，无法执行相对导入）

```python
class Video:
    #定义基本属性
    name = ''
    type = ''
    relative_path = ''
    img = ''

    #定义构造方法
    def __init__(self,name,type,relative_path,img):
        self.name = name
        self.type = type
        self.relative_path = relative_path
        self.img = img
```
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e6a6721232658e24c610cf69efc8a2a5.png)
- 解决办法，加上parse目录就好了

```python
from parse.Video import *
```
