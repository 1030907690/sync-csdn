---
layout:					post
title:					"python自动生成requirements.txt文件"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
### 背景
- 因为项目在windows开发，有1台测试环境，还有正式环境；第一次搭建环境的时候，就需要安装很多依赖；一个一个的安装很麻烦；这时候就可以用`requirements.txt`文件解决。可以自己写，也可以自动生成。


### 生成requirements.txt的办法
#### 方案一

```bash
pip freeze > requirements.txt
```

- 不过这个方案有个缺点就是，会把您当前电脑安装的所以库都列出来；这样的话就有很多您当前项目用不到的库也在`requirements.txt`文件里。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/605726145b7a0b6defe4d1255ec0fb93.png)

#### 方案二
- 使用 `pipreqs` 用于生成 `requirements.txt` 文件可以根据需要导入的任何项目

```bash
pip install pipreqs
#当前项目根目录下执行
pipreqs .
```
- 如果执行 `pipreqs .` 报错

```bash
  File "D:\software\Python35\Scripts\pipreqs.exe\__main__.py", line 9, in <module>
  File "d:\software\python35\lib\site-packages\pipreqs\pipreqs.py", line 470, in main
    init(args)
  File "d:\software\python35\lib\site-packages\pipreqs\pipreqs.py", line 409, in init
    follow_links=follow_links)
  File "d:\software\python35\lib\site-packages\pipreqs\pipreqs.py", line 122, in get_all_imports
    contents = f.read()
UnicodeDecodeError: 'gbk' codec can't decode byte 0xa6 in position 197: illegal multibyte sequence

```
- 请将命令换成：

```bash
pipreqs . --encoding=utf-8
```
### 安装requirements.txt中的类库内容

```bash
pip install -r requirements.txt
```
