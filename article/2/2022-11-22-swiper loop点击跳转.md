---
layout:					post
title:					"swiper loop点击跳转"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- swiper加入`loop=true`各种千奇百怪的问题，找了很久找到解决方案。
- 代码

```
  initSwiper() {
      let vm = this;

      this.swiper = new Swiper(this.$refs.swiperContainerRef, {
        loop: true,
        speed: 2500,
        slidesPerView: 8,
        spaceBetween: 0,
        centeredSlides: true,
        watchSlidesProgress: true, 
        slideToClickedSlide: true, // 点击切换到指定slide
       

        on: {
          slideChangeTransitionEnd: function () {
            //切换结束时，告诉我现在是第几个slide
            vm.currentIndex = this.activeIndex;
            // console.log("slideChangeTransitionEnd  ",vm.currentIndex);
          },
          slideChange: function () {
 
          },
          click: function () {
          
          },

          onSlideChangeEnd: function () {
        
          },
        },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      });

 
       
    },
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/98560a814797219a964ca89fe7040439.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/93bc26664bfcea385be07684aca3d83f.gif)
