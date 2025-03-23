---
layout:					post
title:					"python用tesseract-ocr做图像识别"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
### 浅谈Tesseract-OCR：
- 光学字符识别(OCR,Optical Character Recognition)是指对文本资料进行扫描，然后对图像文件进行分析处理，获取文字及版面信息的过程。OCR技术非常专业，一般多是印刷、打印行业的从业人员使用，可以快速的将纸质资料转换为电子资料。关于中文OCR，目前国内水平较高的有清华文通、汉王、尚书，其产品各有千秋，价格不菲。国外OCR发展较早，像一些大公司，如IBM、微软、HP等，即使没有推出单独的OCR产品，但是他们的研发团队早已掌握核心技术，将OCR功能植入了自身的软件系统。对于我们程序员来说，一般用不到那么高级的，主要在开发中能够集成基本的OCR功能就可以了。
- Tesseract的OCR引擎最先由HP实验室于1985年开始研发，至1995年时已经成为OCR业内最准确的三款识别引擎之一。然而，HP不久便决定放弃OCR业务，Tesseract也从此尘封。数年以后，HP意识到，与其将Tesseract束之高阁，不如贡献给开源软件业，让其重焕新生－－2005年，Tesseract由美国内华达州信息技术研究所获得，并求诸于Google对Tesseract进行改进、消除Bug、优化工作。Tesseract目前已作为开源项目发布，其项目主页https://github.com/tesseract-ocr/在这里查看，Tesseract是一款支持unicode的OCR引擎，可以识别超过100种语言。它可以被训练识别其他语言。Google将Tesseract用于移动设备，视频和Gmail图像垃圾邮件检测中的文本检测。

###一、准备
- Python库：pytesseract和PIL  （PyTesser是Python的光学字符识别模块。它将图像或图像文件作为输入并输出一个字符串。PyTesser使用Tesseract OCR引擎，将图像转换为可接受的格式，并将Tesseract可执行文件作为外部脚本调用）
- 安装识别引擎tesseract-ocr 下载地址[https://github.com/tesseract-ocr/tesseract/wiki/Downloads](https://github.com/tesseract-ocr/tesseract/wiki/Downloads)

- 数据包下载 ： [https://github.com/tesseract-ocr/tesseract/wiki/Data-Files](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files) tesseract-ocr自带了一些英文的数据包，如果要其他的测试数据需要下载,或者自己训练

我把tesseract-ocr-setup-4.00.00dev.exe和chi_sim.traineddata上传到了csdn，如果不想从GitHub下载也可以从这里下载[https://download.csdn.net/download/baidu_19473529/10293968](https://download.csdn.net/download/baidu_19473529/10293968)

###二、安装
- 注意安装PIL用pip install PIL可能会报错，是因为名字改了用

```
pip install Pillow
```
-  安装pytesseract

```
pip install pytesseract
```
- 安装tesseract-ocr我 的是windows的下载的是最新4.0的

 ![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318163013153%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-TD0S16aA-1732781584171)

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318163021245%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-CaOQnNaR-1732781584172)

安装这个就很简单了，省略.....，然后配置一下环境变量，命令试一下这就可以了。
![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318163232225%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-NT7zyvvq-1732781584172)
如果不配置环境就要到Python35\Lib\site-packages\pytesseract\pytesseract.py这个文件里改下代码

```
tesseract_cmd = 'tesseract'
把这个后面的值改成tesseract.exe的那个安装地址
```

###三、运行程序

图片：
![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318164757442%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-Mh0oQVVW-1732781584172)

代码： ImageConvertText.py

```
# -*- coding: utf-8 -*-

from PIL import Image
import pytesseract


print("-----------------------------------------------------------------------------------------------")
text=pytesseract.image_to_string(Image.open('C:/Users/Administrator/Desktop/eng.png'),lang='chi_sim') #chi_sim是一个解析中文简体的数据包,需要自己下载
print(text);

```

结果：
![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=%2F%2Fimg-blog.csdn.net%2F20180318164838301%3Fwatermark%2F2%2Ftext%2FLy9ibG9nLmNzZG4ubmV0L2JhaWR1XzE5NDczNTI5%2Ffont%2F5a6L5L2T%2Ffontsize%2F400%2Ffill%2FI0JBQkFCMA%3D%3D%2Fdissolve%2F70&pos_id=img-9AhVVg6H-1732781584172)

- 这就是大致的使用流程，当然解析结果还是有些差强人意，这个一般多训练，然后给它矫正，是可以提高正确率的。