---
layout:					post
title:					"以太坊的geth java api调用"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
###一、准备工作
- 安装了geth客户端,并且能运行起来
- java开发环境

###二、运行geth
- 我这里是Linux ，在geth目录下运行命令:

```
./geth --datadir /home/zzq/app/geth/data  --rpc --rpcaddr 192.168.137.134 --rpcapi "db,eth,net,web3,miner,personal"   console -dev
```
- 需要注意的是我这里指定了ip因为geth我是安装在Linux虚拟机的,代码运行在windows,如果不指定就只能127.0.0.1访问了。具体可参考文档[https://github.com/ethereum/wiki/wiki/JSON-RPC](https://github.com/ethereum/wiki/wiki/JSON-RPC)

###三、Java代码
- 如果是maven项目就好办了,直接写pom(如果不是只能一个个jar下载了)

```
<properties>
		<geth.version>3.2.0</geth.version>
	</properties>
<!-- geth 依赖 -->
		<dependency>
			<groupId>org.web3j</groupId>
			<artifactId>core</artifactId>
			<version>${geth.version}</version>
		</dependency>
		<dependency>
			<groupId>org.web3j</groupId>
			<artifactId>geth</artifactId>
			<version>${geth.version}</version>
		</dependency>


		<dependency>
			<groupId>org.web3j</groupId>
			<artifactId>parity</artifactId>
			<version>${geth.version}</version>
		</dependency>
```

- 测试代码 GethClientServiceImpl.java 

```
package com.rw.article.geth.service.impl;

import com.alibaba.fastjson.JSON;

import com.rw.article.geth.service.IGethClientService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.admin.Admin;
import org.web3j.protocol.admin.methods.response.NewAccountIdentifier;
import org.web3j.protocol.core.Request;

import org.web3j.protocol.core.methods.response.EthBlockNumber;

import org.web3j.protocol.geth.Geth;
import org.web3j.protocol.http.HttpService;
import org.web3j.protocol.parity.Parity;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;

/**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: geth
 * @date 2018/8/2 17:11
 */
 
public class GethClientServiceImpl {

     
    private String gethClientUrl = "http://192.168.137.134:8545";

    //得到当前块高度
    @Override
    public BigInteger getCurrentBlockNumber() {
        Web3j web3j = initWeb3j();
        Request<?, EthBlockNumber> request = web3j.ethBlockNumber();
        try {

            return request.send().getBlockNumber();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return BigInteger.valueOf(0L);
    }

    //新建用户
    @Override
    public String newAccount(String password) {
        Admin admin = initAdmin();
        Request<?, NewAccountIdentifier> request = admin.personalNewAccount(password);
        NewAccountIdentifier result = null;
        try {
            result = request.send();
            return result.getAccountId();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    //全部用户
    @Override
    public String accounts() {
        Parity parity = initParity();
        List<String> ids = new ArrayList<>();
        try {
            ids = parity.personalListAccounts().send().getAccountIds();
            System.out.println("用户数量 : " + ids.size());
        } catch (Exception e) {
            e.printStackTrace();
        }

        return JSON.toJSONString(ids);
    }

    /**
     * 初始化web3j普通api调⽤用
     *
     * @return web3j
     */
    private Parity initParity() {
        return Parity.build(getService());
    }


    /**
     * 初始化web3j普通api调⽤用
     *
     * @return web3j
     */
    private Web3j initWeb3j() {
        return Web3j.build(getService());
    }


    /**
     * 初始化personal级别的操作对象
     *
     * @return Geth
     */
    private Geth initGeth() {
        return Geth.build(getService());
    }

    /**
     * 通过http连接到geth节点
     *
     * @return
     */
    private HttpService getService() {
        return new HttpService(gethClientUrl);
    }


    /**
     * 初始化admin级别操作的对象
     *
     * @return Admin
     */
    private Admin initAdmin() {
        return Admin.build(getService());
    }


    public static void main(String[] args) {
        String accounts = new GethClientServiceImpl().accounts();
        System.out.println(accounts);
    }

}
```
- 这里面只有几个基础的操作(我是直接把service拷贝过来的看起来可能有点别扭,还请勿怪)，其他的可以查阅官方的文档。

到这儿基本结束了，另外文章代码或者我理解有误的地方,希望能批评指出。