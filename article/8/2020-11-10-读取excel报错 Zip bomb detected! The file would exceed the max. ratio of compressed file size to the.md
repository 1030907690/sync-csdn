---
layout:					post
title:					"读取excel报错 Zip bomb detected! The file would exceed the max. ratio of compressed file size to the"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 读取excel报错 `Zip bomb detected! The file would exceed the max. ratio of compressed file size to the size of the expanded data`，完整报错信息如下所示。
>java.io.IOException: Zip bomb detected! The file would exceed the max. ratio of compressed file size to the size of the expanded data.
This may indicate that the file is used to inflate memory usage and thus could pose a security risk.
You can adjust this limit via ZipSecureFile.setMinInflateRatio() if you need to work with files which exceed this limit.
Uncompressed size: 103231, Raw/compressed size: 900, ratio: 0.008718
Limits: MIN_INFLATE_RATIO: 0.010000, Entry: xl/pivotCache/pivotCacheRecords1.xml

- 主要原因是文件太大，解决办法增加如下代码。

```java
ZipSecureFile.setMinInflateRatio(-1.0d);
```
- 完整代码如下所示。

```java
     FileInputStream fileInputStream = null;
        try {
            fileInputStream = new FileInputStream(filePath);
            ZipSecureFile.setMinInflateRatio(-1.0d);
            XSSFWorkbook sheets = new XSSFWorkbook(fileInputStream);
            //获取sheet
           XSSFSheet sheet = sheets.getSheet(sheetName);
        } catch (Exception e) {
            e.printStackTrace();
        }
```
- 有可能还会发生堆内存溢出，需要设置堆内存大小，如下所示。

```java
-Xmx5550m -Xms5550m
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/99dd1b48dcc7eee1407ecccbf1b7f901.png#pic_center)
