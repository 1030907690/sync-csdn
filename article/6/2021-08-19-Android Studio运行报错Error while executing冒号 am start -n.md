---
layout:					post
title:					"Android Studio运行报错Error while executing: am start -n"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)

## 报错详情

```
08/19 09:54:18: Launching app
$ adb install-multiple -r -t D:\work\self\CallAutoRecord\app\build\intermediates\split-apk\debug\slices\slice_4.apk D:\work\self\CallAutoRecord\app\build\intermediates\split-apk\debug\slices\slice_9.apk D:\work\self\CallAutoRecord\app\build\intermediates\split-apk\debug\slices\slice_3.apk D:\work\self\CallAutoRecord\app\build\intermediates\split-apk\debug\slices\slice_8.apk D:\work\self\CallAutoRecord\app\build\intermediates\split-apk\debug\slices\slice_6.apk D:\work\self\CallAutoRecord\app\build\intermediates\split-apk\debug\slices\slice_5.apk D:\work\self\CallAutoRecord\app\build\intermediates\split-apk\debug\dep\dependencies.apk D:\work\self\CallAutoRecord\app\build\intermediates\split-apk\debug\slices\slice_7.apk D:\work\self\CallAutoRecord\app\build\intermediates\split-apk\debug\slices\slice_2.apk D:\work\self\CallAutoRecord\app\build\intermediates\split-apk\debug\slices\slice_1.apk D:\work\self\CallAutoRecord\app\build\intermediates\resources\instant-run\debug\resources-debug.apk D:\work\self\CallAutoRecord\app\build\intermediates\split-apk\debug\slices\slice_0.apk D:\work\self\CallAutoRecord\app\build\intermediates\instant-run-apk\debug\app-debug.apk 
Split APKs installed in 10 s 564 ms
$ adb shell am start -n "com.guoqi.callautorecord/com.guoqi.callautorecord.MainActivity" -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -D
Error while executing: am start -n "com.guoqi.callautorecord/com.guoqi.callautorecord.MainActivity" -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -D
Starting: Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] cmp=com.guoqi.callautorecord/.MainActivity }
Error type 3
Error: Activity class {com.guoqi.callautorecord/com.guoqi.callautorecord.MainActivity} does not exist.

Error while Launching activity
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/565e1f2e17e81797f5bba161a9c6f778.png)
## 问题原因
- 手机系统BUG没有将APP卸载干净，导致安装失败运行不起来。
## 解决方案
- 先到`sdk\platform-tools`路径找到`adb`命令
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9c880036727998a08bfeedb68151c24c.png)

- 然后在当前目录，打开命令行窗口，输入`adb devices`。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ba1ccabcd8233feaab41ef9a6b166134.png)
- 确认手机已连上，然后用adb卸载，输入命令，`adb  uninstall com.guoqi.callautorecord`（`com.guoqi.callautorecord`是我自己的包名，要换成自己的哦）
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3a361ed84690c8970abcea7707ccf778.png)

- 再安装就成功了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bb570e24b433bbcbca9b9323fad2f0b4.png)
