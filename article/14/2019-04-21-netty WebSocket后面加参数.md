---
layout:					post
title:					"netty WebSocket后面加参数"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 依赖于Tomcat的webSocket地址后面是可以随便跟参数的,但是发现netty WebSocket却不能加参数，代码如下:
- WebSocketServer.java

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
                                           // 服务器端向外暴露的 web socket 端点，当客户端传递比较大的对象时，maxFrameSize参数的值需要调大
                                    .addLast(new WebSocketServerProtocolHandler(Constants.DEFAULT_WEB_SOCKET_LINK, null, true, 10485760))
                                            // 自定义处理器 - 处理 web socket 文本消息
                                    .addLast(new TextWebSocketHandler())
                                    // 自定义处理器 - 处理 web socket 二进制消息
                                    .addLast(new BinaryWebSocketFrameHandler());
                            
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
- 网上搜索了下说是要重写uri,然后我自己debug了程序发现调用了WebSocketServerProtocolHandler#channelRead方法,我可以从msg中拿到uri并重写，但是发现不行，后面我把handler的执行顺序改了下就可以了。
- WebSocketServer.java的更改

```
   // 自定义处理器 - 处理 web socket 文本消息
  .addLast(new TextWebSocketHandler())
   // 自定义处理器 - 处理 web socket 二进制消息
 .addLast(new BinaryWebSocketFrameHandler())
  // 服务器端向外暴露的 web socket 端点，当客户端传递比较大的对象时，maxFrameSize参数的值需要调大
  .addLast(new WebSocketServerProtocolHandler(Constants.DEFAULT_WEB_SOCKET_LINK, null, true, 10485760));
```
- 然后我在TextWebSocketHandler重写uri
 TextWebSocketHandler.java
 

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
- 全部代码可参考[netty webSocket](https://blog.csdn.net/baidu_19473529/article/details/89442189)