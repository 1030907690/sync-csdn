---
layout:					post
title:					"android ijkplayer编译和导入ijkplayer-example例子"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 一、简介
- ijkplayer是bilibili开源的视频播放框架, ijkplayer基于FFmpeg的轻量级Android/iOS视频播放器。FFmpeg的是全球领先的多媒体框架，能够解码，编码， 转码，复用，解复用，流，过滤器和播放大部分的视频格式。它提供了录制、转换以及流化音视频的完整解决方案。它包含了非常先进的音频/视频编解码库libavcodec，为了保证高可移植性和编解码质量，libavcodec里很多code都是从头开发的。
- 官方文档地址:[https://github.com/bilibili/ijkplayer](https://github.com/bilibili/ijkplayer)
- 引入包，调用下它的api,即可简单的实现视频播放
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/96ec5168f0c08dbf990e925561c6f49a.png)
- 但是有很多格式是不支持的,比如m3u8，https链接的视频也不能播放（报Protocol not found），这个时候就需要去编译ijkplayer了。
## 二、编译
- 先来两张官方截图，基本上是按照官方的步骤来。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/33106143219c18227d229782ffa3331c.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b2d20af09e970edb99418aff73f0420c.png)
- 1、准备环境
(1)、准备一个ubuntu系统(其他的linux发行版没试过)，没有的用虚拟机装都行
(2)、gcc、g++、make什么的基本编译环境得有
(3)、android sdk,下载地址 : [https://developer.android.com/studio](https://developer.android.com/studio)  ，我使用的android sdk [https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip](https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip)
(4)、android ndk 下载地址: [https://developer.android.com/ndk/downloads](https://developer.android.com/ndk/downloads)(注意要下载对应支持的版本，否则有坑)，我使用的android ndk [https://dl.google.com/android/repository/android-ndk-r10e-linux-x86_64.zip](https://dl.google.com/android/repository/android-ndk-r10e-linux-x86_64.zip)
- 
- 2、准备好后就可以配置环境变量了，安装git和yasm `apt-get install git` , `apt-get install yasm`然后打开环境变量配置文件编辑`vim /etc/profile`追加。

```
#这里的路径填自己的
export ANDROID_SDK=/home/zzq/software/androidSdk
export ANDROID_NDK=/home/zzq/software/android-ndk-r10e
export PATH=$PATH:$ANDROID_SDK/tools:$ANDROID_NDK
```
- 保存后使用 `source /etc/profile`使其生效。
- 4、拉取ijkplayer代码，配置一些属性；这里选择的第一种方案(比较通用)。
```
git clone https://github.com/Bilibili/ijkplayer ijkplayer-android
cd ijkplayer-android
git checkout -B latest k0.8.8
cd config
ln -s module-default.sh module.sh
```
- 5、初始化和编译，这一步主要在拉取ffmpeg和编译代码，比较慢我要了几个小时，而且拉取ffmpeg中途可能失败，还得重新执行。

```
./init-android.sh
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3542b2cd28b0f1ef2cf1144da51cfc5f.png)
```
cd android/contrib
./compile-ffmpeg.sh clean
./compile-ffmpeg.sh all
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b78b5935ee9e4a20e5c5ef063f96491c.png)

```
cd ..
./compile-ijk.sh all
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e3cb83ba12751f2ebcdd622314f32a8d.png)
- 编译完成

## 三、添加https支持
- 导入了上面的例子以后发现还是不能播放https的视频，查了一下资料是没运行关于openssl的脚本。
- 1、初始化（前面的步骤就不再赘述了）

```
 ./init-android.sh

```

```
 ./init-android-openssl.sh
```
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d015e6601828bdc248f73311b56332d5.png)
- 2、清理和编译

```
cd android/contrib
./compile-openssl.sh clean
./compile-openssl.sh all

```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/05807a7b62d1e6b7441ed69e2829ea73.png)
```
./compile-ffmpeg.sh clean 
./compile-ffmpeg.sh all

cd ..
./compile-ijk.sh all

```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2040e4d2cec1b4bdc9ade4e7902d9326.png)
## 四、导入例子
- 1、用Android Studio打开android/ijkplayer，等待Android Studio自动配置好，运行ijkplayer-example，等程序成功安装到手机上后，就可以测试下了，能够成功播放就说明编译已经完全成功了。
- 2、使用。IJKPlayer使用方法跟系统自带的MediaPlayer用法基本相同。
- 例子运行起来基本上是这样的。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2ed2d7ca73e1c058a92cc80d8808b1a3.png)
## 五、可能遇到的问题
-  报错`You need the NDKr10e or later`；解决办法是NDK使用一个低版本，下载地址:[https://developer.android.com/ndk/downloads/older_releases.html](https://developer.android.com/ndk/downloads/older_releases.html),最好下载对应r10e版本（[https://dl.google.com/android/repository/android-ndk-r10e-linux-x86_64.zip](https://dl.google.com/android/repository/android-ndk-r10e-linux-x86_64.zip)）
- ./libavutil/timer.h:38:31: fatal error: linux/perf_event.h: No such file or directory；解决方案是在`module-default.sh`文件最后加入`export COMMON_FF_CFG_FLAGS="$COMMON_FF_CFG_FLAGS --disable-linux-perf"`，因为是重新设置了属性，所以加入之后编译步骤要重头开始。
- 报错Could not resolve com.android.support:appcompat-v7:23.0.1或者Please install the Android Support Repository from the Android SDK Manager.
	- 开始是报Could not resolve com.android.support:appcompat-v7:23.0.1，然后我在Android Studio Android SDK管理界面并未发现这个版本;后面报错Please install the Android Support Repository from the Android SDK Manager.的时候了解到从api 26开始，support libraries 需要从google的maven仓库下载，所以需要在project的build.gradle中allprojects 添加如下配置即可
```
 maven { url "https://maven.google.com" }
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a7df5189b997f2924f7d78bca96ca60a.png)


- 最后附上编译好的代码:[https://github.com/1030907690/ijkplayer-https](https://github.com/1030907690/ijkplayer-https)，另外文章如果有错误的地方，还请指正。