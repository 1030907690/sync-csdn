---
layout:					post
title:					"python binascii.Error: Incorrect padding"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 在有些字符串base64解码的时候可能会报错 `Incorrect padding`报错如下:

```python
Traceback (most recent call last):
  File "/home/zzq/software/pycharm-2017.2.7/helpers/pydev/pydevd.py", line 1599, in <module>
    globals = debugger.run(setup['file'], None, None, is_module)
  File "/home/zzq/software/pycharm-2017.2.7/helpers/pydev/pydevd.py", line 1026, in run
    pydev_imports.execfile(file, globals, locals)  # execute the script
  File "/home/zzq/software/pycharm-2017.2.7/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "/home/zzq/work/self/public-script/generic/ssr_update.py", line 156, in <module>
    ssr_account3()
  File "/home/zzq/work/self/public-script/generic/ssr_update.py", line 146, in ssr_account3
    ssr_info = str(base64.b64decode(content.text),
  File "/usr/local/python3.5/lib/python3.5/base64.py", line 88, in b64decode
    return binascii.a2b_base64(s)
binascii.Error: Incorrect padding
```
- 有可能是python base64库编码规则不太统一导致的；解决办法就是对base64解码的string补齐等号就可以了；　python中base64串的长度需为4的整数倍，故对长度不为4整数倍的base64串需要用"='补足

```python

def decode_base64(data):
    """Decode base64, padding being optional.
    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '='* missing_padding
    return str(base64.b64decode(data),
                           encoding='utf-8')
```
- 这回把加密字符串传过去就没报错了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4d68c3cc582db12a67360c760d60491f.png)
