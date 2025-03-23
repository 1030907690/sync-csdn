---
layout:					post
title:					"ecshop和discuz的同步登陆和退出"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
第一步、将uc_client复制到ecshop根目录

      



第二步、安装Ucenter

  

点击安装、





需要注意的是你的Ucenter数据库要是本地的数据库，如果你不是本地的数据库需要改代码通信不成功。



这样就成功通信了。

但是据我测试同步登陆和同步退出还是有bug。

需要改ecshop和discuz 具体代码

第一步、

         打开discuz目录下source\plugin\myrepeats\switch.inc.php文件，找到$ucsynlogin = $_G['setting']['allowsynlogin'] ? uc_user_synlogin($_G['uid']) : '';
这一句，将其修改为$ucsynlogin = uc_user_synlogin($_G['uid']);（不做判断，强行指定）。

        

第二步、

打开discuz目录下source\class\class_member.php文件,该文件需要有三处修改。

    1、在大约35行找到$ucsynlogin = $this->setting['allowsynlogin'] ? uc_user_synlogin($_G['uid']) : '';这一句，将其修改为$ucsynlogin =uc_user_synlogin($_G['uid']);（不做判断，强行指定。）；

    2、在大约142行找到$ucsynlogin = $this->setting['allowsynlogin'] ? uc_user_synlogin($_G['uid']) : ''这一句，将其修改为$ucsynlogin = uc_user_synlogin($_G['uid']);（不做判断，强行指定）。[是的，上面两句完全一样]。

   3、在大约找到318行找到$ucsynlogout = $this->setting['allowsynlogin'] ? uc_user_synlogout() : ''，将其修改为$ucsynlogout = uc_user_synlogout();

第三步、

打开ecshop安装目录下includes\modules\integrates\ucenter.php文件，找到函数logout()方法

    function logout() //（大约190行）：
    {
        $this->set_cookie();  //清除cookie
        $this->set_session(); //清除session
        $this->ucdata = uc_call("uc_user_synlogout");   //同步退出
        return true;
    }                                
将$this->ucdata = uc_call("uc_user_synlogout")这一句改为$this->ucdata = uc_call("uc_user_synlogout",array("0"));  //同步退出

第四步、

分别打开discuz与ecshop应用下的uc_client\data\cache目录下的apps.php文件，结果发现两个文件有所不同。其中一个中的文件少了一个应用的配置。可以手动把缺少

应用配置的那个文件填写完整后保存即可。

到此配置完毕，同步登陆和退出就完美了。



​