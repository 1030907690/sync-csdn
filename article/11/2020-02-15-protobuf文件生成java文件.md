---
layout:					post
title:					"protobuf文件生成java文件"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
### 下载可执行文件
- 下载地址:[https://github.com/protocolbuffers/protobuf/releases](https://github.com/protocolbuffers/protobuf/releases)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1c589d15fcd429658a950e970539d1b5.png)
- 比如我的是Linux 64位则可以下载`protoc-3.11.4-linux-x86_64.zip`，解压出来里面有个`protoc`，这就是需要的可执行文件。
- 命令格式

```
./protoc  xxx.proto --java_out=xxx
```
- 我的生成脚本；

```
#!/bin/bash
pwd_dir=`pwd`
if [ ! -d $pwd_dir"/src/main/java" ]; then
 #先来个文件夹去装这些生成的java文件
  mkdir -p $pwd_dir"/src/main/java"
fi
cd protos
#生成这个目录所有proto文件
../protoc  *. proto --java_out=../src/main/java

```



