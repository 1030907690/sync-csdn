@[TOC](目录)
# 前言
- 之前写过[安装scrcpy-client模块av模块异常，环境问题解决方案](https://blog.csdn.net/baidu_19473529/article/details/143442416)，近期有人告诉此方案无效了，我再次尝试确实如此。本篇再来解决这个问题。


# 解决步骤
- 先创建出新的环境
```shell
conda create -n  scrcpy-test python=3.10.13
```
- 如果进入` scrcpy-test`直接安装会`av`模块报错
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/2014bc2c47884195ac56259cb14544f1.png)

## 手动加模块
 咱们换个思路，先安装`av`模块
```
pip install av
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5c68efabcedd4597b1d17385d0b3f5bc.png)

- 下载[https://github.com/leng-yue/py-scrcpy-client](https://github.com/leng-yue/py-scrcpy-client)源码。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/98ef1fbefc5a42909750fc258ab22bdd.png)
- 把`scrcpy`文件夹复制到`conda` `envs/scrcpy-test/Lib/site-packages`里面
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/88740ad0c6c94d2d801679ba3343906a.png)
- 安装`adbutils`
```
pip install adbutils
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a0655eb04c9944caa76fdb20c3cd3fc4.png)


# 验证

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/056bedf54a404ac1a2c82d21340c47e2.png)





#  参考
- [https://github.com/leng-yue/py-scrcpy-client/issues/91](https://github.com/leng-yue/py-scrcpy-client/issues/91)