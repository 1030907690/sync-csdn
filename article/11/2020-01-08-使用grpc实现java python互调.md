---
layout:					post
title:					"使用grpc实现java python互调"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
### 参考资料
- github grpc  [https://github.com/grpc/grpc-java](https://github.com/grpc/grpc-java)  ，[https://github.com/grpc/grpc](https://github.com/grpc/grpc)
- 官方文档 [https://grpc.io/docs](https://grpc.io/docs)

### python grpc
- 所需依赖(可以直接pip安装，文档[https://grpc.io/docs/quickstart/python/](https://grpc.io/docs/quickstart/python/))，代码可以对照参考 [https://github.com/grpc/grpc/tree/master/examples/python/helloworld](https://github.com/grpc/grpc/tree/master/examples/python/helloworld)
	- protobuf
	- grpcio
	- grpcio-tools

- 定义proto文件

```bash
syntax = "proto3";

package com.lyh.app.cartoon.admin.proto;

message Data{
  string text = 1;
}

service DoFormat{
 rpc Text2Upper(Data) returns (Data){}
}
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/708a10609f7d99f0fe32e7b0bf7f83ee.png)

- 生成代码，在proto目录运行  `python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./data.proto`，生成的代码可能导包有问题，可以暂时手动调一下
- 服务端代码service_main.py：

```bash
# -*-coding: UTF-8 -*-

import time
import grpc
from concurrent import futures
from  proceser.proto.data_pb2_grpc import *
from  proceser.proto.data_pb2 import *

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
IP = '50051'

class ServiceMain(DoFormatServicer):
    def Text2Upper(self, request, context):
        txt = request.text
        print('data ' + txt)
        return Data(text=txt.upper())


def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_DoFormatServicer_to_server(ServiceMain(),grpcServer)
    grpcServer.add_insecure_port('[::]:'+IP)
    grpcServer.start()
    print("server start successful")
    try:
       while True:
           time.sleep(_ONE_DAY_IN_SECONDS)
    except Exception as e:
        print(e)
    finally:
        print("finally print")

if __name__ == '__main__':
    serve()
```
- 客户端代码client_main.py

```bash
 # -*-coding: UTF-8 -*-
import grpc
from  proceser.proto.data_pb2_grpc import *
from  proceser.proto.data_pb2 import *
import socket



def get_local_ip():
    local_ip = ""
    try:
        socket_objs = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
        ip_from_ip_port = [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in socket_objs][0][1]
        ip_from_host_name = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]
        local_ip = [l for l in (ip_from_ip_port, ip_from_host_name) if l][0]
    except (Exception) as e:
        print("get_local_ip found exception : %s" % e)
    return local_ip if("" != local_ip and None != local_ip) else socket.gethostbyname(socket.gethostname())

def run():
    '''



    channel = grpc.insecure_channel(get_local_ip()+":50051")
    stub = DoFormatStub(channel=channel)
    response = stub.Text2Upper(Data(text="hello world"))
    print("response %s "   % response.text)
    '''
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = DoFormatStub(channel)
        response = stub.Text2Upper(Data(text="hello world"))
    print("response %s " % response.text)

if __name__ == '__main__':
    run()
```
- 测试调用成功
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2ae49b0b6d4634e98daec4fe1192566e.png)

### java grpc
- 参考github [https://github.com/grpc/grpc-java](https://github.com/grpc/grpc-java) 和教程 [https://grpc.io/docs/tutorials/basic/java/](https://grpc.io/docs/tutorials/basic/java/)

- 加入依赖或者下载jar

```bash
    <!--grpc-->
        <dependency>
            <groupId>io.grpc</groupId>
            <artifactId>grpc-netty-shaded</artifactId>
            <version>1.26.0</version>
        </dependency>
        <dependency>
            <groupId>io.grpc</groupId>
            <artifactId>grpc-protobuf</artifactId>
            <version>1.26.0</version>
        </dependency>
        <dependency>
            <groupId>io.grpc</groupId>
            <artifactId>grpc-stub</artifactId>
            <version>1.26.0</version>
        </dependency>

```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7500bfdec51237770804f2260258a6f7.png)
- 加入生成代码插件

```bash
<build>
  <extensions>
    <extension>
      <groupId>kr.motd.maven</groupId>
      <artifactId>os-maven-plugin</artifactId>
      <version>1.6.2</version>
    </extension>
  </extensions>
  <plugins>
    <plugin>
      <groupId>org.xolstice.maven.plugins</groupId>
      <artifactId>protobuf-maven-plugin</artifactId>
      <version>0.6.1</version>
      <configuration>
        <protocArtifact>com.google.protobuf:protoc:3.11.0:exe:${os.detected.classifier}</protocArtifact>
        <pluginId>grpc-java</pluginId>
        <pluginArtifact>io.grpc:protoc-gen-grpc-java:1.26.0:exe:${os.detected.classifier}</pluginArtifact>
      </configuration>
      <executions>
        <execution>
          <goals>
            <goal>compile</goal>
            <goal>compile-custom</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```
- 我的是maven项目在`src\main`下建立`proto`文件夹，写协议
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ab72b6af4af4771ff31cbd25d2c4658e.png)
- 刷新下maven会增加`protobuf`的插件
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/932a33a7af9b210b73ace4f0624deaf5.png)
- 然后点击这两个生成文件，compile换成package也行
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/11bb2b16e722c900dd3ead25dea6f6b6.png)
- 或者使用`protobuf:compile`和`protobuf:compile-custom`；protobuf:compile生成的文件是与protobuf序列化相关的，也就相当于是数据交换时的java bean，点击protobuf:compile-custom生成的文件是与grpc相关的，主要用于与服务端通信的。
- 运行后会生成这些东西
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c8c02ad75227d27e87a4fac1574cbab5.png)
- 然后写个实现类Text2UpperImpl.java

```bash
package com.lyh.app.cartoon.admin.remote.service;
import com.lyh.app.cartoon.admin.proto.DataOuterClass;
 
import com.lyh.app.cartoon.admin.proto.DoFormatGrpc;
import io.grpc.stub.StreamObserver;
/**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: 调用数据 service
 * @date 2020/1/8 10:35
 */
public class Text2UpperImpl extends DoFormatGrpc.DoFormatImplBase{


    @Override
    public void text2Upper(DataOuterClass.Data request, StreamObserver<DataOuterClass.Data> responseObserver) {
        System.out.println(request.getText());
        String textUpper = request.getText().toUpperCase();
        DataOuterClass.Data data = DataOuterClass.Data.newBuilder().setText(textUpper)
                .build();
        responseObserver.onNext(data);
        responseObserver.onCompleted();
    }
}

```
- 编写服务端GrpcServer.java

```bash
package com.lyh.app.cartoon.admin.remote;

import com.lyh.app.cartoon.admin.remote.service.Text2UpperImpl;
import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;

import java.io.IOException;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

/**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: ${todo}
 * @date 2020/1/8 11:14
 */
public class GrpcServer {
    private static final Logger logger = Logger.getLogger(GrpcServer.class.getName());

    private Server server;

    private void start() throws IOException {
    /* The port on which the server should run */
        int port = 50051;
        server = ServerBuilder.forPort(port)
                .addService(new Text2UpperImpl())
                .build()
                .start();
        logger.info("Server started, listening on " + port);
        Runtime.getRuntime().addShutdownHook(new Thread() {
            @Override
            public void run() {
                // Use stderr here since the logger may have been reset by its JVM shutdown hook.
                System.err.println("*** shutting down gRPC server since JVM is shutting down");
                try {
                    GrpcServer.this.stop();
                } catch (InterruptedException e) {
                    e.printStackTrace(System.err);
                }
                System.err.println("*** server shut down");
            }
        });
    }

    private void stop() throws InterruptedException {
        if (server != null) {
            server.shutdown().awaitTermination(30, TimeUnit.SECONDS);
        }
    }

    /**
     * Await termination on the main thread since the grpc library uses daemon threads.
     */
    private void blockUntilShutdown() throws InterruptedException {
        if (server != null) {
            server.awaitTermination();
        }
    }

    /**
     * Main launches the server from the command line.
     */
    public static void main(String[] args) throws IOException, InterruptedException {
        final GrpcServer server = new GrpcServer();
        server.start();
        server.blockUntilShutdown();
    }


}
```
- 客户端GrpcClient.java

```bash
package com.lyh.app.cartoon.admin.remote;

import com.lyh.app.cartoon.admin.proto.DataOuterClass;
import com.lyh.app.cartoon.admin.proto.DoFormatGrpc;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;

import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * @author Zhou Zhong Qing
 * @Title: ${file_name}
 * @Package ${package_name}
 * @Description: ${todo}
 * @date 2020/1/811:18
 */
public class GrpcClient {
    private static final Logger logger = Logger.getLogger(GrpcClient.class.getName());

    private final ManagedChannel channel;
    private final DoFormatGrpc.DoFormatBlockingStub blockingStub;

    /** Construct client connecting to HelloWorld server at {@code host:port}. */
    public GrpcClient(String host, int port) {
        this(ManagedChannelBuilder.forAddress(host, port)
                // Channels are secure by default (via SSL/TLS). For the example we disable TLS to avoid
                // needing certificates.
                .usePlaintext()
                .build());
    }

    /** Construct client for accessing HelloWorld server using the existing channel. */
    GrpcClient(ManagedChannel channel) {
        this.channel = channel;
        blockingStub = DoFormatGrpc.newBlockingStub(channel);
    }

    public void shutdown() throws InterruptedException {
        channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
    }

    /** Say hello to server. */
    public void greet(String name) {
        logger.info("Will try to greet " + name + " ...");
        DataOuterClass.Data request = DataOuterClass.Data.newBuilder().setText(name).build();
        DataOuterClass.Data response;
        try {
            response = blockingStub.text2Upper(request);
        } catch (StatusRuntimeException e) {
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return;
        }
        logger.info("Greeting: " + response.getText());
    }

    /**
     * Greet server. If provided, the first element of {@code args} is the name to use in the
     * greeting.
     */
    public static void main(String[] args) throws Exception {
        // Access a service running on the local machine on port 50051
        GrpcClient client = new GrpcClient("127.0.0.1", 50051);
        try {
            String user = "Hello world test";
            // Use the arg as the name to greet if provided
            if (args.length > 0) {
                user = args[0];
            }
            client.greet(user);
        } finally {
            client.shutdown();
        }
    }
}
```
- 调用测试
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3500bdc9f5a025c41a6945fba91e41df.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/efde2f656cc8ecf46b4ecfd67cfd61e9.png)

### 互调
- 既然单个的已经调通了，互调也很简单，一个开服务端，一个开客户端；或者一个开客户端，一个开服务端
- java调用python
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/18a1308abcc6eb0a6e52bbb791f729be.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5625143a1874bd2c0591715f28ed3e59.png)

- python调用java
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/391db6d33275aebdda34751bcd8f80e3.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d8f7046e606ed664761bc30f2751ffd1.png)
- 到这里文章已经结束了，本人功底有限，可能文章不正确的地方，希望您能批评指出，感谢您的观看。