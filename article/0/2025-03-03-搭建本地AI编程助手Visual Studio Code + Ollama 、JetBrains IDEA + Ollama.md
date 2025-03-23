---
layout:					post
title:					"搭建本地AI编程助手Visual Studio Code + Ollama 、JetBrains IDEA + Ollama"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 前面[LlamaIndex ollama 搭建本地RAG应用，建立本地知识库](https://sample.blog.csdn.net/article/details/143999694)已经浅尝了一下AI大模型的魅力，本文介绍AI大模型辅助编程，搭建本地AI编程助手。类似于微软Copilot。
- 前后端的开发工具搭建本地AI编程助手都有介绍。
## Visual Studio Code
### 安装插件
- 在扩展中搜索`Continue` ，并安装。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8d991c25bfad472597be0b43258b1a03.png)

### 配置

- 不需要登录，点击`Or, remain local`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/fd28efe82f06477f81a1a13ba901996d.png)
- 根据说明，执行对应的指令。后面绿色的勾表示完成。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5b38eaf0f1274f278184fd3be9fc2799.png)

- 全部完成后，点击`Connect`
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/1ca6c83ab2724150ab54a3a0d50acf02.png)

- 把`Continue`拖动到右侧更方便
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/46364251b93047fc8b0f99d1a071f1be.png)


- 如果再次打开项目发现不见了，要点击右上角这个按钮。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/03fd3787f6db4c379eb7baf93ba260e2.png)


## 验证

### 测试写新代码
- 提出问题`帮我用JS写个冒泡排序`，有结果并且给出了比较详细的解释。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/eb721c66b56e4789abe990c42359cbe4.png)

### 测试修改现有代码

- 首先来看`index.vue`,我想把h2标签里面`XXXX后台管理框架`居中显示。
- 第一步空白处按Ctrl + I打开Edit Mode （如果是在文件中按Ctrl + I，将默认选中该文件，有结果后会反映在该文件中，提示您是否接受修改）
- 第二步选择这个文件。
- 第三步再提问题`帮我把h2标签居中`。
- 按enter键盘，等一会儿就会有修改建议了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5bf00b2437fd4d14b353fb2da8494f50.png)

- 结论是`.home h2 ` 里面加上`text-align: center`即可。经过测试结论正确。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/579e05f24ea84ac0aca1ce6fe1fa3071.png)

## JetBrains IDEA
### 安装插件
- 同样在插件中搜索`Continue` ，并安装。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/7e52b2a280014942b0c01a1a6eb93b7c.png)
- 安装完成后，右侧出现小图标。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/53d50551fd514fa1a84a38ea655d39e3.png)
### 配置
- 与在Visual Studio Code中遇到的界面一样。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0417b359d5a04338958ccaa7c73831de.png)
- 配置不再赘述，点Connect。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3b7f8644c3114f3e8fb776c47913dacb.png)

### 验证

- 全选ctrl + j ,输入问题`帮我删除main函数`。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a443b52a09784204933ef9914f727ae0.png)
- 验证成功



## 其他
- 玩熟练以后，可以直接操作`config.json`文件,替换或新增里面模型等配置。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e69b0ec76b124d178f47c3dfdba6fb19.png)




##  参考

- [https://datawhalechina.github.io/handy-ollama/#/C7/1.%20%E6%90%AD%E5%BB%BA%E6%9C%AC%E5%9C%B0%E7%9A%84%20AI%20Copilot%20%E7%BC%96%E7%A8%8B%E5%8A%A9%E6%89%8B](https://datawhalechina.github.io/handy-ollama/#/C7/1.%20%E6%90%AD%E5%BB%BA%E6%9C%AC%E5%9C%B0%E7%9A%84%20AI%20Copilot%20%E7%BC%96%E7%A8%8B%E5%8A%A9%E6%89%8B)
- [https://www.bilibili.com/video/BV1bJFSeVEJY/](https://www.bilibili.com/video/BV1bJFSeVEJY/)