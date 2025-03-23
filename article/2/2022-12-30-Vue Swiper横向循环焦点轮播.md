---
layout:					post
title:					"Vue Swiper横向循环焦点轮播"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)

## 效果
- Swiper横向循环焦点，并且有层叠的效果。如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/59b2dd251c82a036a20c95da643e8b6c.png)
## 代码
- Html
```html
 
      <div class="home_carousel">
        <div ref="swiperRef" class="swiper-container swiper-container-horizontal">
          <div class="swiper-wrapper" style="transition-duration: 300ms; transform: translate3d(-2780px, 0px, 0px);">
            <div class="swiper-slide  "   :index="index"  v-for="index in 12" :key="index">
              <p>增值电信业务经营许可证{{ index }}</p>
            </div>

          </div>
        </div>
   
        <div class="swiper-button-prev"></div>
        <div class="swiper-button-next"></div>
      </div>
```

- JS
```js
 // Import Swiper Vue.js components
import Swiper from "swiper";
export default {
  name: "HomeCarousel",

  data() {
    return {
      swiper: null,
      currentIndex: 0,
    }
  },
  created() { },
  mounted() {
    this.initSwiper()
  },
  methods: {
    initSwiper() {

     let vm = this
      this.swiper =
        new Swiper(this.$refs.swiperRef, {
          watchSlidesProgress: true,
          slidesPerView: 'auto',
          centeredSlides: true,
          loop: true,
          loopedSlides: 5,
        //   autoplay: true,
          navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
          },
          pagination: {
            // el: '.swiper-pagination',
            //clickable :true,
          },
          on: {
            progress: function (progress) {
              for (let i = 0; i < this.slides.length; i++) {
                let slide = this.slides.eq(i);
                let slideProgress = this.slides[i].progress;
                let modify = 1;
                if (Math.abs(slideProgress) > 1) {
                  modify = (Math.abs(slideProgress) - 1) * 0.3 + 1;
                }
                let translate = slideProgress * modify * 260  + 'px';
                let scale = 1 - Math.abs(slideProgress) / 5;
                let zIndex = 999 - Math.abs(Math.round(10 * slideProgress));
                console.log("translate ",translate);
                slide.transform('translateX(' + translate + ') scale(' + scale + ')');
                slide.css('zIndex', zIndex);
                slide.css('opacity', 1);
                if (Math.abs(slideProgress) > 3) {
                  slide.css('opacity', 0);
                }
              }
            },
            slideChangeTransitionEnd: function () {
            //切换结束时，告诉我现在是第几个slide
            vm.currentIndex = this.activeIndex;
            // console.log("slideChangeTransitionEnd  ",vm.currentIndex);
          },
            setTransition: function (transition) {
              for (let i = 0; i < this.slides.length; i++) {
                let slide = this.slides.eq(i)
                slide.transition(transition);
              }

            }
          }

        })

    },
  },
}
```
- CSS
```css
<style lang="css">
@import "swiper/css/swiper.min.css";
</style>
```

```css
   .home_carousel {
            position: relative;
            width: 100%;
            margin: 0 auto;
            padding: 30px 0 30px 0;
            height: 100%;

            .swiper-container {
                width: 100%;
                height: 100%;

                .swiper-slide {
                    position: relative;
                    height: 531px;
                    width: 700px;
                    background: #fff;
                }
    
                .swiper-slide img {
                    display: block;
                }
    
                .swiper-slide p {
                    line-height: 98px;
                    padding-top: 0;
                    text-align: center;
                    color: #636363;
                    font-size: 1.1em;
                    margin: 0;
                }

                .swiper-slide-active{
                    height: 590px;
                    width: 734px;
                    transition: width,height,transform,left,top;
                    transition-duration: .4s;
                }
            }

          

            .swiper-pagination {
                width: 100%;
                bottom: 20px;
            }

            .swiper-pagination-bullets .swiper-pagination-bullet {
                margin: 0 5px;
                border: 3px solid #fff;
                background-color: #d5d5d5;
                width: 10px;
                height: 10px;
                opacity: 1;
            }

            .swiper-pagination-bullets .swiper-pagination-bullet-active {
                border: 3px solid #00aadc;
                background-color: #fff;
            }

            .swiper-button-prev {
                left: -30px;
                width: 45px;
                height: 45px;
                background: url(ae5f692c.png) no-repeat;
                background-position: 0 0;
                background-size: 100%;
            }

            .swiper-button-prev:hover {
                background-position: 0 -46px;
                background-size: 100%
            }

            .swiper-button-next {
                right: -30px;
                width: 45px;
                height: 45px;
                background: url(5b04ba498ca1a80192ae5f692c.png) no-repeat;
                background-position: 0 -93px;
                background-size: 100%;
            }

            .swiper-button-next:hover {
                background-position: 0 -139px;
                background-size: 100%
            }
        }

```

