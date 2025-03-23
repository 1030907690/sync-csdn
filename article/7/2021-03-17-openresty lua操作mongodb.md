---
layout:					post
title:					"openresty lua操作mongodb"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)

## 准备
- 安装Openresty（官网[http://openresty.org/cn/](http://openresty.org/cn/)）。
 Centos一键安装脚本

```
wget -c https://github.com/1030907690/public-script/raw/master/generic/install-openresty-centos.sh && sh install-openresty-centos.sh
```
- 下载三个依赖

```
git clone https://github.com/isage/lua-resty-moongoo.git
git clone git://github.com/mongodb/libbson.git
git clone https://github.com/isage/lua-cbson.git
```
## 安装依赖
### lua-resty-moongo
- 下载下来后，把`moongoo.lua`和`moongoo文件夹`复制到`lualib/resty`，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/db122d20a321abf39d9c23c888218dde.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f1cc9b5e5f9c308413086eb1bdb749f3.png)
### libbson
- 执行以下命令。如下图所示。
> 先yum install libtool安装一下，否则执行./autogen.sh 可能报错。
```
cd libbson
./autogen.sh 
make
make install
make clean && make LUA_INCLUDE_DIR=/usr/local/openresty/luajit/include/luajit-2.1 LUA_CMODULE_DIR=/usr/local/openresty/lualib LUA_MODULE_DIR=/usr/local/openresty/lualib CBSON_CFLAGS="-g -fpic -I/usr/local/include/libbson-1.0/ " CC=cc
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2d2a472a1ffdae9ec2d03626f58cbd74.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3356cef9663e6193d746fc6f2e17b909.png)
### lua-cbson
- 执行以下命令，如下图所示。

```
cd lua-cbson
mkdir build  
cd build  
cmake ..  
make  
make install
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f473c1e6a18dc7ac3515973c04b132a8.png)
## 使用
### Openresty配置文件

```
...省略...
    location / {
    	 default_type text/html;
	    content_by_lua_file conf/lua_src/video_openapi.lua;    
    }
    ...省略...
```
### 操作MongoDB数据库Lua测试代码

```
local moongoo = require("resty.moongoo") -- 引入依赖
local cbson = require("cbson") 
local mg, err = moongoo.new("mongodb://root:root@127.0.0.1:27017") -- 创建连接
if not mg then
  error(err) -- 如果有错误
 end
local col = mg:db("mm_video"):collection("video_config") -- 选择db和表
-- 插入数据
local ids, err = col:insert({ videoName = "bar",vipVideoPlayUrl= "test"})
mg:close() --关闭连接
```
> Api文档地址： [https://github.com/isage/lua-resty-moongoo](https://github.com/isage/lua-resty-moongoo)，也可以自己找其他的库也条件的自己写也行。
### 测试结果
- 成功插入数据，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/eed3c388a2aa8d339fe681e2477ebe4e.png)
 
 ## 常见问题整理
### [error] 26883#0: *1673522 lua entry thread aborted: runtime error: error loading module 'cbson' from file '/usr/local/openresty/luajit/lib/lua/5.1/cbson.so':	libbson-1.0.so.0: cannot open shared object file: No such file or directory stack traceback:
> 这个问题发生在代码运行阶段 。
- 建立libbson-1.0.so.0软链接并刷新和系统共享的动态链接库
```
ln -s /usr/local/lib/libbson-1.0.so.0  /usr/lib/libbson-1.0.so.0
ldconfig
```
