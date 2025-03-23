---
layout:					post
title:					"Avoid mutating a prop directly since the value will be overwritten whenever the parent component re-"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/50023ec313af85790d2f0d13173ab459.png)

>[Vue warn]: Avoid mutating a prop directly since the value will be overwritten whenever the parent component re-renders. Instead, use a data or computed property based on the prop's value. Prop being mutated: "sidebarDialogVisible"

- 警告原因，我不应该直接在里面修改`props`属性的值。可能会被父类覆盖。

- 解决方案。
- 新建data `sidebarDialogVisible`,原来的prop属性我改了名字`sidebarDialogVisibleProp`，这样我html代码就不动了。
```js
 ... 省略 ...
   props: {
    sidebarDialogVisibleProp: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      sidebarDialogVisible: this.sidebarDialogVisibleProp,
    };
  },
  ... 省略 ...
```

- 监听变化

```js
  watch:{
    sidebarDialogVisibleProp(newVal) {
      this.sidebarDialogVisible = newVal
    },
  },
```

- 父类使用

```html
 <Sidebar :sidebarDialogVisibleProp="sidebarSwitch"></Sidebar>
```
