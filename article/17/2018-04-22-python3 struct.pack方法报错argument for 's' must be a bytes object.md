---
layout:					post
title:					"python3 struct.pack方法报错argument for 's' must be a bytes object"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 在python3下使用struct模块代码

```
fileHead = struct.pack('128sl', os.path.basename(filePath),os.stat(filePath).st_size);
```

抛出异常：

```
argument for 's' must be a bytes object必须要是字节类型。
```

- 解决办法：
 把字符串的地方转为字节类型,还要要先转成utf-8的编码(否则报错`string argument without an encoding`),代码如下:
 
 
```
fileHead = struct.pack('128sl', bytes(os.path.basename(filePath).encode('utf-8')),os.stat(filePath).st_size);

```