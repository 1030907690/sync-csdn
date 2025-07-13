@[TOC](目录)
# 简介
- Flowable是一个轻量的Java业务流程引擎，用于实现业务流程的管理和自动化。相较于老牌的Activiti做了一些改进和扩展，实现更高的性能和更小的内存占用，支持更多的数据库类型。

# 准备
## JDK
- JDK 17
## MySQL
- flowable程序初始化会生产表，所以要数据库。
- `MySQL` 数据库，我使用的是`phpstudy`（下载地址：[https://www.xp.cn/phpstudy#phpstudy](https://www.xp.cn/phpstudy#phpstudy)）集成环境的`MySQL8.0.12`。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c9ec351587af445983213d2b77d85eb2.png)


## flowable-ui
- 需要事先建一个流程给flowable，所以要个可视化界面创建流程。
- `flowable-ui`：使用docker安装，使用命令：
```shell
 docker run -d --name fu -p 8080:8080 flowable/flowable-ui
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/7dfc5191c16b4a7a85ca37bee16e5c2a.png)
- 运行起来的网页效果，地址是 http://ip:8080/flowable-ui
> 默认帐号密码: `admin`    `test`    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a3c7d1dfe45a4516b2446d047d107354.png)



- 如果拉不下来镜像，请尝试以下方案：
	- 方案一、设置代理，参考拙作[Docker设置代理](https://blog.csdn.net/baidu_19473529/article/details/147011252)
	- 方案二、更换镜像源，如下配置（编辑`/etc/docker/daemon.json`）：
```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io"
  ]
}
```

# 创建流程图
- 实现一个创建采购订单，`order.totalPrice`金额大于1000要经理确认的功能。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/20c3ab1df2de4dbab61fd0898579137f.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e99d1cedf4454c7e9237afba1c4cb68a.png)
- 完整流程图
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/829eea4cd29245bebcb517cdbc548274.png)
## 要注意的地方
- 设置分支条件，`order.totalPrice`大于1000要经理确认。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/541ad54d41ae47759c4c805cea44b950.png)

- 任务要绑定处理类
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/446c558951d24b58ad93bc3d60f9f019.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a01c5d9bf6a6494a871f7f33bfde2096.png)
- 经理确认节点要绑定参数 Assignee `manager`
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/401f065a87d74aa29c0832d9ac268bfd.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ecb5201f86654cbdb0a5c8b3ccd831eb.png)


# 编码

## 依赖和配置
- 引入的包
```xml
		<dependency>
			<groupId>com.baomidou</groupId>
			<artifactId>mybatis-plus-spring-boot3-starter</artifactId>
			<version>3.5.11</version>
		</dependency>
		<!-- 阿里数据库连接池 -->
		<dependency>
			<groupId>com.alibaba</groupId>
			<artifactId>druid-spring-boot-starter</artifactId>
			<version>1.2.23</version>
		</dependency>
		<!-- Mysql驱动包 -->
		<dependency>
			<groupId>mysql</groupId>
			<artifactId>mysql-connector-java</artifactId>
			<version>8.0.33</version>
		</dependency>

		<dependency>
			<groupId>org.flowable</groupId>
			<artifactId>flowable-spring-boot-starter</artifactId>
			<version>7.1.0</version>
		</dependency>
```

- 程序配置文件
```yaml
spring:
  application:
    name: flowable-sample
  profiles:
    active: dev
server:
  port: 8080

# MyBatis配置
mybatis-plus:
  # 搜索指定包别名
  typeAliasesPackage: com.zzq.domain
  # 配置mapper的扫描，找到所有的mapper.xml映射文件
  mapperLocations: classpath*:mapper/**/*Mapper.xml
  # 加载全局的配置文件
  configLocation: classpath:mybatis/mybatis-config.xml

# 日志配置
logging:
  level:
    com.zzq: debug
flowable:
  #  是否激活异步执行器
  async-executor-activate: false
  # 数据库模式更新策略，true表示自动更新数据库模式
  database-schema-update: true

```

- application-dev.yml
```yaml
# 数据源配置
spring:
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource
    driverClassName: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/flowable_sample?nullCatalogMeansCurrent=true&useUnicode=true&characterEncoding=utf8&zeroDateTimeBehavior=convertToNull&useSSL=true&serverTimezone=GMT%2B8
    username: root
    password: root


```

- 下载文件放到项目中`resources/processes`
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/17eebff5bcf04f57922ab6ec9d9288ec.png)
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9308f33a95d3453a870190a109777efd.png)
- FlowableConfig
```
package com.zzq.config;

import org.flowable.spring.SpringProcessEngineConfiguration;
import org.flowable.spring.boot.EngineConfigurationConfigurer;
import org.springframework.context.annotation.Configuration;

/**
 * FlowableConfig
 *
 * @Description: 解决Diagram生成的流程图文字显示为”口口口“ 这是因为本地没有默认的字体，安装字体或者修改配置解决
 * @Author: zzq
 * @Date 2025/4/5 15:16
 * @since 1.0.0
 */
@Configuration
public class FlowableConfig implements EngineConfigurationConfigurer<SpringProcessEngineConfiguration> {

    @Override
    public void configure(SpringProcessEngineConfiguration springProcessEngineConfiguration) {
        springProcessEngineConfiguration.setActivityFontName("宋体");
        springProcessEngineConfiguration.setLabelFontName("宋体");
        springProcessEngineConfiguration.setAnnotationFontName("宋体");
    }
}
```
## 控制器
- OrderFlowController
```java
package com.zzq.controller;

import com.zzq.domain.Order;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletResponse;
import org.apache.commons.io.IOUtils;
import org.flowable.bpmn.model.BpmnModel;
import org.flowable.engine.*;
import org.flowable.engine.history.HistoricActivityInstance;
import org.flowable.engine.history.HistoricActivityInstanceQuery;
import org.flowable.engine.impl.persistence.entity.ProcessDefinitionEntity;
import org.flowable.engine.runtime.Execution;
import org.flowable.engine.runtime.ProcessInstance;
import org.flowable.image.ProcessDiagramGenerator;
import org.flowable.task.api.Task;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.util.FastByteArrayOutputStream;
import org.springframework.web.bind.annotation.*;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.*;

/**
 * Zhou Zhongqing
 * 2025-04-01
 * 订单流程控制器
 */
@RestController
@RequestMapping("/orderFlow")
public class OrderFlowController {

    private static final Logger log = LoggerFactory.getLogger(OrderFlowController.class);

    @Resource
    private HistoryService historyService;

    @Resource
    private RepositoryService repositoryService;

    @Resource
    private RuntimeService runtimeService;

    @Resource
    private TaskService taskService;

    @Resource
    private ProcessEngine processEngine;

    /**
     * 开始流程
     * @param content
     * @param totalPrice
     * @return
     */
    @PostMapping("/create_order")
    public ResponseEntity<String> startFlow(String content, Integer totalPrice) {
        Map<String, Object> map = new HashMap<>();
        map.put("order", new Order(content, totalPrice));
        ProcessInstance processInstance = runtimeService.startProcessInstanceByKey("flowable-sample", map);
        String processId = processInstance.getId();
        log.info("{} 流程实例ID:{} ", processInstance.getProcessDefinitionName(), processId);
        Task task = taskService.createTaskQuery().processInstanceId(processId).active().singleResult();
        taskService.complete(task.getId());
        return ResponseEntity.ok(processId);
    }


    /**
     * 订单列表，待确认的，返回任务id
     * @return
     */
    @RequestMapping("/order_list")
    public String getOrderList() {
        List<Task> list = taskService.createTaskQuery().taskAssignee("manager").list();
        StringBuffer stringBuffer = new StringBuffer();
        list.stream().forEach(task -> stringBuffer.append(task.getId()
                + " : " + runtimeService.getVariable(task.getExecutionId(), "order") + "\n"));
        return stringBuffer.toString();
    }

    /**
     * 经理确认
     * @param taskId
     * @return
     */
    @PostMapping("/confirm/{taskId}")
    public ResponseEntity<String> confirm(@PathVariable String taskId) {
        Task task = taskService.createTaskQuery().taskId(taskId).singleResult();
        HashMap<String, Object> map = new HashMap<>();
        map.put("verified", true);
        taskService.complete(taskId, map);
        return ResponseEntity.ok("success");
    }


    /**
     * 生成图，某个流程处理进度显示
     * @param response
     * @param processId
     * @throws Exception
     */
    @GetMapping(value = "/processDiagram/{processId}")
    public void genProcessDiagram(HttpServletResponse response, @PathVariable("processId") String processId) throws Exception{
        ProcessInstance pi = runtimeService.createProcessInstanceQuery().processInstanceId(processId).singleResult();

        if (null == pi) {
            return;
        }
        Task task = taskService.createTaskQuery().processInstanceId(pi.getId()).singleResult();
        //使用流程实例ID，查询正在执行的执行对象表，返回流程实例对象
        String instanceId = task.getProcessInstanceId();
        List<Execution> executions = runtimeService.createExecutionQuery().processInstanceId(instanceId).list();
        //得到正在执行的Activity的Id
        List<String> activityIds = new ArrayList<>();
        List<String> flows = new ArrayList<>();
        List<HistoricActivityInstance> historyList = historyService.createHistoricActivityInstanceQuery().processInstanceId(processId).orderByHistoricActivityInstanceStartTime().asc().list();
        for (HistoricActivityInstance historicActivityInstance : historyList) {
            String activityId = historicActivityInstance.getActivityId();
            if("sequenceFlow".equals(historicActivityInstance.getActivityType())){
                flows.add(activityId);
            }
        }

        for (Execution exe : executions) {
            List<String> ids = runtimeService.getActiveActivityIds(exe.getId());
            activityIds.addAll(ids);
        }
        // 获取流程图
        BpmnModel bpmnModel = repositoryService.getBpmnModel(pi.getProcessDefinitionId());
        ProcessEngineConfiguration engConf = processEngine.getProcessEngineConfiguration();
        ProcessDiagramGenerator diagramGenerator = engConf.getProcessDiagramGenerator();
        String format = "png";

        InputStream in = diagramGenerator.generateDiagram(bpmnModel, "png", activityIds, flows, engConf.getActivityFontName(), engConf.getLabelFontName(), engConf.getAnnotationFontName(), engConf.getClassLoader(), 1.0, false);
//        OutputStream out = null;
//        byte[] buf = new byte[1024];
//        int legth = 0;
//        try {
//            out = response.getOutputStream();
//            while ((legth = in.read(buf)) != -1) {
//                out.write(buf, 0, legth);
//            }
//        } finally {
//            if (in != null) {
//                in.close();
//            }
//            if (out != null) {
//                out.close();
//            }
//        }



            IOUtils.copy(in, response.getOutputStream());
    }



}

```
## 实体
- Order

```java
package com.zzq.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.io.Serializable;
import java.io.Serial;
@TableName(value = "t_order")
public class Order implements Serializable {

    @Serial
    private static final long serialVersionUID = 8347055723013141158L;


    public Order() {
    }

    public Order(String content, Integer totalPrice) {
        this.content = content;
        this.totalPrice = totalPrice;
    }

    public Order(Integer id, String content, Integer totalPrice) {
        this.id = id;
        this.content = content;
        this.totalPrice = totalPrice;
    }

    @TableId(value = "id",type = IdType.AUTO)
    private Integer id;

    private String content;

    private Integer totalPrice;


    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public Integer getTotalPrice() {
        return totalPrice;
    }

    public void setTotalPrice(Integer totalPrice) {
        this.totalPrice = totalPrice;
    }
}

```

## Flowable任务处理类

- CreateOderProcess
```java
package com.zzq.process;

import org.flowable.engine.delegate.DelegateExecution;
import org.flowable.engine.delegate.JavaDelegate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CreateOderProcess implements JavaDelegate {

    private static final Logger log = LoggerFactory.getLogger(CreateOderProcess.class);

    @Override
    public void execute(DelegateExecution delegateExecution) {
        log.info("订单创建成功 {}",delegateExecution.getVariable("order"));
    }
}

```

- SendMailProcess
```java
package com.zzq.process;

import org.flowable.engine.delegate.DelegateExecution;
import org.flowable.engine.delegate.JavaDelegate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SendMailProcess implements JavaDelegate {
    private static final Logger log = LoggerFactory.getLogger(SendMailProcess.class);

    @Override
    public void execute(DelegateExecution delegateExecution) {
        log.info("发送审核邮件 {} ",delegateExecution.getVariable("order"));
    }
}

```

# 验证
## 启动程序
- 配置了`database-schema-update: true`第一次启动会自动创建表
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/fad2af6117154b84aa70ef262c8cb2f4.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e35b0b5201b74e569bb1b45e24e0bda6.png)

## 调用接口

- 创建采购订单， /orderFlow/create_order ，返回流程实例ID
	- 不需要经理确认
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8a9dde28a74b49e3af7d292ee7e0684d.png)
	- 需要经理确认
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/78ed4329706d4640a212d722486b2254.png)

- 查看待确认的订单，返回任务id拼接Order
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b6d5769db42a4b93b4c9008c1a86e233.png)
- 查看某个流程处理进度显示，传入流程实例id
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5a5d2c0ff6e44796a0603436ea4564c1.png)
- 经理调用确认采购订单，传入taskId
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6b47914e69ee47908301abcafd76cbdb.png)
- 确认后再调用待确认订单接口也就没有刚才的任务id了
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/44a6d8063cbe4057ac6ba11d3df91a3a.png)
- 验证完成


 


#  本文源码
- [https://github.com/1030907690/flowable-sample](https://github.com/1030907690/flowable-sample)

#  参考
- [https://www.bilibili.com/video/BV1gnkJYJEbg/](https://www.bilibili.com/video/BV1gnkJYJEbg/)
- [https://blog.csdn.net/qq_34162294/article/details/143806673](https://blog.csdn.net/qq_34162294/article/details/143806673)
- [https://blog.51cto.com/u_16213663/10188533](https://blog.51cto.com/u_16213663/10188533)
- [https://blog.csdn.net/houyj1986/article/details/85546680](https://blog.csdn.net/houyj1986/article/details/85546680)