---
layout:					post
title:					"git push异常No refs in common and none specified; doing nothing. Perhaps you should specify a branch"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- git push异常具体如下（一般发生在首次推送）:

```
No refs in common and none specified; doing nothing. Perhaps you should specify a branch such as 'master'
```
- 翻译过来就是没有指定推送到哪个分支里去。
- 解决方案:使用`git push origin master` 可以指定推送该远程库的主分支去。