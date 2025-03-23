---
layout:					post
title:					"ecshop和UCenter整合后用户注册检测不成功解决方案"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
ecshop和UCenter整合后莫名其妙的



很容易看出来sql语法不对定位到includes/modules/integrates/integrate.php看代码



原因就是$this->field_mobile_phone未被赋值为空。想过直接赋值

但都不是最终的解决办法，于是乎开始对这个$user对象感兴趣了，找了下资料，大致如下

ecshop的程序中，有个对象：$user，它就是用来处理用户信息的。 
比如登陆，注册，还有就是用来和第三方管理通讯和共享资源的。
在user.php中，有一条$user->check_mobile_phone($username, $password)。 
这里的$user 是来自includes/init.php中的   $user = & init_users(); 
而inti_user函数又在lib_common.php中，他里面有一段非常经典的代码。
    include_once(ROOT_PATH . 'includes/modules/integrates/' . $GLOBALS['_CFG']['integrate_code'] . '.php'); 
    $cfg = unserialize($GLOBALS['_CFG']['integrate_config']); 
    $cls = new $GLOBALS['_CFG']['integrate_code']($cfg);
默认情况下 $GLOBALS['_CFG']['integrate_code'] 的值为： ecshop 
这是在 /includes/lib_common.php 文件的 function load_config()函数中定义的：
if (empty($arr['integrate_code'])) 
{ 
    $arr['integrate_code'] = 'ecshop'; // 默认的会员整合插件为 ecshop 
}
默认情况下，调用的会员整合插件是ecshop。 
那么这包含的文件就是：'includes/modules/integrates/ecshop.php', 
打开ecshop.php这个文件，你会发现它继承了'includes/modules/integrates/integrate.php'. 
integrate.php里面有很多的方法：login()登陆，edit_user()编辑用户资料，add_user()注册用户。 
使用各自系统整合时，就需要重写 integrate 基类，然后调用这个重写后的类。

我找到了lib_common.php的& init_users();方法把 $GLOBALS['_CFG']['integrate_code'] 打印了日志出来



惊奇的发现他居然调用的是ucenter.php文件，我打开文件查看他的带参构造方法



这里可以看到没有给$this->field_mobile_phone赋值的

那现在手动加上





现在就成功了，估计是兼容的问题，我的ucenter.php版本低了吧。

​