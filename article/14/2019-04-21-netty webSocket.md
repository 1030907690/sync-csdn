---
layout:					post
title:					"netty webSocket"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 1、导包
pom.xml主要加入
```
    <!--netty-->
        <dependency>
            <groupId>io.netty</groupId>
            <artifactId>netty-all</artifactId>
            <version>4.1.27.Final</version>
        </dependency>
```

- 2、建立服务端
WebSocketServer.java
```
package com.rw.article.chat.websocket;

import com.rw.article.chat.action.ApiController;
import com.rw.article.chat.websocket.handler.BinaryWebSocketFrameHandler;
import com.rw.article.chat.websocket.handler.TextWebSocketHandler;
import com.rw.article.common.constant.Constants;
import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelOption;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.http.HttpObjectAggregator;
import io.netty.handler.codec.http.HttpServerCodec;
import io.netty.handler.codec.http.websocketx.WebSocketServerProtocolHandler;
import io.netty.handler.codec.http.websocketx.extensions.compression.WebSocketServerCompressionHandler;
import io.netty.handler.logging.LogLevel;
import io.netty.handler.logging.LoggingHandler;
import io.netty.handler.stream.ChunkedWriteHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: WebSocket
 * @date 2019/4/16 17:26
 */
public class WebSocketServer {
    private Logger log = LoggerFactory.getLogger(this.getClass()); // 日志对象

    public void main(String[] args) throws InterruptedException {
        EventLoopGroup bossGroup = new NioEventLoopGroup();
        EventLoopGroup workGroup = new NioEventLoopGroup();
        try {
            ServerBootstrap bootstrap = new ServerBootstrap();
            bootstrap.group(bossGroup, workGroup)
                    .option(ChannelOption.SO_BACKLOG, 128)
                    .childOption(ChannelOption.TCP_NODELAY, true)
                    .childOption(ChannelOption.SO_KEEPALIVE, true)
                    .handler(new LoggingHandler(LogLevel.TRACE))
                    .channel(NioServerSocketChannel.class)
                    .childHandler(new ChannelInitializer<SocketChannel>() {
                        @Override
                        protected void initChannel(SocketChannel ch) throws Exception {
                            ch.pipeline()
                                    .addLast(new LoggingHandler(LogLevel.TRACE))
                                    // HttpRequestDecoder和HttpResponseEncoder的一个组合，针对http协议进行编解码
                                    .addLast(new HttpServerCodec())
                                    // 分块向客户端写数据，防止发送大文件时导致内存溢出， channel.write(new ChunkedFile(new File("bigFile.mkv")))
                                    .addLast(new ChunkedWriteHandler())
                                    // 将HttpMessage和HttpContents聚合到一个完成的 FullHttpRequest或FullHttpResponse中,具体是FullHttpRequest对象还是FullHttpResponse对象取决于是请求还是响应
                                    // 需要放到HttpServerCodec这个处理器后面
                                    .addLast(new HttpObjectAggregator(10240))
                                    // webSocket 数据压缩扩展，当添加这个的时候WebSocketServerProtocolHandler的第三个参数需要设置成true
                                    .addLast(new WebSocketServerCompressionHandler())
                                    // 自定义处理器 - 处理 web socket 文本消息
                                    .addLast(new TextWebSocketHandler())
                                    // 自定义处理器 - 处理 web socket 二进制消息
                                    .addLast(new BinaryWebSocketFrameHandler())
                                    // 服务器端向外暴露的 web socket 端点，当客户端传递比较大的对象时，maxFrameSize参数的值需要调大
                                    .addLast(new WebSocketServerProtocolHandler(Constants.DEFAULT_WEB_SOCKET_LINK, null, true, 10485760));

                        }
                    });
            ChannelFuture channelFuture = bootstrap.bind(8092).sync();
            log.info("webSocket server listen on port : [{}]", 8092);
            channelFuture.channel().closeFuture().sync();
        } finally {
            bossGroup.shutdownGracefully();
            workGroup.shutdownGracefully();
        }
    }
}
```
- 2、写handle
  - TextWebSocketHandler.java  文本消息的处理类
  

```
 package com.rw.article.chat.websocket.handler;

import com.alibaba.fastjson.JSON;
import com.fasterxml.jackson.databind.util.BeanUtil;
import com.rw.article.chat.entity.vo.Message;
import com.rw.article.chat.queue.DelayOrderQueueManager;
import com.rw.article.chat.queue.DelayOrderWorker;
import com.rw.article.chat.websocket.OnlineContainer;
import com.rw.article.chat.websocket.protocol.IMsgCode;
import com.rw.article.chat.websocket.protocol.ProcessorContainer;
import com.rw.article.common.configuration.GenericConfiguration;
import com.rw.article.common.constant.Constants;
import com.rw.article.common.spring.BeansUtils;
import com.rw.article.common.type.MessageSendType;
import com.rw.article.common.type.MessageType;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.handler.codec.http.FullHttpRequest;
import io.netty.handler.codec.http.HttpObjectAggregator;
import io.netty.handler.codec.http.websocketx.TextWebSocketFrame;
import io.netty.handler.codec.http.websocketx.WebSocketServerProtocolHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.BeanUtils;

import java.net.InetSocketAddress;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: 文本消息处理
 * @date 2019/4/16 17:29
 */
public class TextWebSocketHandler extends SimpleChannelInboundHandler<TextWebSocketFrame> {
    private Logger log = LoggerFactory.getLogger(this.getClass()); // 日志对象

    private OnlineContainer onlineContainer;


    private BeansUtils beansUtils;

    public TextWebSocketHandler() {
        onlineContainer = BeansUtils.getBean(OnlineContainer.class);
    }

    /*
    经过测试，在 ws 的 uri 后面不能传递参数，不然在 netty 实现 websocket 协议握手的时候会出现断开连接的情况。
   针对这种情况在 websocketHandler 之前做了一层 地址过滤，然后重写
   request 的 uri，并传入下一个管道中，基本上解决了这个问题。
    * */
    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        if (null != msg && msg instanceof FullHttpRequest) {

            FullHttpRequest request = (FullHttpRequest) msg;
            // log.info("调用 channelRead request.uri() [ {} ]", request.uri());
            String uri = request.uri();
            // log.info("Origin [ {} ] [ {} ]", request.headers().get("Origin"), request.headers().get("Host"));
            String origin = request.headers().get("Origin");
            if (null == origin) {
                log.info("origin 为空 ");
                ctx.close();
            } else {
                if (null != uri && uri.contains(Constants.DEFAULT_WEB_SOCKET_LINK) && uri.contains("?")) {
                    String[] uriArray = uri.split("\\?");
                    if (null != uriArray && uriArray.length > 1) {
                        String[] paramsArray = uriArray[1].split("=");
                        if (null != paramsArray && paramsArray.length > 1) {
                            onlineContainer.putAll(paramsArray[1], ctx);          
                        }
                    }
                    request.setUri(Constants.DEFAULT_WEB_SOCKET_LINK);
                }
            } else {
                log.info("不允许 [ {} ] 连接 强制断开", origin);
                ctx.close();
            }

        }
        super.channelRead(ctx, msg);
    }

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, TextWebSocketFrame msg) {
        log.info("接收到客户端的消息:[{}]", msg.text());
        // 如果是向客户端发送文本消息，则需要发送 TextWebSocketFrame 消息
        InetSocketAddress inetSocketAddress = (InetSocketAddress) ctx.channel().remoteAddress();
        String ip = inetSocketAddress.getHostName();
        String txtMsg = "[" + ip + "][" + LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss")) + "] ==> " + msg.text();
        //TODO 这是发给自己
        ctx.channel().writeAndFlush(new TextWebSocketFrame(txtMsg));
   
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
        //移除map
        onlineContainer.removeAll(ctx.channel().id().asLongText());
        ctx.close();
        log.error("服务器发生了异常: [ {} ]", cause);
    }


   

    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        // 添加
        //log.info(" 客户端加入 [ {} ]", ctx.channel().id().asLongText());
        super.channelActive(ctx);
    }

    @Override
    public void channelInactive(ChannelHandlerContext ctx) throws Exception {
        // 移除
        //log.info(" 离线 [ {} ] ", ctx.channel().id().asLongText());


        super.channelInactive(ctx);
        //移除map
        String key = onlineContainer.removeAll(ctx.channel().id().asLongText());
        ctx.close();
    }

}
```
 - BinaryWebSocketFrameHandler.java 二进制消息的处理类  例如发送图片
 

```
package com.rw.article.chat.websocket.handler;

import com.alibaba.fastjson.JSON;
import com.rw.article.chat.service.IFileUploadService;
import com.rw.article.chat.service.impl.AliyunOSSClientServiceImpl;
import com.rw.article.chat.websocket.OnlineContainer;
import com.rw.article.common.configuration.GenericConfiguration;
import com.rw.article.common.constant.Constants;
import com.rw.article.common.spring.BeansUtils;

import io.netty.buffer.ByteBuf;
import io.netty.buffer.ByteBufInputStream;
import io.netty.buffer.Unpooled;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.handler.codec.http.FullHttpRequest;
import io.netty.handler.codec.http.websocketx.BinaryWebSocketFrame;
import org.apache.tomcat.util.http.fileupload.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import sun.misc.BASE64Decoder;

import java.io.*;
import java.sql.Blob;
import java.util.UUID;
import java.util.concurrent.ExecutorService;

/**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: 二进制消息处理
 * @date 2019/4/16 17:30
 */
public class BinaryWebSocketFrameHandler extends SimpleChannelInboundHandler<BinaryWebSocketFrame> {
    private Logger log = LoggerFactory.getLogger(this.getClass()); // 日志对象
 
 
    public BinaryWebSocketFrameHandler() {
      
    }

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
     
        super.channelRead(ctx, msg);
    }

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, BinaryWebSocketFrame msg) throws Exception {
        log.info("服务器接收到二进制消息. [{}]",msg.toString());
        ByteBuf content = msg.content();
        content.markReaderIndex();
        int flag = content.readInt();
        log.info("标志位:[{}]", flag);
        content.resetReaderIndex();

        ByteBuf byteBuf = Unpooled.directBuffer(msg.content().capacity());
        byteBuf.writeBytes(msg.content());

        //转成byte
        byte [] bytes = new byte[msg.content().capacity()];
        byteBuf.readBytes(bytes);
        //byte转ByteBuf
        ByteBuf byteBuf2 = Unpooled.directBuffer(bytes.length);
        byteBuf2.writeBytes(bytes);

      
        log.info("JSON.toJSONString(byteBuf) [ {} ]",JSON.toJSONString(byteBuf));
          //TODO 这是发给自己
        ctx.writeAndFlush(new BinaryWebSocketFrame(byteBuf));


    }




    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        // 添加
        log.info(" 客户端加入 [ {} ]", ctx.channel().id().asLongText());
    }

    @Override
    public void channelInactive(ChannelHandlerContext ctx) throws Exception {
        // 移除
        log.info(" 离线 [ {} ] ", ctx.channel().id().asLongText());
    }
}

```
 - OnlineContainer.java 是用来做存储在线用户的,这个对象存在spring中，通过ApplicationContext获取到,没用spring反正建个单例对象都行。
 

```
 package com.rw.article.chat.websocket;

import io.netty.channel.ChannelHandlerContext;
import lombok.val;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import javax.management.relation.Relation;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: 存储在线ws用户的容器
 * @date 2019/4/16 20:50
 */
@Component
public class OnlineContainer {

    private Logger log = LoggerFactory.getLogger(this.getClass()); // 日志对象
    /**
     * <session,ChannelHandlerContext>
     **/
    private Map<String, ChannelHandlerContext> onlineUserMap = new ConcurrentHashMap<>();

    /**
     * <userId,sessionId>
     **/
    private Map<String, String> userMap = new ConcurrentHashMap<>();


 

    public Map<String, String> getUserMap() {
        return userMap;
    }

    public void setUserMap(Map<String, String> userMap) {
        this.userMap = userMap;
    }

    public Map<String, ChannelHandlerContext> getOnlineUserMap() {
        return onlineUserMap;
    }

    public void setOnlineUserMap(Map<String, ChannelHandlerContext> onlineUserMap) {
        this.onlineUserMap = onlineUserMap;
    }


 

    /***
     * 根据userId得到通道
     * */
    public ChannelHandlerContext getChannelHandlerContextByUserId(String userId) {
        return onlineUserMap.getOrDefault(userMap.getOrDefault(userId, ""), null);
    }

    /***
     * 添加session信息
     * */
    public void putAll(String userId, ChannelHandlerContext ctx) {
        userMap.put(userId, ctx.channel().id().asLongText());
        onlineUserMap.put(ctx.channel().id().asLongText(), ctx);
        log.info("用户 [ {} ] 上线", userId);
    }


    /***
     * 删除session信息
     * */
    public String removeAll(String sessionId) {
        //如果存在则删除
        String key = null;
        if (userMap.containsValue(sessionId)) {

            for (Map.Entry<String, String> entry : userMap.entrySet()) {
                if (null != entry.getValue() && entry.getValue().equals(sessionId)) {
                    key = entry.getKey();
                    break;
                }
            }
            if (null != key) {
                log.info("用户 [ {} ] 离线 ", key);
                userMap.remove(key);
            }
            onlineUserMap.remove(sessionId);
        }
        return key;
    }
}

```
 - BeansUtils.java 主要用来拿spring容器中bean的实例

```
 package com.rw.article.common.spring;

import org.springframework.beans.BeansException;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.lang.Nullable;
import org.springframework.stereotype.Component;


/**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: spring util
 * @date 2018/8/1 17:08
 */
@Component
public class BeansUtils  implements ApplicationContextAware {

    private static ApplicationContext context;

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        BeansUtils.context = applicationContext;
    }

    public static   <T> T getBean(Class<T> bean) {
        return context.getBean(bean);
    }
    public  static  <T> T getBean(String var1, @Nullable Class<T> var2){
        return context.getBean(var1, var2);
    }

    public static   ApplicationContext getContext() {
        return context;
    }

}

```
- Constants.java

```
 /**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: 常量及公共方法
 * @date 2018/8/117:03
 */
public class Constants {

    /** 移除聊天关系 **/
    public static final String REMOVE_CUSTOMER_RELATION = "REMOVE_CUSTOMER_RELATION";

    public static final String DEFAULT_SUCCESS_STRING = "success";


    public static final String DEFAULT_ZERO = "0";

    /** 默认客服前缀**/
    public static final String DEFAULT_CUSTOMER_PREFIX = "tb_";

    /** 默认用户前缀**/
    public static final String DEFAULT_USER_PREFIX = "user_";


    public static final String DEFAULT_WEB_SOCKET_LINK = "/ws";
    }
```

- 3、页面测试这是一个测试websocket的页面
  - chat.html 
 

```
<!DOCTYPE html>
<html  lang="zh-CN" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>web socket 测试</title>
</head>
<body>

<div style="width: 600px;height: 400px;">
    <p>服务器输出:</p>
    <div style="border: 1px solid #CCC;height: 300px;overflow: scroll" id="server-msg-container">

    </div>
    <p>
        <textarea id="inp-msg" style="height: 50px;width: 500px"></textarea><input type="button" value="发送" id="send"><br/>
        选择图片： <input type="file" id="send-pic">
    </p>
</div>

<script type="application/javascript">
    //?userId=tb_1
    var ws = new WebSocket("ws://localhost:8092/ws?userId=tb_1");
    ws.onopen = function (ev) {

    };
    ws.onmessage = function (ev) {
        console.info("onmessage", ev);
        var inpMsg = document.getElementById("server-msg-container");
        if (typeof  ev.data === "string") {
            inpMsg.innerHTML += ev.data + "<br/>";
        } else {
            var result = ev.data;
            var flagReader = new FileReader();
            flagReader.readAsArrayBuffer(result.slice(0, 4));
            flagReader.onload = function (flag) {
                console.log(new DataView(flag.target.result).getInt32(0))
                if (new DataView(flag.target.result).getInt32(0) === 20) {
                    var imageReader = new FileReader();
                    imageReader.readAsDataURL(result.slice(4));
                    imageReader.onload = function (img) {
                        var imgHtml = "<img src='" + img.target.result + "' style='width: 100px;height: 100px;'>";
                        inpMsg.innerHTML += imgHtml.replace("data:application/octet-stream;", "data:image/png;") + "<br />";
                    }
                } else {
                    alert("后端返回的是非图片类型数据，无法显示。");
                }
            }
        }
    };
    ws.onerror = function () {
        var inpMsg = document.getElementById("server-msg-container");
        inpMsg.innerHTML += "发生异常" + "<br/>";
    };
    ws.onclose = function () {
        var inpMsg = document.getElementById("server-msg-container");
        inpMsg.innerHTML += "webSocket 关闭" + "<br/>";
    };

    // 发送文字消息
    document.getElementById("send").addEventListener("click", function () {
        var data = {};
        var text = document.getElementById("inp-msg").value;
        data.text = text;
        data.toUserId = "user_1";
        data.fromUserId = "tb_1";
        ws.send(JSON.stringify(data));
    }, false);

    // 发送图片
    document.querySelector('#send-pic').addEventListener('change', function (ev) {
        var files = this.files;
        if (files && files.length) {
            var file = files[0];
            var fileType = file.type;
            // 表示传递的是 非图片
            var dataType = 20;
            if (!/^image/.test(fileType)) {
                // 表示传递的是 图片
                dataType = 10;
                return;
            }
            var fileReader = new FileReader();

            //base64
            fileReader.readAsDataURL(file);
            fileReader.onload = function (e) {
                console.log(this.result);
                var data = {};
                data.text = this.result;
                data.toUserId = "user_1";
                data.fromUserId = "tb_1";
                ws.send(JSON.stringify(data));

            }
            //Blob对象方式
            /*fileReader.readAsArrayBuffer(file);
            fileReader.onload = function (e) {
                // 获取到文件对象
                var result = e.target.result;
				console.log("result : " +result);
                // 创建一个 4个 字节的数组缓冲区
                var arrayBuffer = new ArrayBuffer(4);
                var dataView = new DataView(arrayBuffer);
                // 从第0个字节开始，写一个 int 类型的数据(dataType)，占4个字节
                dataView.setInt32(0, dataType);
                // 组装成 blob 对象
                var blob = new Blob([arrayBuffer, result]);
				var objectUrl = URL.createObjectURL(blob);
				console.log("objectUrl : " + objectUrl);
                // 发送到 webSocket 服务器端
                ws.send(blob);
            }*/
        }
    }, false);
</script>

</body>
</html>
```
- 发送图片的功能上面两种方式一种是发base64的字符串，一种是Blob对象方式。
- 目前我对netty的还不是很熟悉，如果有错误的地方还望指正。
