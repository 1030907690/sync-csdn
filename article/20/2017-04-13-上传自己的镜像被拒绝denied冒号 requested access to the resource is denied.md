---
layout:					post
title:					"上传自己的镜像被拒绝denied: requested access to the resource is denied"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
我登录后想要上传自己保持的镜像。

[zzq@weekend110 ~]$ docker images
REPOSITORY           TAG                 IMAGE ID            CREATED             SIZE
a1030907690/ubuntu   latest              938aec5e0cbb        41 hours ago        550 MB
0ef2e08ed3fa         latest              3bd2787b9fa3        3 days ago          550 MB
<none>               <none>              1fce756b350f        3 days ago          130 MB
tomcat               latest              2698323ee8ec        9 days ago          357 MB
ubuntu               latest              0ef2e08ed3fa        6 weeks ago         130 MB
zzq/ubuntu           test                0ef2e08ed3fa        6 weeks ago         130 MB
hello-world          latest              48b5124b2768        2 months ago        1.84 kB
[zzq@weekend110 ~]$ docker push 0ef2e08ed3fa
The push refers to a repository [docker.io/library/0ef2e08ed3fa]
cbec076ebdd0: Preparing 
d8332256f30e: Preparing 
6f2ac32dce2a: Preparing 
f7cf0e41c38b: Preparing 
9377ea912b09: Preparing 
00ae4d242ea6: Waiting 
dbbd2c11cefa: Waiting 
56827159aa8b: Waiting 
440e02c3dcde: Waiting 
29660d0e5bb2: Waiting 
85782553e37a: Waiting 
745f5be9952c: Waiting 
denied: requested access to the resource is denied


报了denied: requested access to the resource is denied异常

需要使用 docker tag改名字

docker tag 3bd2787b9fa3 a1030907690/ubuntu:latest
上面的信息显示是拒接访问，因为tag的名字斜线前面部分a1030907690不是本人的用户名，下面把它修改为a1030907690/xxxxx就push成功。需要注意的是a1030907690是本人的docker用户名。进入docker hub网站查看，发现多了一个公共的repository。

[zzq@weekend110 ~]$ docker push a1030907690/ubuntu
把名字提交成这样的格式就成功了


 



​