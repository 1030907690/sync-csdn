---
layout:					post
title:					"解决easypoi多行表头ExcelImportUtil.importExcel，无法获取值"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)

## 背景
- 需要读取excel数据，我使用的是 easypoi的ExcelImportUtil.importExcel方法。
- 读取的表格格式如下图所示，注意：多行的表头。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1860ae78d9d48e38a594463b09e1df83.png)
- 代码如下所示。

```java
package com.springboot.sample.service;

import cn.afterturn.easypoi.excel.ExcelImportUtil;
import cn.afterturn.easypoi.excel.entity.ImportParams;

import java.io.File;
import java.util.List;

public class Reader {

    public static void main(String[] args) {
        File file = new File("D:\\work\\excel\\temp\\xxx2.xlsx");
        ImportParams importParams = new ImportParams();
        importParams.setTitleRows(0);
        importParams.setHeadRows(2);
        importParams.setSheetNum(1);
        List<UserPo> userObjects = ExcelImportUtil.importExcel(file, UserPo.class, importParams);

        for (UserPo userObject : userObjects) {
            System.out.println(userObject.getDate() + "---" + userObject.getGuestId());
        }
    }
}
```


```java
package com.springboot.sample.service;

import cn.afterturn.easypoi.excel.annotation.Excel;
import lombok.Data;

@Data
public class UserPo {
    @Excel(name = "日期",importFormat = "yyyy/MM/dd")
    String date;

    @Excel(name = "对话ID")
    String talkId;

    @Excel(name = "访客ID")
    String guestId;
}

```
- 结果如下所示，日期字段一直是null。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d852db5241a1a32ce193788e8edc9f0a.png)

## 解决方案
- 第二行表头第一列增加第一列的名称（**格式：第一行的名称_下一行第一列的名称，下一行的第一列需要这样做**），代码如下所示。

```java
package com.springboot.sample.service;

import cn.afterturn.easypoi.excel.annotation.Excel;
import lombok.Data;

@Data
public class UserPo {
    @Excel(name = "投放部分_日期",importFormat = "yyyy/MM/dd")
    String date;// excel时间类型注意增加格式

    @Excel(name = "对话ID")
    String talkId;

    @Excel(name = "访客ID")
    String guestId;
}
```
- 结果如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/74881992027b21d2133debeb7bb436a4.png)

- 另一个方法，UserPo 不改，修改titleRows（表格标题行数,默认0）和headRows（表头行数,默认1）属性。

```java
package com.springboot.sample.service;

import cn.afterturn.easypoi.excel.ExcelImportUtil;
import cn.afterturn.easypoi.excel.entity.ImportParams;

import java.io.File;
import java.util.List;

public class Reader {

    public static void main(String[] args) {
        File file = new File("D:\\work\\excel\\temp\\xxx2.xlsx");
        ImportParams importParams = new ImportParams();
        importParams.setTitleRows(1);
        importParams.setHeadRows(1);
        importParams.setSheetNum(1);
        List<UserPo> userObjects = ExcelImportUtil.importExcel(file, UserPo.class, importParams);

        for (UserPo userObject : userObjects) {
            System.out.println(userObject.getDate() + "---" + userObject.getGuestId());
        }
    }
}
```
