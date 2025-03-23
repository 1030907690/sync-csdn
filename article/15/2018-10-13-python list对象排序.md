---
layout:					post
title:					"python list对象排序"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- python list对象排序主要使用sort函数。

```
list.sort(key=None,reverse=False)
```

- 由于list.sort()函数在排序时，使用的是小于号对比，所以自定义的对象类型需要override __lt__(小于)函数才能实现排序。

- 代码如下:
- 1、新建一个对象 PythonFile,这里是根据number属性排序。

```
class PythonFile:
    def __init__(self, name, path,number):
        self.name = name;
        self.path = path;
        self.number = number;

    def getName(self):
        return self.name;

    def getPath(self):
        return self.path;


    def getNumber(self):
        return self.number;

    def __lt__(self, other):  # override <操作符
        if self.number < other.number:
            return True
        return False

```
- 然后下面main方法调用(注意下代码缩进排版等):

```
if __name__ == '__main__':
     pythonFileList = [];
     pythonFile1 = PythonFile("py_1.py", "./py_1.py", 1);
     pythonFile2 = PythonFile("py_2.py", "./py_2.py", 2);
	 pythonFileList.append(pythonFile1);
	 pythonFileList.append(pythonFile2);	
     #排序 这里默认是升序排序
     pythonFileList.sort();
     #这是降序
     #pythonFileList.sort(reverse=True);
     
	for item in pythonFileList:
		print(item.getName() + "----" + str(item.getNumber()));
```

- 执行结果:

```
py_1.py----1
py_2.py----2
```
