@[TOC](目录)
# 前言
- 要实现`以图搜图`主要需以下两个功能：
	- 提取向量：我使用[CLIP](https://huggingface.co/sentence-transformers/clip-ViT-B-32)模型提取图片向量。
    - 根据向量搜索：有许多数据库就自带向量功能的，比如`PostgreSQL`，`Elasticsearch`、`MySQL（MySQL 9开始有向量）`。借助数据库就可以实现。我选用了`PostgreSQL`，更准确地说是`PostgreSQL + pgvector扩展`。


# 前置准备
## PostgreSQL
- 官网地址：[https://www.postgresql.org/](https://www.postgresql.org/)
- Windows 版本下载地址： [https://www.enterprisedb.com/downloads/postgres-postgresql-downloads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) ，如何安装就不赘述了。
## Visual Studio
- Windows编译`pgvector`需要`nmake`命令，需要先安装`Visual Studio`。
- 下载地址：[https://visualstudio.microsoft.com/](https://visualstudio.microsoft.com/)
- 编译`pgvector`至少需要的安装库
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/56ea2b3251f34ff4a400a3c572552ffb.png)
	- C++环境
	- MSVC
	- CRT 
	- Windows 10 SDK （选适应自己系统的）

## pgvector
- 文档和下载地址：[https://github.com/pgvector/pgvector](https://github.com/pgvector/pgvector)

- 要执行的命令（要去`x64 Native Tools Command Prompt for VS [version]`执行）
```bash
git clone git@github.com:pgvector/pgvector.git
git checkout v0.8.1
set "PGROOT=D:\software\PostgreSQL\17"
cd pgvector
nmake /F Makefile.win
nmake /F Makefile.win install
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0e669263eccf4da4bcde843d891f1981.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/083b3de2c1c3441c84aab6ed75305266.png)
## 创建数据库和表
- 创建数据库`vector_sample`

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/34764d5c64f2423e88cdafe547cdd05e.png)

- 启用插件,在`vector_sample`数据库执行
```
CREATE EXTENSION vector;
```

 


# 编写代码
- 我使用Django项目，官方提供的例子地址：[https://github.com/pgvector/pgvector-python](https://github.com/pgvector/pgvector-python)

- 如何创建项目就不赘述了，请参考拙作[创建Django项目](https://sample.blog.csdn.net/article/details/148908539) ，以下是核心代码。

- 创建model
```python
from django.db import models

# Create your models here.

from datetime import datetime
from pgvector.django import VectorField

class Item(models.Model):
    id = models.AutoField(primary_key=True)  # 主键可省略不写
    embedding = VectorField(dimensions=512)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'items'  # 指定数据库表名

```
- 编写接口(GET是查询，POST是保存)
```python
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.models import Item
from app.serializers import ItemSerializer
from sentence_transformers import SentenceTransformer, util
from PIL import Image
from pgvector.django import L2Distance

# Create your views here.


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def vector(request):
    model = SentenceTransformer('clip-ViT-B-32')
    # Encode an image:
    # img_emb = model.encode(Image.open('C:/Users/Administrator/Pictures/sc.png'))
    img_emb = model.encode(Image.open('C:/Users/Administrator/Pictures/Screenshot 2025-09-14 180548.png'))
    print(len(img_emb.tolist()))
    print(img_emb.tolist())
    if request.method == 'GET':
        # result = Item.objects.order_by(L2Distance('embedding', img_emb.tolist()))[:5]
        result = Item.objects.alias(distance=L2Distance('embedding', img_emb.tolist())).filter(distance__lt=2)
        serializer = ItemSerializer(result, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        item = Item(embedding=img_emb.tolist())
        item.save()
        return Response({'message': f'Hello, world! {item.id}'})
    return Response({'message': 'Hello, world!'})


```

- 生成表

```bash
python manage.py makemigrations
python manage.py migrate
```
- 如果无法下载`clip`模型，请设置以下环境变量

```bash
HF_ENDPOINT=https://hf-mirror.com
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0ded3a928e944a0c8b75b7434efc8778.png)

# 验证
- 现今有3条数据
	- `sc.png`是id为1 、2的数据
	- `Screenshot 2025-09-14 180548.png`是id为3的数据

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b641459800bd4c438fd4e0888bf56790.png)
- 我使用GET请求接口查看结果就能知道是否有效。

## 第一次请求
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/886fd641949441edbdc1b3a486204bff.png)
- 结果正确
## 第二次请求
- 更换要搜索的图片，下面注释，上面放开
```python
img_emb = model.encode(Image.open('C:/Users/Administrator/Pictures/sc.png'))
    # img_emb = model.encode(Image.open('C:/Users/Administrator/Pictures/Screenshot 2025-09-14 180548.png'))
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ec18ec8038d24787a952f4dd3984dfa5.png)

- 结果正确



# 源码地址
- 本文例子源码地址： [https://github.com/1030907690/pgvector_sample](https://github.com/1030907690/pgvector_sample)





# 参考
- https://www.cnblogs.com/russellluo/archive/2011/10/15/2212787.html
- https://developercommunity.visualstudio.com/t/cannot-open-include-file-corecrth/8023
- https://stackoverflow.com/questions/21029654/error-c1083-cannot-open-include-file-winsock2-h-no-such-file-or-directory
- https://juejin.cn/post/7337579872746127369
- https://github.com/pgvector/pgvector