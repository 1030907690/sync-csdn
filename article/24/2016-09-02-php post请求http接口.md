---
layout:					post
title:					"php post请求http接口"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
这里用的是curl方式,所以要先保证curl函数库开启：在php.ini文件里;extension=php_curl.dll前面的;分号去掉

上代码：

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
//测试无参数
request_post('http://www.baidu.com');
//有参数
$post_data['id']='1';
request_post('http://www.baidu.com',$post_data);

</pre><pre>


​