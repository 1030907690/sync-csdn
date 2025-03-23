---
layout:					post
title:					"git提交项目npm run lint异常"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 具体异常，应该是触发了代码检查的机制

```java
0 files committed, 1 file failed to commit: 注册页面 > @ precommit D:\work\company\HaoJing\xxx > npm run lint > @ lint D:\work\company\HaoJing\xxx > eslint --ext .js src test Oops! Something went wrong! :( ESLint couldn't find a configuration file. To set up a configuration file for this project, please run: eslint --init ESLint looked for configuration files in D:\work\company\HaoJing\xxx\src\apiPlat\components and its ancestors. If you think you already have a configuration file or if you need more help, please stop by the ESLint chat room: https://gitter.im/eslint/eslint npm ERR! code ELIFECYCLE npm ERR! errno 1 npm ERR! @ lint: `eslint --ext .js src test` npm ERR! Exit status 1 npm ERR! npm ERR! Failed at the @ lint script. npm ERR! This is probably not a problem with npm. There is likely additional logging output above. npm ERR! A complete log of this run can be found in: npm ERR! C:\Users\Administrator\AppData\Roaming\npm-cache\_logs\2020-06-30T06_12_11_295Z-debug.log npm ERR! code ELIFECYCLE npm ERR! errno 1 npm ERR! @ precommit: `npm run lint` npm ERR! Exit status 1 npm ERR! npm ERR! Failed at the @ precommit script. npm ERR! This is probably not a problem with npm. There is likely additional logging output above. npm ERR! A complete log of this run can be found in: npm ERR! C:\Users\Administrator\AppData\Roaming\npm-cache\_logs\2020-06-30T06_12_11_311Z-debug.log husky - pre-commit hook failed (add --no-verify to bypass)
```
- 解决办法，安装依赖

```java
npm install --save-dev pre-commit
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cf56fa0d51d76f2429a12c0064f1d5b6.png)
- 再次commit成功
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f641fde9bd3de1ff1ef2909323db2e3f.png)