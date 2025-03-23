---
layout:					post
title:					"LlamaIndex ollama 搭建本地RAG应用，建立本地知识库"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
##   简介
- ollama：本地运行大型语言模型的工具软件。用户可以轻松下载、运行和管理各种开源 LLM。降低使用门槛，用户能快速启动运行本地模型。
- LlamaIndex：用来连接大语言模型和外部数据的框架(外部数据指自身领域的特定知识)，它将两者结合起来，提升回答的准确性。


## 安装前的准备
### 下载ollama
- ollama官方下载地址 [https://ollama.com/download](https://ollama.com/download)  ,目前最新版是0.4.2。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/355066b053e6462b986da98e24c1d080.png)
### 创建llamaindex conda环境，为后面编码作准备
- 为啥要用conda呢？
> 后面要编码，考虑不同项目依赖的python版本可能不同，用conda来管理,可以快速新增python环境，如果环境搞砸了，用命令删除也很方便。

- conda下载地址 [https://www.anaconda.com/download/success](https://www.anaconda.com/download/success)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/4f103edc1d6e4dbbb351af610f355c66.png)

## 环境变量


| 参数                     | 标识与配置                                                                                                                                                                                                                          |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OLLAMA_MODELS            | 表示模型文件的存放目录，默认目录为**当前用户目录**即  `C:\Users%username%.ollama\models`<br />Windows 系统 **建议不要放在C盘**，可放在其他盘（如 `d:\software\ollama\models`）                                             |
| OLLAMA_HOST              | 表示ollama 服务监听的网络地址，默认为**127.0.0.1** <br />如果想要允许其他电脑访问 Ollama（如局域网中的其他电脑），**建议设置**成 **0.0.0.0**                                                                    |
| OLLAMA_PORT              | 表示ollama 服务监听的默认端口，默认为**11434** <br />如果端口有冲突，可以修改设置成其他端口（如**8080**等）                                                                                                            |
| OLLAMA_ORIGINS           | 表示HTTP 客户端的请求来源，使用半角逗号分隔列表<br />如果本地使用不受限制，可以设置成星号 `*`                                                                                                                                     |
| OLLAMA_KEEP_ALIVE        | 表示大模型加载到内存中后的存活时间，默认为**5m**即 5 分钟<br />（如纯数字300 代表 300 秒，0 代表处理请求响应后立即卸载模型，任何负数则表示一直存活）<br />建议设置成 **24h** ，即模型在内存中保持 24 小时，提高访问速度 |
| OLLAMA_NUM_PARALLEL      | 表示请求处理的并发数量，默认为**1** （即单并发串行处理请求）<br />建议按照实际需求进行调整                                                                                                                                   |
| OLLAMA_MAX_QUEUE         | 表示请求队列长度，默认值为**512** <br />建议按照实际需求进行调整，超过队列长度的请求会被抛弃                                                                                                                                  |
| OLLAMA_DEBUG             | 表示输出 Debug 日志，应用研发阶段可以设置成**1** （即输出详细日志信息，便于排查问题）                                                                                                                                        |
| OLLAMA_MAX_LOADED_MODELS | 表示最多同时加载到内存中模型的数量，默认为**1** （即只能有 1 个模型在内存中）                                                                                                                                                |

- 注意下`OLLAMA_HOST`，好像会自动创建用户环境变量。本地直接用`127.0.0.1`。方便调试。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e49d2391241c4af3bf2b8866f395e225.png)

- `OLLAMA_MODELS`环境建议配置一下，默认是在C盘，一个模型一般是几个G。比较占用空间。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/87ccfd87f64e496290df758e4d4eb93f.png)


## 迁移ollama到其他盘
- 由于ollama是直接安装在C盘，C盘如果空间紧张，可以像我一样迁移到D盘，如果觉得没有必要，可忽略此步骤。
- - 方法就是在C盘创建软链接，将真是数据放到D盘。
> Administrator   是我的用户名
```bash
mklink /D C:\Users\Administrator\.ollama D:\software\Ollama\.ollama
mklink /D C:\Users\Administrator\AppData\Local\Ollama D:\software\Ollama\log
mklink /D C:\Users\Administrator\AppData\Local\Programs\Ollama D:\software\Ollama\app
```

- 迁移后的结果
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f3d581334ee94912b8da5c91774863a9.png)
## 运行ollama 
### 方式一
- 在程序栏中找到
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a59d17d777464042b5551aaf76cebd24.png)
 点击就会运行。然后右下角会出现ollama的小图标。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e47724a126d0466a9a7bc503063ca481.png)

### 方式二
- 在命令行中输入 `ollama serve` (我没有独显，是以CPU方式运行的)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3daa1d016c7c48b09a82fa99fcbc48e8.png)



### 禁止ollama开机自启动
- 如果不想让ollama开机自启动，打开任务管理器， 到 `启动` 栏目，选中右键 -> 禁用止自启动。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/806ba68de8054368ae4586f464b30b80.png)
### 运行第一个模型
- 打开[https://ollama.com/](https://ollama.com/) 网站在输入框中输入`qwen`。进入`qwen2.5-coder`,`coder`表示对编程方面的问题有优化。![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0afc99cd81974e38abfd7e68ab5277a1.png)
- 在详情页面可以看到各种版本tag。可以根据自身电脑配置情况使用哪一个。一般来说模型越大就越消耗资源。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5de9492e947d4e2ba697654905758207.png)
- 我选择的是当前最新版本。运行的命令是。如何没有就会先下载。

```
ollama run qwen2.5-coder
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6a149cb16f0f42cb97faa11cf2af764c.png)
- 运行后的界面如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e954242583c04f639d60a622ef556c5f.png)
- 然后我们输入一个问题，验证是否成功。`13.8与13.11哪个大？`
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/bdaa035be9ea4e2cab601de3bbe9e91c.png)
- 可以看出答案正确，安装成功了。


## Chatbox聊天
- 面对CMD的窗口聊天体验不太好，所以我们用一下Chatbox软件。
### 下载Chatbox
- 下载地址 [https://chatboxai.app/en](https://chatboxai.app/en)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/7544e4eb85e7426d9df666c90c8c662f.png)


### 配置ollama地址和模型
- 第一个下拉框选择 ollama ， 下面的下拉框选地址和模型配置。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/85a461581fd8457baf024393609b2437.png)

### 验证
- 我们输入一个问题，验证是否成功。`13.8与13.11哪个大？`
 
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/2e8148ef626b477fa5594670a8901111.png)
-  结果正确。

- 然后我们再试一个冷门问题`介绍一下CSDN博主愤怒的苹果ext擅长什么？` 。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8ab6a6ba3cf54ebeb2e9743a1ada1051.png)
- 可以看出这个问题它是不知道的。

## 建立自身特定知识数据搭配大语言模型
- 一般对于模型不知道或不准确的回答有两种解决方案
	- 1、模型微调。
	- 2、建立自身特定知识数据 + 大语言模型
- 对于要求准确度不是很高的场景一般会采用建立自身特定知识数据的方案。本文要实践的就是这种方案。

### 创建项目环境

- 利用conda创建
```bash
 conda create -n llamaindex python=3.10.13
 conda activate  llamaindex
 #  安装依赖
pip install llama-index
pip install llama-index-llms-ollama
pip install llama-index-embeddings-ollama
pip install llama-index-readers-file
```

- 如果不知道怎么在pycharm中应用conda环境，可以看我这篇文章 [https://blog.csdn.net/baidu_19473529/article/details/143442416](https://blog.csdn.net/baidu_19473529/article/details/143442416)，就不再赘述。

- 拉取嵌入模型.

```python
ollama pull quentinz/bge-small-zh-v1.5
```

### 代码 
- test.py

```python
 
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.core.node_parser import SentenceSplitter
import logging
import sys

# 增加日志信息
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
# 配置 嵌入模型/预训练，这里我们用quentinz/bge-small-zh-v1.5
from llama_index.embeddings.ollama import OllamaEmbedding
Settings.embed_model = OllamaEmbedding(model_name="quentinz/bge-small-zh-v1.5")
# 配置ollama的LLM模型，这里我们用qwen2.5-coder
Settings.llm = Ollama(model="qwen2.5-coder", request_timeout=600.0)

#特定知识数据
data_file = ['D:/work/self/Llamaindex-sample/data/a.txt']
documents = SimpleDirectoryReader(input_files=data_file).load_data()
index = VectorStoreIndex.from_documents(documents, transformations=[SentenceSplitter(chunk_size=256)])

query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("介绍一下CSDN博主愤怒的苹果ext擅长什么？")
print(response)

```


- 特定知识数据内容 a.txt

```python
 CSDN博主愤怒的苹果ext擅长Ai、Fw、Fl、Br、Ae、Pr、Id、Ps等软件的安装与卸载，精通CSS、JavaScript、PHP、ASP、C、C＋＋、C#、Java、Ruby、Perl、Lisp、python、Objective-C、ActionScript、Pascal等单词的拼写，熟悉Windows、Linux、Mac、Android、IOS、WP8等系统的开关机。
```
###  运行结果
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/674f065340ee424b95c375a4eba28252.png)
- 可以看出现在的运行结果基本上就是我们想要的结果了。

### streamlit应用
- 通过硬编码的方式去问答没有图形化界面方便，下面引入streamlit就能得到干净好看的Web问答界面了，

- 命令行运行

```python
 pip install streamlit
```

- 代码 app.py

```python
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.memory import ChatMemoryBuffer
import os
import tempfile
import hashlib

# OLLAMA_NUM_PARALLEL：同时处理单个模型的多个请求
# OLLAMA_MAX_LOADED_MODELS：同时加载多个模型
os.environ['OLLAMA_NUM_PARALLEL'] = '2'
os.environ['OLLAMA_MAX_LOADED_MODELS'] = '2'


# Function to handle file upload
def handle_file_upload(uploaded_files):
    if uploaded_files:
        temp_dir = tempfile.mkdtemp()
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
        return temp_dir
    return None


# Function to calculate a hash for the uploaded files
def get_files_hash(files):
    hash_md5 = hashlib.md5()
    for file in files:
        file_bytes = file.read()
        hash_md5.update(file_bytes)
    return hash_md5.hexdigest()


# Function to prepare generation configuration
def prepare_generation_config():
    with st.sidebar:
        st.sidebar.header("Parameters")
        max_length = st.slider('Max Length', min_value=8, max_value=5080, value=4056)
        temperature = st.slider('Temperature', 0.0, 1.0, 0.7, step=0.01)
        st.button('Clear Chat History', on_click=clear_chat_history)

    generation_config = {
        'num_ctx': max_length,
        'temperature': temperature
    }
    return generation_config


# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是你的助手，你需要什么帮助吗？"}]


# File upload in the sidebar
st.sidebar.header("Upload Data")
uploaded_files = st.sidebar.file_uploader("Upload your data files:", type=["txt", "pdf", "docx"],
                                          accept_multiple_files=True)

generation_config = prepare_generation_config()


# Function to initialize models
@st.cache_resource
def init_models():
    embed_model = OllamaEmbedding(model_name="quentinz/bge-small-zh-v1.5")
    Settings.embed_model = embed_model

    llm = Ollama(model="qwen2.5-coder", request_timeout=360.0,
                 num_ctx=generation_config['num_ctx'],
                 temperature=generation_config['temperature'])
    Settings.llm = llm

    documents = SimpleDirectoryReader(st.session_state['temp_dir']).load_data()
    index = VectorStoreIndex.from_documents(documents)

    memory = ChatMemoryBuffer.from_defaults(token_limit=4000)
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt="You are a chatbot, able to have normal interactions.",
    )

    return chat_engine


# Streamlit application
st.title("💻 Local RAG Chatbot 🤖")
st.caption("🚀 A RAG chatbot powered by LlamaIndex and Ollama 🦙.")

# Initialize hash for the current uploaded files
current_files_hash = get_files_hash(uploaded_files) if uploaded_files else None

# Detect if files have changed and init models
if 'files_hash' in st.session_state:
    if st.session_state['files_hash'] != current_files_hash:
        st.session_state['files_hash'] = current_files_hash
        if 'chat_engine' in st.session_state:
            del st.session_state['chat_engine']
            st.cache_resource.clear()
        if uploaded_files:
            st.session_state['temp_dir'] = handle_file_upload(uploaded_files)
            st.sidebar.success("Files uploaded successfully.")
            if 'chat_engine' not in st.session_state:
                st.session_state['chat_engine'] = init_models()
        else:
            st.sidebar.error("No uploaded files.")
else:
    if uploaded_files:
        st.session_state['files_hash'] = current_files_hash
        st.session_state['temp_dir'] = handle_file_upload(uploaded_files)
        st.sidebar.success("Files uploaded successfully.")
        if 'chat_engine' not in st.session_state:
            st.session_state['chat_engine'] = init_models()
    else:
        st.sidebar.error("No uploaded files.")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是你的助手，你需要什么帮助吗？"}]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message['role'], avatar=message.get('avatar')):
        st.markdown(message['content'])

# Display chat input field at the bottom
if prompt := st.chat_input("Ask a question about Datawhale:"):

    with st.chat_message('user'):
        st.markdown(prompt)

    # Generate response
    print("st.session_state ",st.session_state)
    response = st.session_state['chat_engine'].stream_chat(prompt)
    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        res = ''
        for token in response.response_gen:
            res += token
            message_placeholder.markdown(res + '▌')
        message_placeholder.markdown(res)

    # Add messages to history
    st.session_state.messages.append({
        'role': 'user',
        'content': prompt,
    })
    st.session_state.messages.append({
        'role': 'assistant',
        'content': response,
    })
```

- 运行app.py的命令

```bash
  streamlit run app.py
```

- 运行后将自动打开浏览器页面
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/7cf444fac68f47d6ae30f3fe51bed9e5.png)

- 启动完成后，首先上传外部数据，初始化模型。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/23a166fc5891409db39390b80c072408.png)
- 再提问验证是否成功。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/59c2055dbea04a88b8de0556dd3525d2.png)
- 与前面的回答差不多就表示成功了。

## 本文所使用的源码地址

- [https://github.com/1030907690/Llamaindex-sample](https://github.com/1030907690/Llamaindex-sample)


## 参考

- https://juejin.cn/post/7418086006114713619
- https://blog.llyth.cn/1555.html
- https://www.bilibili.com/opus/978763969531478024
- https://github.com/datawhalechina/handy-ollama/blob/main/notebook/C7/LlamaIndex_RAG/%E4%BD%BF%E7%94%A8LlamaIndex%E6%90%AD%E5%BB%BA%E6%9C%AC%E5%9C%B0RAG%E5%BA%94%E7%94%A8.ipynb




















