---
layout:					post
title:					"element ui 路由配置"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 创建router
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2eae38e40a218d7de03fbd8df0c0ba72.png)
- router/index.js代码如下所示

```javascript
import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
Vue.use(Router)

export default new Router({
  mode: 'history', // 如果不加这段代码，地址中间有#号
  routes: [
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    } 
  ]
})
```

## 修改main.js
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/33257ce23c7896b8abb476aae17f8b9f.png)
- main.js完整代码如下。

```javascript
import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import router from './router'

Vue.use(ElementUI);

new Vue({
  el: '#app', 
  router,
  render: h => h(App)
});
```
## App.vue加入router-view标签
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e25aae53ca509c3f149211fd0efede8b.png)
- App.vue完整代码如下所示。

```javascript
<template>
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
     <router-view></router-view>
  </div>
</template>

<script>
 
export default {
  name: 'App',
  components: {
   
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

```

## 其他
- 需要安装依赖。

```bash
npm install --save vue-route --registry=https://registry.npm.taobao.org
```
