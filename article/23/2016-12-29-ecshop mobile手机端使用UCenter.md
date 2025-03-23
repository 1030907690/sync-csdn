---
layout:					post
title:					"ecshop mobile手机端使用UCenter"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
虽然ecshop mobile端并没有设置UCenter整合用户的选项，但是上有对策，下有政策。

我们主要可以修改数据库。ecs_ecsmart_shop_config表这就是配置表

第一步、

把uc_client复制到mobile文件夹下



再修改uc_client/data/cache/apps.php



加入自己新添加的应用

第二步、

在UCenter建立应用（此时是未通信成功的，这个是成功后的样子）



第三步、

改数据库表ecs_ecsmart_shop_config



integrate_code 的值为ucenter

integrate_config 的值 

a:17:{s:5:"uc_id";s:1:"应用id";s:6:"uc_key";s:64:"秘钥";s:6:"uc_url"
;s:32:"UCenter服务端地址";s:5:"uc_ip";s:0:"";s:10:"uc_connect";s:5:"mysql";s:10:"uc_charset";s:5:"utf-8";s:7:"db_host";s:9:"localhost";s:7:"db_user";s:4:"root";s:7:
"db_name";s:6:"discuz";s:7:"db_pass";s:4:"root";s:6:"db_pre";s:15:"discuz_ucenter_";s:10:"db_charset";s:4:"utf8";s:7:"uc_lang";a:2:{s:7:"credits";a:2:{i:0;a:1:{i:0;s:12:"等级积分";}
i:1;a:1:{i:0;s:12:"消费积分";}}s:8:"exchange";s:19:"UCenter积分兑换";}s:13:"cookie_domain";s:0:"";s:11:"cookie_path";s:1:"/";s:10:"tag_number";s:0:"";s:5:"quiet";i:1;}

修改好这些。

第三步、

改lib_common.php大概245行

$out = preg_replace('!s:(\d+):"(.*?)";!se', "'s:'.strlen('$2').':\"$2\";'", $GLOBALS['_CFG']['integrate_config'] );
    $cfg = unserialize($out);
避免unserialize时报错

测试登陆成功


 



​