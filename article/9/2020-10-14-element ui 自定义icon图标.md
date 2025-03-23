---
layout:					post
title:					"element ui 自定义icon图标"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 因为要按照原型图设计实现页面，在element ui自带的图标库好像没有，所以按钮的图标icon需要自定义，原型如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5aa72f0de71e3079f54d57cc36b5b436.png#pic_center)
- 第一步：复制图片到项目内。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d6177c6705bba3c75963f07560785812.png#pic_center)
- 第二步：建立css样式，代码如下所示。

```css
<<style >
 
.el-icon-my-export{
    background: url('~@/assets/image/export.png') center no-repeat;
   /* background-size: cover;*/
}
.el-icon-my-export:before{
    content: "替";
    font-size: 16px;
    visibility: hidden;
}

 
.el-icon-my-export{
    font-size: 16px;
}
.el-icon-my-export:before{
    content: "\e611";
}


 </style>
```
- 第三步：按钮使用自定义的icon。代码如下所示。

```html
  <el-button type="primary" icon="el-icon-my-export" class="interval">导出</el-button>
```
- 最终效果如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9dab74dd6a6522a78ac88f0556e1aec0.png#pic_center)



### 更新于2022年3月1日16:22:13
- 有许多小伙伴评论说效果，我在这里把源码开放出来，以便于大家找问题，实现自己的功能。

```
# 安装依赖
npm install
# 运行
npm run serve

```

- GitHub地址：[https://github.com/1030907690/river](https://github.com/1030907690/river)
- 源码运行效果，地址`http://localhost:8080/targetBehaviorAnalysis`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a1867f3c554b79d6fe159e7c31372afa.png)


