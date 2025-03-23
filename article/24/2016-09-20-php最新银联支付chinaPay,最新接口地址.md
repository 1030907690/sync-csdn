---
layout:					post
title:					"php最新银联支付chinaPay,最新接口地址"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
需要下载这2个文件 再拿到公钥和秘钥

netpayclient_config.php

netpayclient.php



目录结构 ：



核心代码ChinaPay.php：

<?php

header('Content-type: text/html; charset=gbk');
include_once ("./chinaPay/netpayclient_config.php");
require_once ('./lib/SmartyLoad.php');
//加载 netpayclient 组件
include_once ("./chinaPay/netpayclient.php");
require_once ("./chinaPay/functions.php");

//导入私钥文件, 返回值即为您的商户号，长度15位
$merid = buildKey('D:\fileStore\tzusr\chinapay\MerPrK.key');

if(!$merid) {
    echo "导入私钥文件失败！";
    exit;
}else{
    echo 'success'.$merid.'<br/>';
}


//订单号跟商户号的关系:
//商户提交给ChinaPay的交易订单号，订单号的第五至第九位必须是商户号的最后五位

//生成订单号，定长16位，任意数字组合，一天内不允许重复，必填
$ordid = ecshopsn2chinapaysn(date('Ymd').mt_rand(10000,99999),$merid);
//订单金额，定长12位，以分为单位，不足左补0，必填
$transamt = formatamount(0.01);



//货币代码，3位，境内商户固定为156，表示人民币，必填
$curyid = "156";

//订单日期，本例采用当前日期，必填
$transdate = date('Ymd',time());
//交易类型，0001 表示支付交易，0002 表示退款交易
$transtype = "0001";
//接口版本号，有两个支付版本： 20070129、20040916，客户是808080开头的，就用04版本，必填
$version = "20040916";
//页面返回地址(您服务器上可访问的URL)，最长80位，当用户完成支付后，银行页面会自动跳转到该页面，并POST订单结果信息，可选
$pagereturl = "$site_url/netpayclient_order_feedback.php";
//后台返回地址(您服务器上可访问的URL)，最长80位，当用户完成支付后，我方服务器会POST订单结果信息到该页面，必填
$bgreturl = "$site_url/netpayclient_order_feedback.php";


/************************
 页面返回地址和后台返回地址的区别：
 后台返回从我方服务器发出，不受用户操作和浏览器的影响，从而保证交易结果的送达。
 ************************/

//支付网关号，4位，上线时建议留空，以跳转到银行列表页面由用户自由选择，本示例选用0001农商行网关便于测试，可选
$gateid = "";
//备注，最长60位，交易成功后会原样返回，可用于额外的订单跟踪等，可选
$priv1 = "memo";
//官方手册有两种签名方式:
//04的应该是第二种

//第一种:
//按次序组合订单信息为待签名串
//$plain = $merid . $ordid . $transamt . $curyid . $transdate .$transtype.$priv1;

//生成签名值，必填
//$chkvalue = sign($plain);

//第二种：
//生成签名值，必填

$chkvalue = signOrder($merid,$ordid,$transamt,$curyid,$transdate,$transtype);
echo $merid.'---'.$ordid.'---'.$transamt.'---'.$curyid.'---'.$transdate.'---'.$transtype.'<br/>';



if (!$chkvalue) {
    echo "签名失败！";
    exit;
}else{
    echo '签名成功<br/>';
}



 

/* $arr1 = array('zh', '26');
$arr2 = array('name'=>'zh', 'age'=>26);*/
$smarty->assign('str', '银联支付');//字符串
$smarty->assign('MerId', $merid);//字符串
$smarty->assign('ordid', $ordid);//字符串
$smarty->assign('transamt', $transamt);
$smarty->assign('curyid', $curyid);
$smarty->assign('transdate', $transdate);
$smarty->assign('transtype', $transtype);
$smarty->assign('version', $version);
$smarty->assign('bgreturl', $bgreturl);
$smarty->assign('pagereturl', $pagereturl);
$smarty->assign('gateid', $gateid);
$smarty->assign('priv1', $priv1);
$smarty->assign('chkvalue', $chkvalue);


/* $smarty->assign('num', 6);//数值型
$smarty->assign('arr1', $arr1);//索引数组1
$smarty->assign('arr2', $arr2);//关联数组2 */
$smarty->display('views/home.html'); 
?>

html页面代码home.html

<form action="https://payment.chinapay.com/CTITS/payment/TransGet" method="post" target="_blank">
<label>商户号</label>

<input type="text" name="MerId" value="{$MerId}" />

<label>订单号</label>

<input type="text" name="OrdId" value="{$ordid}" />

<label>订单金额</label>

<input type="text" name="TransAmt" value="{$transamt}" />

<label>货币代码</label>

<input type="text" name="CuryId" value="{$curyid}" />

<label>订单日期</label>

<input type="text" name="TransDate" value="{$transdate}" />

<label>交易类型</label>

<input type="text" name="TransType" value="{$transtype}" />

<label>支付版本号</label>

<input type="text" name="Version" value="{$version}" />

<label>后台返回地址</label>

<input type="text" name="BgRetUrl" value="{$bgreturl}"/>

<label>页面返回地址</label>

<input type="text" name="PageRetUrl" value="{$pagereturl}"/>

<label>网关号</label>

<input type="text" name="GateId" value="{$gateid}"/>

<label>备注</label>

<input type="text" name="Priv1" value="{$priv1}" />

<label>签名值</label>

<input type="text" name="ChkValue" value="{$chkvalue}" />

<input type="submit" value="支付">
</form>
源码下载地址：http://download.csdn.net/download/baidu_19473529/9638415（最新接口地址chinaPay银联支付的例子，修复了金额小数的问题）



​