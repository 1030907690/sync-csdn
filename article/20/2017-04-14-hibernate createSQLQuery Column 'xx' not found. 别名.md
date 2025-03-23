---
layout:					post
title:					"hibernate createSQLQuery Column 'xx' not found. 别名"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
hibernate使用原生sql别名报错

SQLQuery query = baseDao.getByRealSqlData("select telphone  as count from address  limit 0,?");
		query.setParameter(0, 3);
		query.setResultTransformer(Transformers.aliasToBean(AddressVo.class));  
		List<AddressVo> vo = query.list();
		for (AddressVo addressVo : vo) {
			System.out.println(addressVo);
		}


里面封装的是createSQLQuery 方法

解决办法：

改变数据库连接地址：jdbc:mysql://127.0.0.1:3306/cts5_ygg?useUnicode=true&amp;characterEncoding=UTF-8&amp;useOldAliasMetadataBehavior=true 

然后就支持as了

​