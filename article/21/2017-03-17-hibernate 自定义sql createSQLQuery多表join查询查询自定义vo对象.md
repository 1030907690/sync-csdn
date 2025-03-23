---
layout:					post
title:					"hibernate 自定义sql createSQLQuery多表join查询查询自定义vo对象"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
由于要做个left join所以要搞个vo对象


LogManageVo.java
里面就写属性和get set方法就可以了

import com.sevnce.log.entity.LogManageDetails;



/**
 * Created by zhouzhongqing on 2017/3/16.
 */
public class LogManageVo extends LogManageDetails{


    /**
     * 操作人id
     * */
    private int usrUserId;

    /**
     * 操作人名称
     * **/
    private String usrUserName;


    /**
     * 操作人动作，操作了哪个模块
     * **/

    private String whatAction;


    /**
     * 记录的操作日志是否为登录,0 登录 1 其他
     * **/
    private int isLogin;

    public int getUsrUserId() {
        return usrUserId;
    }

    public void setUsrUserId(int usrUserId) {
        this.usrUserId = usrUserId;
    }

    public String getUsrUserName() {
        return usrUserName;
    }

    public void setUsrUserName(String usrUserName) {
        this.usrUserName = usrUserName;
    }

    public String getWhatAction() {
        return whatAction;
    }

    public void setWhatAction(String whatAction) {
        this.whatAction = whatAction;
    }

    public int getIsLogin() {
        return isLogin;
    }

    public void setIsLogin(int isLogin) {
        this.isLogin = isLogin;
    }
  String sql = "SELECT lmd.*,lm.usrUserId,lm.usrUserName,lm.whatAction,lm.isLogin from log_manage_details as lmd LEFT JOIN log_manage as lm on  lm.id = lmd.ref_LogManageId ";
        Query query = baseDao.querySql(sql).setResultTransformer(Transformers.aliasToBean(LogManageVo.class));
querySql里面封装的createSQLQuery


重要的是这个方法setResultTransformer，createSQLQuery返回的是数组，如果要转换的bean对象是一个VO或者是POLO对象的话就用这个方法




​