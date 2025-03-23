---
layout:					post
title:					"Python爬虫(3),Python3.x"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request;
#中文注释

def load_page(url):
	'''
	发送URL请求
	'''
 	 
	user_agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;";
	headers = {'User-Agent':user_agent};	
	req = urllib.request.Request(url,headers=headers);
	response = urllib.request.urlopen(req);
	html =str(response.read(),'utf-8')
	#html = response.read();  这代码出现一种byte字节　　详见　http://www.zhihu.com/question/27062410
	print('loading...baidu');
	return html;


def write_to_file(file_name,txt):
	'''
		讲txt文本存入到file_name文件中
	'''
	print("正在存储文件"+str(file_name));
	#1 打开文件
	#w 如果没有这个文件将创建这个文件
	f = open(file_name,'w',encoding='utf-8');
	#2 读写文件
	f.write(str(txt));
	#3 关闭文件
	f.close();
	
	
def tieba_spider(url,begin_page,end_page):
	'''
		贴吧爬虫定义的方法
	'''
	 
	for i in range(int(begin_page) ,int(end_page)+1):	
		pn = 50 * (i - 1 );
		#组成地址
		my_url = url + str(pn);
		print("请求的地址"+str(my_url));
		html = load_page(my_url);
		print("=========第 %d 页=========" %(i));
		#print(html);
		print("=================");
		file_name = str(i) +".html";
		write_to_file(file_name,html);


#main
if __name__=="__main__":
	url = input("请输入url地址");
	print(url);
	begin_page = input("请输入起始页码");
	end_page = input("请输入终止页码");
	#print(begin_page);
	#print(end_page);
	tieba_spider(url,begin_page,end_page);
以地址lol贴吧为例：

url地址

http://tieba.baidu.com/f?kw=lol&ie=utf-8&pn=0

​