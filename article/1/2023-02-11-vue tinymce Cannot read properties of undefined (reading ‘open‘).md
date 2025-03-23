---
layout:					post
title:					"vue tinymce Cannot read properties of undefined (reading ‘open‘)"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 在页面直接使用tinymce `<Editor>`标签会报错

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/378651fd8d617ab3ccbb3289482a0d78.png)

## 解决方案
- 先用v-if把代码包裹起来。

```html
// displayEditContainer默认值是0
<span v-if="displayEditContainer">
 <Editor placeholder="xxxx" class="tinymce_class"   :init="initEdit" v-model="videoDesc" />
 </span>
```

- 在`mounted`，延迟改变`displayEditContainer`的值，实现延迟加载。

```js
...省略...
  mounted () {
      
      // 延迟加载tinymce编辑器
      setTimeout(() => {
        this.displayEditContainer = 1
      }, 1000);
  },
  ...省略...
```
## 参考
- [https://github.com/tinymce/tinymce-angular/issues/76](https://github.com/tinymce/tinymce-angular/issues/76)