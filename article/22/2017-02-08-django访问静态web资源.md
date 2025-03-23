---
layout:					post
title:					"django访问静态web资源"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
使用django访问如html这些页面，或者引入其他东西时就需要配置静态web资源了；

只需要修改urls.py即可

"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from project.views import hello,search,search_post,ajax_post,requests_test,ui
from django.conf import settings

# static files
import os
from django.conf.urls.static import static

urlpatterns = [
    url(r'^hello/', hello),
	url(r'^search/', search),
	url(r'^search_post/', search_post),
	url(r'^ajax_post/', ajax_post),
	url(r'^requests_test/', requests_test),
	url(r'^ui/', ui),
	
]

''' 访问静态web资源配置 start '''
if settings.DEBUG:
	media_root = os.path.join(settings.BASE_DIR,'templates')
	urlpatterns += static('/templates/', document_root=media_root)
''' 访问静态web资源配置 end '''
我的目录结构：


 

访问结果：



也还有其他的方法可以配置，有时间的话可以试试其他的

​