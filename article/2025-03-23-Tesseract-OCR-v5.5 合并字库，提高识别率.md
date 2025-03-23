---
layout:					post
title:					"Tesseract-OCR-v5.5 合并字库，提高识别率"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---

@[TOC](目录)
## 前言
- 前面已经写了[Tesseract-OCR-v5.5 jTessBoxEditor训练](https://blog.csdn.net/baidu_19473529/article/details/144111835)，训练的基本操作。有时候，我们需要把两次的训练结果合并成一个字库。
- 本文结合上文的图片和另一张图片训练结果合并成一个字库。
![](https://i-blog.csdnimg.cn/direct/50e28f073be944598087a0dd367b3cfe.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9ec1f83ca35c493bb81fb4a24d163b01.png)

## 测试

- 先看看用上篇的`addr.traineddata`识别两张是什么效果。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6c6d83c57161451ca59e5ef9539d6b7b.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e63f5d3b531c4936b5dca5fba752556c.png)
- 结果是正常的，第二张图片识别错误是由于没有训练的原因。下面开始训练。

## 训练新的图片
### 打开jTessBoxEditor设置font
- Settings -> Font，设置为`宋体`，否则中文会乱码。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8d0195261a3f416e9caa21da898a2aea.png)

- 选中要训练的图片，可以多选。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0ba8a6d2a4334756ad0f0ca2e2cfb701.png)
- TIFF文件名称规则:
[lang].[fontname].exp[num].tif
例如 自定义字库 addr2，字体名test,num为0，那么我们把图片文件命名为 `addr2.test.exp0.tif`
### box文件
- 使用上文写好的脚本。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e8326454286641ccb3d97cc3134cc1a4.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0683c747c963438882299104ce4dd1c6.png)
- 打开tif文件
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/90a9ac6bb28e4403997c34053efde064.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b6ee47b88de340bf995ec504a92671cc.png)
### 矫正
- 从上图可以看出，识别到了但是不太准确，我们来矫正一下。矫正后的效果。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b2e6a70be19c4c5a8c135b60fc3e3bfa.png)

- 点击保存。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/cfe6c05677234625980e08428a489cb2.png)
- 回到脚本，输入任意键继续。会得到以下文件。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/93bcec4cbcdb4b1c9ae17e797c385f3f.png)
## 合并
- 创建merge文件夹，把两边的box文件复制进来，执行命令。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b3cbec669b9b468b91c66e103964a959.png)

```python
 unicharset_extractor addr.test.exp0.box addr2.test.exp0.box
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/4c4ff740a4c340e59de83d677dbd874d.png)
- 复制font_properties与tr文件到merge文件夹。执行以下命令。

```python
mftraining -F font_properties -U unicharset -O added.unicharset addr.test.exp0.tr addr2.test.exp0.tr
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/112f560ae4ef43f69616046f8433da87.png)

```python
cntraining addr.test.exp0.tr addr2.test.exp0.tr

```

- 合并所有文件，生成一个大的 .traineddata 字库文件
	- 先修改文件名加上merge。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/57a6ee923d25436bb0b494b803964d9c.png)
- 执行以下命令

```python
combine_tessdata merge.
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/2414f4f3906b4184b9c46ad0c2597c55.png)

- 把`merge.traineddata`放到Tesseract-OCR的tessdata目录中。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6d96d9796c624344826ca2a5bbb657e7.png)
## 验证
- 执行以下命令验证识别结果。

```python
tesseract 2.png result -l merge
tesseract addr2.png result -l merge
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/18b1c96af17a4b7aa6cc95c2ed782e23.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/423df0d951bf4b1f9a82bae8c6241bfe.png)

- 识别结果成功。



## 参考
- https://www.cnblogs.com/interdrp/p/15427555.html
- https://www.cnblogs.com/pyweb/p/11527465.html

