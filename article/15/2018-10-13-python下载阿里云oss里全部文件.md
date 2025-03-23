---
layout:					post
title:					"python下载阿里云oss里全部文件"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 背景:因为要换一个阿里云账号，所以这些文件得下下载下来，转移到那个账号的oss里面去。
- 先替换掉accesskey_id信息等等

```

endpoint = "http://oss-cn-beijing.aliyuncs.com";
accesskey_id = "xx";
accesskey_secret = "xx";
bucket_name = "rw-xxx-xxx";

```
- 安装SDK ，文档地址[https://help.aliyun.com/document_detail/85288.html?spm=a2c4g.11186623.6.745.6b056901JNgvfI](https://help.aliyun.com/document_detail/85288.html?spm=a2c4g.11186623.6.745.6b056901JNgvfI)

```
建议直接使用 pip install oss2 安装
```

- 代码 oss_file.py :

```
# -*- coding: utf-8 -*-

'''

oss 操作

'''
import oss2
import os


endpoint = "http://oss-cn-beijing.aliyuncs.com";
accesskey_id = "xx";
accesskey_secret = "xx";
bucket_name = "rw-xxx-xxx";


#本地文件保存路径前缀
download_local_save_prefix = "C:/Users/Administrator/Desktop/download/";

'''
列举prefix全部文件
'''
def prefix_all_list(bucket,prefix):
    print("开始列举"+prefix+"全部文件");
    oss_file_size = 0;
    for obj in oss2.ObjectIterator(bucket, prefix ='%s/'%prefix):
   
         #print(' key : ' + obj.key)
         oss_file_size = oss_file_size + 1;
         download_to_local(bucket, obj.key, obj.key);

    print(prefix +" file size " + str(oss_file_size));


'''
列举全部的根目录文件夹、文件
'''
def root_directory_list(bucket):
    # 设置Delimiter参数为正斜线（/）。
    for obj in oss2.ObjectIterator(bucket, delimiter='/'):
        # 通过is_prefix方法判断obj是否为文件夹。
        if obj.is_prefix():  # 文件夹
            print('directory: ' + obj.key);
            prefix_all_list(bucket,str(obj.key).strip("/")); #去除/
        else:  # 文件
            print('file: ' + obj.key);
            #下载根目录的单个文件
            download_to_local(bucket, str(obj.key) , str(obj.key));



'''
下载文件到本地
'''
def download_to_local(bucket,object_name,local_file):
    url = download_local_save_prefix + local_file;
    #文件名称
    file_name = url[url.rindex("/")+1:]

    file_path_prefix = url.replace(file_name, "")
    if False == os.path.exists(file_path_prefix):
        os.makedirs(file_path_prefix);
        print("directory don't not makedirs "+  file_path_prefix);

    # 下载OSS文件到本地文件。如果指定的本地文件存在会覆盖，不存在则新建。
    bucket.get_object_to_file(object_name, download_local_save_prefix+local_file);


if __name__ == '__main__':
    print("start \n");
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth(accesskey_id,accesskey_secret)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth,endpoint , bucket_name);
    #单个文件夹下载
    #prefix_all_list(bucket, "newDown");
    root_directory_list(bucket);
    print("end \n");

```

- 调用root_directory_list方法能列举出根目录的所有文件夹和文件,如果是文件直接下载，如果是文件夹再调用prefix_all_list方法列举这个文件夹所有文件。