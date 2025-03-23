---
layout:					post
title:					"Could not resolve com.tencent.mm.opensdk:wechat-sdk-android-with-mta:+."
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- Android导包报错：

```javascript
Could not resolve com.tencent.mm.opensdk:wechat-sdk-android-with-mta:+.
```
- 解决方案
	- 到[https://bintray.com/wechat-sdk-team/maven/com.tencent.mm.opensdk%3Awechat-sdk-android-with-mta](https://bintray.com/wechat-sdk-team/maven/com.tencent.mm.opensdk:wechat-sdk-android-with-mta)找到详细版本，指定详细版本

	```javascript
	implementation 'com.tencent.mm.opensdk:wechat-sdk-android-with-mta:5.4.0'
	```
