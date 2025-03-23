---
layout:					post
title:					"Project /Users/mac/work/video-client-ios/GHYProj.xcodeproj cannot be opened because it is missing it"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 从git上刚拉下来的项目，使用xcode打开提示`Project /Users/mac/work/video-client-ios/GHYProj.xcodeproj cannot be opened because it is missing it`，不允许打开项目。
## 原因分析
### 第一种情况：缺少`project.pbxproj`文件
- 右键根目录的`GHYProj.xcodeproj`，选择显示包内容。<font color="red">注意：这里`GHYProj.xcodeproj`  ，GHYProj是我项目的名称，自己的可能不一样。</font>,如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e2f33f84e6a5c297bd593c219bb70b63.png)
### 第二种情况，文件有冲突
- 经历过多人，多次提交后，`project.pbxproj`文件内容有冲突，有特殊符号如：=、>>、<<之类的。
## 解决方案
### 第一种情况
- 拿到`project.pbxproj`文件就可以了。
### 第二种情况
- 解决冲突，删除特殊字符。

