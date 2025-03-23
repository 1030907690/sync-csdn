---
layout:					post
title:					"Ubuntu adb devices no permissions (user in plugdev group; are your udev rules wrong?);"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 我的是Ubuntu18.04异常情况如下:
	- as找不到设备我的小米Max3
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a1ba80e3355c312a60ea1cd3bb731392.png)
	- 命令查看

```
root@zzq-HP-Pavilion-15-Notebook-PC:/home/zzq/software/Android/Sdk/platform-tools# ./adb devices
List of devices attached
3eefc48f	no permissions (user in plugdev group; are your udev rules wrong?); see [http://developer.android.com/tools/device.html]
```
- 没有权限后来了解到需要添加usb驱动，在Windows上一般都是自动安装，很难出现这种问题。
- 解决办法
	- 1、先用`lsusb`命令找到自己的厂商号和产品号
	
	```
	zzq@zzq-HP-Pavilion-15-Notebook-PC:~/software/android-studio$ lsusb
	Bus 002 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
	Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
	Bus 001 Device 004: ID 04d9:a09e Holtek Semiconductor, Inc. 
	Bus 001 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
	Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
	Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
	Bus 003 Device 002: ID 05c8:0361 Cheng Uei Precision Industry Co., Ltd (Foxlink) SunplusIT INC. HP Truevision HD Webcam
	Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
	
	```
	
	```
	zzq@zzq-HP-Pavilion-15-Notebook-PC:~/software/android-studio$ lsusb
	Bus 002 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
	Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
	Bus 001 Device 004: ID 04d9:a09e Holtek Semiconductor, Inc. 
	Bus 001 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
	Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
	Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
	Bus 003 Device 002: ID 05c8:0361 Cheng Uei Precision Industry Co., Ltd (Foxlink) SunplusIT INC. HP Truevision HD Webcam
	Bus 003 Device 014: ID 18d1:4ee7 Google Inc. 
	Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
	```
	- 两次`lsusb`命令就能很容易找到那个新增设备了
	```
	Bus 003 Device 014: ID 18d1:4ee7 Google Inc. 
	```
	
	- 2、在目录/etc/udev/rules.d/下添加文件70-android.rules，根据上面的设备信息在文件中添加如下内容：
	
	```
	SUBSYSTEM=="usb", ATTRS{idVendor}=="18d1", ATTRS{idProduct}=="4ee7",MODE="0666"
	```
	- 其中`idVendor`和`idProduct`分别代表厂商号和产品号,一般就改这2个值就可以了。


- 最后效果成功了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/46046f03f0df154085c209fbef0f5f70.jpeg)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bcf685615fb1ae6a05e28b1413922133.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/faa709b06706c0fa47dd8cb0fb26f352.png)