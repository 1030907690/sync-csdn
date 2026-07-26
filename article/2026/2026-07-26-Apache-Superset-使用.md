@[TOC](目录)
# 简介
- Apache Superset 是一个开源数据探索和可视化平台（BI 工具），能连接大部分支持SQL的数据库。主要特点是可自助分析、自定义仪表盘、分析结果可视化（导出）、还集成了一个 SQL 编辑器，可以进行 SQL 编辑查询等，提供丰富的拖拽式图表和仪表盘，帮助用户轻松实现自助式数据分析。


#  安装
## 基础功能安装
-  我使用pypi方式，官方文档：[https://superset.apache.org/admin-docs/installation/pypi](https://superset.apache.org/admin-docs/installation/pypi)

- 使用conda创建一个环境
```shell
conda create -n superset python=3.10.6
conda activate superset
```
- 然后按照官方文档执行一下命令
```shell
pip install apache_superset
# 密钥最好复杂一点，可用 python -c "import secrets; print(secrets.token_urlsafe(42))" 生成，演示随便设置的
export SUPERSET_SECRET_KEY=123456
export FLASK_APP=superset
superset db upgrade
superset fab create-admin
superset load_examples
superset init

```
- 如果遇到`cachetools`异常执行
```
pip install cachetools
```

- 安装连接Doris依赖
```
pip install pydoris
```



## MCP 安装

- Superset 支持MCP，有了它我们可用告诉AI要怎样的图表。Superset  MCP 官方文档 ：[https://superset.apache.org/admin-docs/configuration/mcp-server/#1-start-the-mcp-server](https://superset.apache.org/admin-docs/configuration/mcp-server/#1-start-the-mcp-server)
```
 pip install "apache-superset[fastmcp]"
```


# 启动
- 创建一个公共的配置文件，Web UI和MCP都用它。

- superset_config.py
```python


# 密钥
SECRET_KEY="123456"
#MCP
MCP_DEV_USERNAME = "admin"

# -------------- Superset 汉化配置 --------------

# 开启多语言支持
BABEL_IS_TEXTDOMAIN_PER_LANGUAGE = True

# 设置默认语言为简体中文
BABEL_DEFAULT_LOCALE = "zh"



# 语言列表选项
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "zh": {"flag": "cn", "name": "Chinese"},
}
```
 
- Web UI启动

```shell
set SUPERSET_CONFIG_PATH=D:/work/self/superset/superset_config.py
set FLASK_APP=superset
superset run -p 8088 --with-threads --reload --host 0.0.0.0
```

- 启动 MCP

```
set SUPERSET_CONFIG_PATH=D:/work/self/superset/superset_config.py
superset mcp run --host 0.0.0.0 --port 5008
```


# 基础使用
## 创建连接
- 支持很多数据库，这里以Doris为例。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d3e3d7827c824ed1adbfae56fc29ea26.png)

## 创建数据集
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/22ee3af4830a4455a207ec485422d22f.png)

##  创建图表

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/7475cf2a49e14267a0db6b6f60dc6139.png)
## 创建 Dashboard并且绑定图表
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f98df8733f554a7abb8da120e7345008.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d96b60696d3249ef865e456b00dcd6d6.png)





# MCP 使用
- 我使用的是qwen调用MCP, 可用告诉qwen要新增MCP。它会自己配置。
```
{
  "mcpServers": {
    "superset": {
      "url": "http://192.168.81.166:5008/mcp"
    }
  }
}
```
- 配置好的效果如下图
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0f1fccd60a8f4c6192d49efd88ed6900.png)


- 然后输入问题
> 调用superset mcp，生成每天注册量折线图，数据集从t_user获取

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/fbcb82e62f93405890afe950b5098794.png)
- 查看图表创建成功。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a06707a89a8e45a5bd17d66a8c80e7b7.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ea5f513aaae6466da95ce1794432d523.png)




 








 





