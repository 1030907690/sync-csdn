---
layout:					post
title:					"vue swiper点击切换slide"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 做轮播挑选了很久最终选择用`swiper` 
- 我用的是swiper 5.4.5，听说新版本对vue2支持不好。
- 找到一个很活跃的库`vue-awesome-swiper`，但是居然宣布过时了。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b06c392900bfabb47b00c2d068de5e18.png)
- 也是踩了很多坑，最终在[https://www.swiper.com.cn/demo/index.html](https://www.swiper.com.cn/demo/index.html)找到例子和实例下载地址。
- 回头一看，例子在github也能下载的。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f3191b7e1502e422121809d78613685d.png)
- 照着例子写了个基础的。



## 效果
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/adc6b83128160e1201a610befae25a49.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6dc4d1784df3a2bcb09c0a73ad7a521c.gif)
## 代码
- 组件`TagTitle.vue`
> 注意：建议封装成组件，写在一个页面的时候，可能是层级太深，我用`el-dialog`套在外面`Swiper`对象初始化不了。我踩的一个坑。

```html
<template>
    
    <div class="container">
        <!-- Swiper -->
        <div class="swiper-container" ref="swiper">
          <div class="swiper-wrapper">
            <div class="swiper-slide" @click="switchSlide(count)" v-for="count in 10 " :key="count" >Slide {{count}}</div>
         
          </div>
          <!-- Add Pagination -->
          <!-- <div class="swiper-pagination" ref="pagination"></div> -->
        </div>
    </div>
  </template>
  <script>
  // Import Swiper Vue.js components
  import Swiper from "swiper";
  // Import Swiper styles
  import "swiper/css/swiper.min.css";
  
  export default {
    name: "TagTitle",
    data() {
      return {
        swiper: null,
      };
    },
    mounted() {
      this.swiper = new Swiper(this.$refs.swiper, {
        slidesPerView: 4,
        spaceBetween: 30,
        centeredSlides: true,
        delay: 3000, 
        paginationClickable: true,


        // pagination: {
        //   el: this.$refs.pagination,
        //   clickable: true,
        // },
      });
    },
    methods: {
        switchSlide(index){
            this.swiper.slideTo(index-1,100)
        },
    },
  };
  </script>
  <style lang="css" scoped>
  
  .swiper-container {
    width: 100%;
    height: 500px;
  }
  .swiper-slide {
    text-align: center;
    font-size: 18px;
    background: #fff;
  
    /* Center slide text vertically */
    display: -webkit-box;
    display: -ms-flexbox;
    display: -webkit-flex;
    display: flex;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    -webkit-justify-content: center;
    justify-content: center;
    -webkit-box-align: center;
    -ms-flex-align: center;
    -webkit-align-items: center;
    align-items: center;
  }
  </style>
```
- 主要就是这个`slideTo`方法，还有从`0`开始。

- 页面使用

```html
 
  <div class="xx">
     <el-dialog
      width="100%"
   ...省略其他属性...
    > 
        <TagTitle></TagTitle>
    </el-dialog>
  </div>
  ...省略引入组件代码...
```
