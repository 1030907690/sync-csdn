
@[TOC](目录)

# 准备
- NodeJS 18+版本



# 配置环境变量
- 设置`GEMINI_API_KEY` 变量，在[https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)创建key

- 设置代理（可选，取决于您的网络）,不配置可能会报错 `api error: exception typeerror: fetch failed sending request`
```
set HTTP_PROXY=http://127.0.0.1:10808  # 配置到系统环境变量也行，换成自己的地址
```
# 运行
- 我用`RuoYi-Vue`项目测试一下，在当前目录运行

```
npx https://github.com/google-gemini/gemini-cli
或者
npm install -g @google/gemini-cli
gemini
```


- 登录有点小问题 ,应该暂时未解决
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e8e963acf689479b9565514f144998a1.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/303b8d430c084287bbe55ac75ed30b71.png)

- 我多次尝试网页认证然后重新打开cmd就能进入了


![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c4f2674ced5a498bb3728ccde20a7a27.png)



# 使用
## 基础使用
- 输入问题
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ed6275d293144a789764409e8c758fba.png)

- 运行结果

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/364f30963b634ea88a8ca361112534c9.png)
## 配置MCP
- context7（获取最新代码文档）、task-master（生成产品需求文档，再拆分成子任务）
	- https://github.com/eyaltoledano/claude-task-master
	- https://github.com/upstash/context7
- 找到当前用户目录下`.gemini/settings.json`
```json
 {
 ...省略...
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
	"taskmaster-ai": {
	  "command": "npx",
	  "args": ["-y", "--package=task-master-ai", "task-master-ai"],
	  "env": {
		"GOOGLE_API_KEY": "用你自己的key"
	  }
	}
	
  }
}
```
-  输入`/mcp`后就能看到可调用的工具
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8a81214701f04381bb4154f48d83606c.png)

## 调用MCP

- 输入`使用mcp context7讲解AutoGen最新版新增的新特性`

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/225c466cdf844be4beba458d26b26890.png)
- 选择始终允许

- 运行结果
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/24dfb2ae0f274f5aafc63bbe4e8250d8.png)








# 参考
- [https://github.com/google-gemini/gemini-cli/issues/1549](https://github.com/google-gemini/gemini-cli/issues/1549)
- [https://www.cnblogs.com/maplepie/p/18949291](https://www.cnblogs.com/maplepie/p/18949291)
- [https://www.bilibili.com/video/BV13zKozyEKC/](https://www.bilibili.com/video/BV13zKozyEKC/)