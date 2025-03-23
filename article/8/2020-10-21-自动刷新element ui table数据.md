---
layout:					post
title:					"自动刷新element ui table数据"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 使用`setInterval`函数调用重新赋值table表格getTableList方法，代码如下所示。

```html
 created() {
 
    this.getTableList();
    this.refreshTable();
  },
...省略...
  refreshTable() {
      setInterval(() =>  {
        this.getTableList();
      }, 60000);
    },
```
