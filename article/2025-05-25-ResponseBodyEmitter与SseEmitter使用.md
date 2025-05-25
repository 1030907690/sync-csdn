@[TOC](目录)
# 背景
- 最近在接入阿里云百炼AI助手时，接触到`ResponseBodyEmitter`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e118643b0d6747be8b6b85c6ae412630.png)![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d39a4a4d16b14b05abd16484454ebd7a.png)
- 实现了流式返回，比较感兴趣，所以去了解了一下如何实现。

# ResponseBodyEmitter
## 简介
- Spring 框架提供的通用流式传输接口，支持分块传输编码（Chunked Encoding），允许逐步向客户端发送数据块，异步推送数据，而非一次性响应。返回ResponseBodyEmitter灵活性强，也可以自己构造标准的SSE返回。

## 核心代码实现
###  后端代码
```java

    private final ExecutorService executorService = Executors.newFixedThreadPool(2000);

    private final List<String> replyData = Arrays.asList("我是", "您的AI助手", "有什么可以帮您", "我是", "您的AI助手", "有什么可以帮您");
    /**
     * 返回ResponseBodyEmitter灵活性强，也可以自己构造标准的SSE返回
     * @param response
     * @return
     */
    @RequestMapping(value = "/responseBodyEmitter")
    @CrossOrigin
    public ResponseBodyEmitter responseBodyEmitter(HttpServletResponse response) {
        ResponseBodyEmitter emitter = new ResponseBodyEmitter(180000L);
        executorService.execute(() -> {
            try {
                for (String value : replyData) {
                    emitter.send(value.getBytes(java.nio.charset.StandardCharsets.UTF_8));
                    Thread.sleep(1000);
                }
                emitter.complete();
            } catch (Exception e) {
                log.error("其他的请求聊天异常 {}", e);
                emitter.completeWithError(e);
                throw new RuntimeException(e);
            }
        });
        return emitter;
    }
```

### 前端代码
- 先来看百炼助手使用fetch
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/31b63f5821694e6db6d90e14dd40a10f.png)

- 我是使用Nuxt 3 框架,也用`fetch` API调用

```javascript

const fetchStream = async () => {
    const response = await fetch('http://127.0.0.1:8080/api/index/responseBodyEmitter'); // 替换为你的接口路径
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    // 持续读取数据流
    while (true) {
        const { done, value } = await reader.read();
        if (done) {
            console.log('Stream completed');
            break;
        }
        const textChunk = decoder.decode(value, { stream: true });
        console.log('Received chunk:', textChunk);
        text.value += textChunk
  
    }
}


onMounted(()=>{
  console.log("onMounted")
  // 返回ResponseBodyEmitter 
  fetchStream()

})
```
## 运行效果
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/1d232d853b2d4f57ae1ae1c3904c4046.gif)




# SseEmitter
- 在了解ResponseBodyEmitter时又发现了SseEmitter。
## 简介
- `ResponseBodyEmitter`的子类，为​​Server-Sent Events（SSE）​​协议设计，基于`text/event-stream`格式实现服务器到客户端的单向推送。自带重连机制。




## 核心代码实现

### 后端代码

```java
   private final List<String> replyData = Arrays.asList("我是", "您的AI助手", "有什么可以帮您", "我是", "您的AI助手", "有什么可以帮您");
     private final ExecutorService executorService = Executors.newFixedThreadPool(2000);

    @RequestMapping("/chat")
    @CrossOrigin
    public SseEmitter chat(String query) {
        SseEmitter emitter = new SseEmitter(180000L);

        executorService.execute(() -> {
            try {
                for (int i = 0; i < replyData.size(); i++) {
                    String value = replyData.get(i);
                    emitter.send(value.getBytes(java.nio.charset.StandardCharsets.UTF_8));
                    Thread.sleep(1000);
                }
                emitter.send(SseEmitter.event().name("end").data("[DONE]"));
                Thread.sleep(1000);
                emitter.complete();
            } catch (Exception e) {
                log.error("其他的请求聊天异常 {}", e);
                emitter.completeWithError(e);
                throw new RuntimeException(e);
            }
        });
        log.info("返回emitter");
        return emitter;
    }

```

### 前端代码

```javascript

//接收后台消息
const  receiveMessage = () =>{
  let eventSource  = new EventSource('http://127.0.0.1:8080/api/index/chat');
   
    eventSource.onopen = (event) =>{
      console.log("onopen ",event); 
    }
    //接收成功
    eventSource.onmessage = (event) => {
      console.log("onmessage ",event);
      
      text.value =  text.value + event.data;
    };

    
    
    eventSource.addEventListener('end', (event) => {
      console.log("服务器主动关闭连接");
      eventSource.close(); // 主动关闭连接
    });


    //接收失败
    eventSource.onerror = (error) => {
        console.error('SSE error:',eventSource.readyState, error);
        if (eventSource.readyState === EventSource.CLOSED) { 
          console.log("正常关闭"); // 应在此过滤已关闭状态
        } else {
          console.error("真实错误:");
        }
        // 如果不close，会自动重连
        eventSource.close()
    };

    
}



onMounted(()=>{

  console.log("onMounted")
  // SseEmitter 的方式
  receiveMessage()

})


```

## 运行效果
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/09f685c5e9934f0499833aab2f10f475.gif)


# 小程序
- 小程序也支持SSE，核心代码如下，我使用的是uni-app-x
## 小程序代码
```javascript

let title = ref<string>("hello")
	onMounted(() => {
		console.log("onMounted")
		startStream()
	})

	const startStream = () => {
		const requestTask = wx.request({
			url: 'http://127.0.0.1:8080/api/index/chat', // 后端接口地址
			method: 'GET',
			// dataType: 'text',
			//responseType: 'stream', // 关键：设置响应类型为 stream
			enableChunked: true,
			success: (res) => {

			},
			fail: (err) => {
				console.error("请求失败:", err);
			}
		});
		const decoder = new TextDecoder('utf-8');

		requestTask.onChunkReceived(function (resp) {
			let data = decoder.decode(resp.data)
			console.log(data)
			title.value += data
		});
	}

```

##  运行效果

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/fa1f926f8b344ac9b846928855be5ebd.gif)



# 本文源码
- [https://github.com/1030907690/emitter-test](https://github.com/1030907690/emitter-test)
- [https://github.com/1030907690/emitter-test-mobile](https://github.com/1030907690/emitter-test-mobile)
- [https://github.com/1030907690/response-body-emitter-web](https://github.com/1030907690/response-body-emitter-web)
#  总结
- ​​ResponseBodyEmitter​​适用于更灵活的流式传输​​场景，如大文件下载或兼容性要求高的实时日志。SseEmitter则是基于标准的SSE协议。
- `ResponseBodyEmitter、SseEmitter`与 `DeferredResult、Callable`同为异步处理，不同的是 `DeferredResult、Callable`只能发送一次数据。`ResponseBodyEmitter、SseEmitter`可以多次调用`send`发送多次。

- 想要了解`DeferredResult和Callable`，可以参考本人拙作 [Spring MVC(Boot) Servlet 3.0异步处理，DeferredResult和Callable](https://blog.csdn.net/baidu_19473529/article/details/123596792)、[Spring MVC(Boot) Servlet 3.0异步处理，DeferredResult和Callable（续篇）](https://blog.csdn.net/baidu_19473529/article/details/130192257)
