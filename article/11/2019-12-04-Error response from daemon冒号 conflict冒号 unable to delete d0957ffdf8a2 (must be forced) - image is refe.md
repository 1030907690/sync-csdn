---
layout:					post
title:					"Error response from daemon: conflict: unable to delete d0957ffdf8a2 (must be forced) - image is refe"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 使用`IMAGE ID`删除镜像报错`Error response from daemon: conflict: unable to delete d0957ffdf8a2 (must be forced) - image is referenced in multiple repositories`是因为有多个镜像的`IMAGE ID`是相同的，可以使用`REPOSITORY+TAG`的方式去删除；如下：

```
root@zzq-HP-Pavilion-15-Notebook-PC:/home/zzq# docker images
REPOSITORY               TAG                 IMAGE ID            CREATED             SIZE
a1030907690/php-ubuntu   14.04               b35f43a8bbb5        28 minutes ago      1.12GB
php-ubuntu14.04          latest              b35f43a8bbb5        28 minutes ago      1.12GB
centos                   7                   5e35e350aded        3 weeks ago         203MB
ubuntu                   latest              775349758637        4 weeks ago         64.2MB
ubuntu                   14.04               2c5e00d77a67        6 months ago        188MB
centos                   6.7                 9f1de3c6ad53        8 months ago        191MB
centos                   6                   d0957ffdf8a2        8 months ago        194MB
centos                   centos6             d0957ffdf8a2        8 months ago        194MB
```
- 这里我centos:6和centos:centos6的`IMAGE ID`是相同的，删除就会报错。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6ec1642ad330115357de5097037c11be.png)
- 解决办法可以用`REPOSITORY+TAG`的方式删除

```
docker rmi centos:centos6
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1aefc29d0f00e0aeea2bcf20ecb3c212.png)
- 再次查看验证是成功的
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3e0b7b6f773c867150abe96722e9832c.png)