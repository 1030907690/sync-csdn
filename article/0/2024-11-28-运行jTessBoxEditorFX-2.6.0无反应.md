---
layout:					post
title:					"运行jTessBoxEditorFX-2.6.0无反应"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 遇到的问题

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/bebf0bb0dfd14deeb1f08ecc631d48b0.png)
- 无论是点击 `train.bat` 还是`jTessBoxEditorFX.jar`都没有任何反应。也没有任何异常。
- 命令行启动也没有任何效果。


## 解决方案

- 了解到JDK 从 1.8 开始自带 JavaFX，到 JDK 11 开始不再内置 JavaFX，我用的JDK 17 ,要自己下载javafx的sdk。
- 下载地址： [https://gluonhq.com/products/javafx/](https://gluonhq.com/products/javafx/)。选择自己 对应的版本。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/15a7da93db8f4f1fb625c21e20707924.png)

- 完成后解压文件，配置环境变量`PATH_TO_FX`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/78e0f535ff4d430e9bf55e1516c4e36e.png)
- 编辑`train.bat`文件，第一行`set PATH_TO_FX`不需要了，因为我们前面已经设置了环境变量，用`rem`注释。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5e01976aa3584101a2c558150ee6e357.png)

- 保存后，双击`train.bat`即可启动。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/edc3a593087f4e8a822ed93cd792b105.png)



## 参考

- https://blog.csdn.net/weixin_52728894/article/details/136352767
- https://blog.csdn.net/qq_33697094/article/details/126429278
