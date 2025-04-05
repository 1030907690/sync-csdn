@[TOC](目录)
##  前言
- 普通用户执行某些命令sudo时，要求输入密码就很麻烦，不想直接用`sudo -i`或`-s`切换到root。这时我们就可以去修改`/etc/sudoers`文件。起到不用输密码的效果。
- 下面介绍两种方案。

## 方案一
- 编辑文件
```
sudo vim /etc/sudoers
```

- 在后面加入自己用户名的配置`zzq`是我的用户名，请改成自己的。

```
zzq ALL=(ALL:ALL) NOPASSWD: ALL
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c6a9b05400bc4fe8a9a91adb35593c87.png)
- 保存时用`wq!`强制保存

- 为啥要在后面加呢？因为这个配置会被覆盖。如果放在前面，执行sudo -l的效果如下图。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3802e0e9a0ce43b799905ab58ab2bba6.png)
- 放在后面的效果
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/10090a5582754b839225359d36eb6ec1.png)


## 方案二

- 同样编辑文件
```
sudo vim /etc/sudoers
```

- 找到`%sudo   ALL=(ALL:ALL)  ALL`这行，修改为

```python
%sudo   ALL=(ALL:ALL) NOPASSWD:  ALL
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/00235e01c897492a80f6eb69bc6727cc.png)

- 执行`sudo -l`就能看到效果
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/2c2d3fc4764d4ffd81129e9e1612e8f1.png)

