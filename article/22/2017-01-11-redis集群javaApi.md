---
layout:					post
title:					"redis集群javaApi"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
pom.xml需要这2个包

	
	<!-- https://mvnrepository.com/artifact/redis.clients/jedis -->
	<dependency>
	    <groupId>redis.clients</groupId>
	    <artifactId>jedis</artifactId>
	    <version>2.8.0</version>
	</dependency>
		
	 <!-- https://mvnrepository.com/artifact/net.sourceforge.cobertura/cobertura -->
	<dependency>
	    <groupId>net.sourceforge.cobertura</groupId>
	    <artifactId>cobertura</artifactId>
	    <version>2.0.3</version>
	</dependency>

代码：

import java.io.IOException;
import java.util.HashSet;
import java.util.List;
import java.util.Set;


import redis.clients.jedis.HostAndPort;
import redis.clients.jedis.JedisCluster;

/**
* @ClassName: RedisJava
* @Description: java api 操作例子
* @author zhouzhongqing
* @date 2017年1月10日 下午3:39:48
*
*/ 
public class RedisJava {
	
	/*	List<JedisShardInfo> shards = new ArrayList<JedisShardInfo>();
	JedisShardInfo j = new JedisShardInfo("", 78);
	ShardedJedis shardedJedis = new ShardedJedis(shards );*/
	
	//集群操作
	JedisCluster jedisCluster = null;

	    
	public RedisJava() {
		 // redis节点信息   这里最好写入配置文件
		 Set<HostAndPort> nodes = new HashSet<HostAndPort>();
		 HostAndPort hap1 = new HostAndPort("192.168.16.130", 7000);
		 HostAndPort hap2 = new HostAndPort("192.168.16.130", 7001);
		 HostAndPort hap3 = new HostAndPort("192.168.16.130", 7002);
		 HostAndPort hap4 = new HostAndPort("192.168.16.135", 7003);
		 HostAndPort hap5 = new HostAndPort("192.168.16.135", 7004);
		 HostAndPort hap6 = new HostAndPort("192.168.16.135", 7005);

		 nodes.add(hap1);
		 nodes.add(hap2);
		 nodes.add(hap3);
		 nodes.add(hap4);
		 nodes.add(hap5);
		 nodes.add(hap6);
		 jedisCluster = new JedisCluster(nodes);
	}
	
	
 
	
	/**
	*	<p>函数名称: findByKey</p>
	*	<p>方法描述: 通过key查询</p>
	*	<p>方法调用例子：</p>
	*	<p>完成日期：2017年1月10日</p>
	*	@param @param key
	*	@return void
	*	@throws Exception
	*	@version 1.0
	*/
	private void findByKey(String key) {
		try {//取字符串
			String value = jedisCluster.get(key);
			System.out.println(value);
		} catch (Exception e) {
			try {//取list
				// 取数据，第一个是key，第二个是起始位置，第三个是结束位置，jedis.llen获取长度 -1表示取得所有
				 List<String> values = jedisCluster.lrange(key, 0, -1);
				 System.out.println(values);
			} catch (Exception e2) {
				System.out.println("redis没有这个key");
			}
			
		}
		
		
	}
	
	
	/**
	*	<p>函数名称: findByKey</p>
	*	<p>方法描述: 通过key删除</p>
	*	<p>方法调用例子：</p>
	*	<p>完成日期：2017年1月10日</p>
	*	@param @param key
	*	@return void
	*	@throws Exception
	*	@version 1.0
	*/
	private void deleteByKey(String key) {
		 Long value = jedisCluster.del(key);
		 System.out.println(value);
	}
	
	
	
	
	/**
	*	<p>函数名称: insertObjec</p>
	*	<p>方法描述: 新增</p>
	*	<p>方法调用例子：</p>
	*	<p>完成日期：2017年1月10日</p>
	*	@param @param key
	*	@return void
	*	@throws Exception
	*	@version 1.0
	 * @throws IOException 
	*/
	private void insertObjec() throws IOException {
		Long value = jedisCluster.lpush("testLists", "1","2","3");// k-v存储，v表示的List(队列形式)   //先进先出  
		//或者rpush方法 注意，此处的rpush和lpush是List的操作。是一个双向链表（但从表现来看的
		System.out.println(value);
		if(jedisCluster != null){
			jedisCluster.close();
		}
	}


​