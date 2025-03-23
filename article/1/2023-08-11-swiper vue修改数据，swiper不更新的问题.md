---
layout:					post
title:					"swiper vue修改数据，swiper不更新的问题"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- swiper第一次初始化的时候正常，但是当我改变源数据时，要么就是不能把数据显示完，要么就是没有翻页。尝试过重新赋值swiper，但是依旧没有解决，后面找到下面的方案，测试能够解决我的问题。

- 解决方案，增加监听的配置。

```js

  initSwiper() {
		// 这是我的源数据
      const length = this.liveListProp ? this.liveListProp.length : 0
      
    const group =  length % this.slidesPerViewProp == 0
            ? length / this.slidesPerViewProp
            : length / this.slidesPerViewProp + 1
            console.log("group ",group);
      this.swiper = new Swiper(this.$refs.discoverLiveListRef, {
        slidesPerView: this.slidesPerViewProp,
        spaceBetween: 15,
        slidesPerGroup:group,
        loop: false,
        loopFillGroupWithBlank: true,
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
	
		// 这2段代码起作用
        observer:true,  //修改swiper自己或子元素时，自动初始化swiper
        observeParents:true,  //修改swiper的父元素时，自动初始化swiper
      });
    },
 
```
