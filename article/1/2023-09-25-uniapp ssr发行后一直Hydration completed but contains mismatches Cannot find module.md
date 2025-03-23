---
layout:					post
title:					"uniapp ssr发行后一直Hydration completed but contains mismatches Cannot find module"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---

- 最开始我用前端网页托管的地址访问一直是 Hydration completed but contains mismatches
## 解决方案
- 要从云函数的地址访问项目。
- 先绑定域名，否则用uniapp自带地址访问一直是下载文件
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0f6d89297690cf9bba203e41289f72b9.png)

- 设置路径
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/07b3cd2e0b75f6334b5a008f5acdc4fb.png)

- 最后效果
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f2078a815517d4926f20599ccdbbec26.png)

## uniapp ssr 云函数访问  MODULE_NOT_FOUND:Cannot find module './server/entry-server.js

```
{
"success": false,
"error": {
"code": "FunctionBizError",
"message": "MODULE_NOT_FOUND:Cannot find module './server/entry-server.js'"
}
}
```


- 项目根路径新增 vite.config.ts 文件
```
import {
	defineConfig
} from 'vite'
import uni from '@dcloudio/vite-plugin-uni'
// https://vitejs.dev/config/
export default defineConfig({
	base: 'https://static-xxxx.bspapp.com/', // uniCloud 前端网页托管资源地址（主要是应用编译后的js，图片等静态资源，可以配置为二级目录）
	plugins: [
		uni(),
	],
	ssr: {
		format: 'cjs'
	}
})


```
## 参考
- [https://ask.dcloud.net.cn/question/154591](https://ask.dcloud.net.cn/question/154591)
- [https://uniapp.dcloud.net.cn/tutorial/ssr.html#distribute](https://uniapp.dcloud.net.cn/tutorial/ssr.html#distribute)