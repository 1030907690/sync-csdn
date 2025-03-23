---
layout:					post
title:					"php curl post请求返回400 bad request"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- php post请求返回400 bad request，代码如下:

```
/**
 * 模拟post进行url请求
 * @param string $url
 * @param array $post_data
 */
function request_post($url = '', $post_data = array()) {//url为必传  如果该地址不需要参数就不传
     if (empty($url)) {
         return false;
     }
     
    if(!empty($post_data)){
     $params = '';
      foreach ( $post_data as $k => $v ) 
      { 
          $params.= "$k=" . urlencode($v). "&" ;
         // $params.= "$k=" . $v. "&" ;
      }
      $params = substr($params,0,-1);
    } 
     $ch = curl_init();//初始化curl
     curl_setopt($ch, CURLOPT_URL,$url);//抓取指定网页
     curl_setopt($ch, CURLOPT_HEADER, 0);//设置header
     curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);//要求结果为字符串且输出到屏幕上
     curl_setopt($ch, CURLOPT_POST, 1);//post提交方式
     if(!empty($post_data))curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
     $data = curl_exec($ch);//运行curl
     curl_close($ch);
     return $data;
}

```
- 在windows上运行正常，在Linux上就一直报400，后来查到是 `curl_setopt($ch, CURLOPT_POST, 1);`这段代码的问题,可能是我的地址不用加请求参数,所以不用加这段代码。有这段代码，如果没有请求参数在Linux上会返回400。
