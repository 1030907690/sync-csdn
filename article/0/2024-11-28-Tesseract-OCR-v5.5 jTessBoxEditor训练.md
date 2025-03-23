---
layout:					post
title:					"Tesseract-OCR-v5.5 jTessBoxEditor训练"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 之前写过[python用tesseract-ocr做图像识别](https://blog.csdn.net/baidu_19473529/article/details/79602028)， 虽然Tesseract-OCR有chi_sim数据集识别中文，但有时不太精准，需要自行矫正，提高准确率。
## 准备

- 下载`chi_sim`相关数据集，注意高版本有新的数据集地址，原文地址 [https://tesseract-ocr.github.io/tessdoc/Data-Files.html](https://tesseract-ocr.github.io/tessdoc/Data-Files.html)。
![](https://i-blog.csdnimg.cn/direct/b1b958e422574bcbbc5b5935657f1154.png)

	- 所以去[https://github.com/tesseract-ocr/tessdata_best](https://github.com/tesseract-ocr/tessdata_best)（Tesseract-OCR高版本下载地址）下载`chi_sim.traineddata`与`chi_sim_vert.traineddata`。
- 配置环境变量`TESSDATA_PREFIX`。指定放置数据集的路径。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5f53ea3cfbc149879bdec6b67b211edf.png)

- 下载[https://sourceforge.net/projects/vietocr/files/jTessBoxEditor/](https://sourceforge.net/projects/vietocr/files/jTessBoxEditor/)。注意使用jTessBoxEditor前要先安装JDK。安装JDK的教程很容易找到就不赘述了。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/61813a8a3ad34e5ea793f2b92d217218.png)
> FX版本我遇到右侧无法预览图像的问题，就没使用它。我用的是jTessBoxEditor-2.6.0.zip。
## 训练前的效果

- 我以下面的图片为例（名称为2.png）。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/50e28f073be944598087a0dd367b3cfe.png)


- 执行命令

```python
tesseract 2.png result -l chi_sim
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/03d4d94b083b4f4b8dcd9542659ab619.png)

- 可以看出有些地方没有空白的地方多了空格。不够精准。

## 开始训练
### 打开jTessBoxEditor设置font
- Settings -> Font，设置为`宋体`，否则中文会乱码。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8d0195261a3f416e9caa21da898a2aea.png)
### 合并TIFF
- 点击Merge TIFF
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c1f2c5fd27d8449a851bce9a463f4c8b.png)


- 选中要训练的图片，可以多选。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0543030e63634add8c6d900f51b7ac3e.png)

- TIFF文件名称规则:
[lang].[fontname].exp[num].tif
例如 自定义字库 addr，字体名test,num为0，那么我们把图片文件命名为 `addr.test.exp0.tif`
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ae0dfbabeb64413fafa038f50954b6e3.png)
### box文件
- 生成box文件
```bash
 tesseract addr.test.exp0.tif addr.test.exp0 -l chi_sim --psm 6 batch.nochop makebox
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/fea081ae10414cf5bbaff73c7474099f.png)
- 打开tif文件
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/90a9ac6bb28e4403997c34053efde064.png)

- ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f8d7a44e285c4afdafc8f1b214e64062.png)

### 矫正
- 从上图可以看出，识别到了但是不太准确，我们来矫正一下。比如第二个字。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c4b8d025e8fd457c8fa658cd25fe95c4.png)
- 矫正后
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/eabecfa3de4e44f7ba62562d19005d86.png)
- 其他的字也是一样的，看字符、坐标、宽高是否正确。不正确就修改。

- 最后效果
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/da8e3d8015614e0caa54b4ce0942b9d6.png)
- 然后保存
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/741434665c1f431a8546d1f01398529e.png)


### 生成font_properties文件

- test 是字体。与前面对应。输入内容 `test 0 0 0 0 0”`表示字体test的粗体、倾斜等共计5个属性
```
echo test 0 0 0 0 0 >font_properties
```
### 生成.tr训练文件

```python
  tesseract addr.test.exp0.tif addr.test.exp0 nobatch box.train
```

### 生成字符集文件

```python
unicharset_extractor addr.test.exp0.box
```

### 生成shape文件

```python
 shapeclustering -F font_properties -U unicharset -O addr.unicharset addr.test.exp0.tr
```


### 生成聚字符特征文件

```python
  mftraining -F font_properties -U unicharset -O addr.unicharset addr.test.exp0.tr
```

### 生成字符正常化特征文件

```python
cntraining addr.test.exp0.tr
```

### 文件重命名
>

将inttemp改为 addr.inttemp
 将  pffmtable 改为addr.pffmtable
将shapetable改为addr.shapetable
将normproto改为 addr.normproto


### 合并训练文件

```python
 combine_tessdata addr.
```


## 验证
### 把traineddata文件放入tessdata目录

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/05933ca23c5f49f99bde17b5961500d9.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f82ae036a800446a8a36792792bf44a5.png)

### 查看效果
- 输入命令

```python
 tesseract 2.png result -l addr
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/15795be0877b42228711b9ffc499a9b6.png)

- 现在效果比之前好很多了。

## 辅助脚本
- 我发现命令实在太多了，所以我写了个脚本。源码地址 [https://github.com/1030907690/public-script/blob/master/machine_vision/tesseract_ocr_train.py](https://github.com/1030907690/public-script/blob/master/machine_vision/tesseract_ocr_train.py)
- 源代码

```python
 # -*- coding: utf-8 -*-

import os

'''

tesseract_ocr_train 训练
'''


def invocation_command(cmd: str):
    print("执行命令 ", cmd)
    os.system(cmd)


if __name__ == '__main__':
    print("请先确认配置好执行Tesseract-OCR命令环境变量和TESSDATA_PREFIX环境变量，默认会读取addr.test.exp0.tif")
    # tif文面命名格式[lang].[fontname].exp[num].tif
    lang = "addr"
    font_name = "test"
    num = "0"

    lang_tmp = input("请输入lang,默认addr ")
    if lang_tmp:
        lang = lang_tmp

    font_name_tmp = input("请输入fontname 默认test")
    if font_name_tmp:
        font_name = font_name_tmp

    num_tmp = input("请输入num，默认0 ")
    if num_tmp:
        num = num_tmp


    tif_name = lang + "." + font_name + ".exp" + num + ".tif"
    name = lang + "." + font_name + ".exp" + num

    print("tif_name ",tif_name)
    input("1、按任意键继续，会生成.box文件")
    cmd = "tesseract " + tif_name + " " + name + " -l chi_sim --psm 6 batch.nochop makebox"
    invocation_command(cmd)
    input("请用jTessBoxEditor打开文件，矫正并保存后按任意键继续")

    print("2、生成font_properties文件")
    invocation_command("echo " + font_name + " 0 0 0 0 0 >font_properties")

    print("3、生成.tr训练文件")
    invocation_command("tesseract " + tif_name + " " + name + " nobatch box.train")

    print("4、生成字符集文件")
    invocation_command("unicharset_extractor " + name + ".box")

    print("5、生成shape文件 ")
    invocation_command("shapeclustering -F font_properties -U unicharset -O " + lang + ".unicharset " + name + ".tr")

    print("6、生成聚字符特征文件")
    invocation_command("mftraining -F font_properties -U unicharset -O " + lang + ".unicharset " + name + ".tr")

    print("7、生成字符正常化特征文件")
    invocation_command("cntraining " + name + ".tr")

    print("8、文件重命名")
    file_list = ["inttemp","pffmtable","shapetable","normproto"]
    for file in file_list:
        if os.path.exists(file):
            rename_file = lang+"."+file
            if os.path.exists(rename_file):
                os.remove(rename_file)
            print("rename ",file +" " + rename_file)
            os.rename(file,rename_file)


    print("9、合并训练文件")
    invocation_command("combine_tessdata "+lang+".")
```







- 如果没有python环境，你是Windows系统就用exe地址 [https://github.com/1030907690/public-script/blob/master/machine_vision/tesseract_ocr_train.exe](https://github.com/1030907690/public-script/blob/master/machine_vision/tesseract_ocr_train.exe)









## 参考

- https://www.cnblogs.com/interdrp/p/15427555.html


























