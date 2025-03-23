---
layout:					post
title:					"python3 socket上传文件"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
###一、建立两个进程的TCP连接这里用到了struct库对文件信息进行处理。这里的struct类似于c中的结构体，可以把变量转换成具有c结构体形式的字符串。

```
这是我使用的大致结构
struct{
    char filepath[128]; //文件名
    long long fileSize;  //文件大小
    char pwd[2];  //密码
}
```

服务端代码 socketReceive.py：

```
#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: socketReceive.py
socket service
"""

import re
import socket
import threading
import time
import sys
import os
import struct


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 9000))
        s.listen(10)
    except socket.error as msg:
        print(msg);
        sys.exit(1)
    print('Waiting client connection...');

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr));
    #conn.settimeout(500)
    conn.send(b'Hi, Welcome to the server!')

    while 1:
        fileinfo_size = struct.calcsize('128si2s')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize ,pwd = struct.unpack('128si2s', buf);
            print("pwd : "+ bytes.decode(pwd));
            #删除byte转为str后的\x00  用strip也可以
            newFileName = bytes.decode(filename).rstrip('\x00');
            new_filename = os.path.join('d:/', '' +newFileName);
            print('file new name is {0}, filesize if {1}'.format(new_filename,filesize));

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print('start receiving...');

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print('end receive...');
        conn.close()
        break


if __name__ == '__main__':
    socket_service()
```

客户端代码 socketSend.py：

```
#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: socketSend.py
socket client
"""

import socket
import os
import sys
import struct

'''
字符串和字节互转
'''
def convertStrOrByte():
    # bytes object
    byte = b"example"

    # str object
    str = "example"

    # str to bytes 字符串转字节
    bytes(str, encoding="utf8")

    # bytes to str  字节转字符串
    str(bytes, encoding="utf-8")

    # an alternative method
    # str to bytes  字符串转为字节
    str.encode(str)

    # bytes to str  字节转为字符串
    bytes.decode(bytes)


def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9000))
    except socket.error as msg:
        print(msg);
        sys.exit(1)

    print(s.recv(1024));

    while 1:
        #filepath = input('please input file path: ')
        filepath = "C:/Users/Administrator/Desktop/sort.exe";
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小 2s 代表的是2个字节的字符串长度
            fileinfo_size = struct.calcsize('128si2s')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128si2s', bytes(os.path.basename(filepath).encode('utf-8')),os.stat(filepath).st_size,b'pw');
            s.send(fhead)
            print('client filepath: {0}'.format(filepath))

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print('{0} file send over...'.format(filepath));
                    break
                s.send(data)
        s.close()
        break


if __name__ == '__main__':
    socket_client()
```


运行效果：
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/a2b978b46ff2faf8f326a7cd27bea57d.png)

![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/9fbeec1189a5ade25b25361cd660e790.png)
服务端端是可以一直接受上传请求的。



###二、 改进代码  
  1 、 判定密码是否正确
  2、 有的时候我们上传的文件可能需要放到不同的路径下,可以写个配置。

  全部读取配置，新建一个test.properties文件

```
#密码
pwd=pw  
#sort.exe传到哪个路径
sort.exe=d:/test/
#默认路径
defaultDir=d:/
```
服务端代码：

```
#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: socketReceive.py
socket service
"""

import re
import socket
import threading
import time
import sys
import os
import struct


#读取配置的依赖
import re
import os
import tempfile


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 9000))
        s.listen(10)
    except socket.error as msg:
        print(msg);
        sys.exit(1)
    print('Waiting client connection...');

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr));
    #conn.settimeout(500)
    conn.send(b'Hi, Welcome to the server!')

    while 1:
        fileinfo_size = struct.calcsize('128si2s')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize ,pwd = struct.unpack('128si2s', buf);
            print("pwd : "+ bytes.decode(pwd));
            #判定密码是否正确
            file_path = './test.properties'
            property = Properties(file_path);  # 读取文件
            if property.get("pwd") == bytes.decode(pwd):
                print("password validate success!")
            else:
                print("password validate error")
                break;
            #删除byte转为str后的\x00  用strip也可以
            newFileName = bytes.decode(filename).rstrip('\x00');
            #得到文件路径前缀
            dirPrefix = property.get(newFileName);
            if dirPrefix == None or dirPrefix == "":
                dirPrefix = property.get("defaultDir");
            new_filename = os.path.join(dirPrefix, '' +newFileName);
            print('file new name is {0}, filesize if {1}'.format(new_filename,filesize));

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print('start receiving...');

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print('end receive...');
        conn.close()
        break



'''

zhouzhongqing
2018年5月2日16:17:13
读取properties文件

'''



class Properties:

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception:
            #raise Exception
            print("read file exception ...");
        else:
            fopen.close();

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=''):
        if key in self.properties:
            return self.properties[key]
        return default_value

    def put(self, key, value):
        self.properties[key] = value
        replace_property(self.file_name, key + '=.*', key + '=' + value, True)


def parse(file_name):
    return Properties(file_name)


def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
    tmpfile = tempfile.TemporaryFile()

    if os.path.exists(file_name):
        r_open = open(file_name, 'r')
        pattern = re.compile(r'' + from_regex)
        found = None
        for line in r_open:
            if pattern.search(line) and not line.strip().startswith('#'):
                found = True
                line = re.sub(from_regex, to_str, line)
            tmpfile.write(bytes(line, encoding="utf8"))
        if not found and append_on_not_exists:
            tmpfile.write( bytes('\n' + to_str ,encoding="utf-8"))
        r_open.close()
        tmpfile.seek(0)

        content = tmpfile.read()

        if os.path.exists(file_name):
            os.remove(file_name)

        w_open = open(file_name, 'w')
        w_open.write(str(content,encoding="utf-8"))
        w_open.close()

        tmpfile.close()
    else:
        print("file %s not found" % file_name);



if __name__ == '__main__':
    socket_service()



```



客户端代码：

```
#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: socketSend.py
socket client
"""

import socket
import os
import sys
import struct

'''
字符串和字节互转
'''
def convertStrOrByte():
    # bytes object
    byte = b"example"

    # str object
    str = "example"

    # str to bytes 字符串转字节
    bytes(str, encoding="utf8")

    # bytes to str  字节转字符串
    str(bytes, encoding="utf-8")

    # an alternative method
    # str to bytes  字符串转为字节
    str.encode(str)

    # bytes to str  字节转为字符串
    bytes.decode(bytes)


def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9000))
    except socket.error as msg:
        print(msg);
        sys.exit(1)

    print(s.recv(1024));

    while 1:
        #filepath = input('please input file path: ')
        filepath = "C:/Users/Administrator/Desktop/sort.exe";
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小 2s 代表的是2个字节的字符串长度
            fileinfo_size = struct.calcsize('128si2s')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128si2s', bytes(os.path.basename(filepath).encode('utf-8')),os.stat(filepath).st_size,b'pw');
            s.send(fhead)
            print('client filepath: {0}'.format(filepath))

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print('{0} file send over...'.format(filepath));
                    break
                s.send(data)
        s.close()
        break


if __name__ == '__main__':
    socket_client()
```

当然这里面应该还有很多不完善的地方,有问题的地方希望多多指正。