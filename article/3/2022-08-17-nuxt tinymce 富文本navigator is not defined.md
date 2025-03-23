---
layout:					post
title:					"nuxt tinymce 富文本navigator is not defined"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 用`tinymce`的时候会报navigator is not defined。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/277aa3920cb372417794b9e768df65e4.png)


## 解决方案
- 关闭服务端渲染就能解决。
- 在`plugins`目录新建`tinymce.js`，内容如下。

```js
import Vue from "vue"
import tinymce from "tinymce/tinymce"
import Editor from '@tinymce/tinymce-vue'
Vue.prototype.$tinymce = tinymce
Vue.component("Editor", Editor)

```
- `nuxt.config.js`在`plugins`增加

```js
  {
      src: '@/plugins/tinymce',
      ssr: false,
    },
```

- 界面这样写
```html
  <textarea></textarea>
```

```js
   mounted() {
        // window.tinymce.baseURL = window.location.origin + '/tinymce'
        this.$tinymce.init({
            selector: 'textarea',
            plugins: 'lists link image table code help wordcount image',
            toolbar: 'image',
            toolbar_mode: 'floating',
            tinycomments_mode: 'embedded',
            tinycomments_author: 'Author name',
        });
    }
```

- 当然了，界面也可直接引入组件标签。

```js
        <div>
            <Editor   :init="init" />
        </div>
...省略 部分JS ...
   data() {
        return {
            init: {
                language: 'zh-Hans',   // 这是语言包，可以在https://www.tiny.cloud/get-tiny/language-packages/ 下载
                language_url: '/language/tinymce/zh_CN.js', //下载后放到static目录
                plugins: 'lists link image table code help wordcount image',
                toolbar: 'image',
                images_upload_url: '/api/image/upload',
            }
        }
    },
```
- 把node_modules里`tinymce`模块复制到`static`改名为`_nuxt`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1c27dd5712adf740d96542de8b27e40e.png)
## 效果
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d7dc8f17657c3f3127eb27c7ccaec15c.png)
> css、js都会从本地加载


## 自定义本地资源加载的位置
- 先有`tinymce`模块。
```js
  window.tinymce.baseURL = window.location.origin + '/tinymce'
```
- 我试了下这句写在`tinymce.js`也可以

```js
import Vue from "vue"
import tinymce from "tinymce/tinymce"
import Editor from '@tinymce/tinymce-vue'
window.tinymce.baseURL = window.location.origin + '/_nuxt'
Vue.prototype.$tinymce = tinymce
Vue.component("Editor", Editor)

```

## 参考
- [https://blog.csdn.net/qq_39199892/article/details/103817826](https://blog.csdn.net/qq_39199892/article/details/103817826)