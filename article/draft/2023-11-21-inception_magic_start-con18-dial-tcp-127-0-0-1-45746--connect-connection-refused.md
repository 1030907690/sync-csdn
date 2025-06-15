## 背景
- 发现SQL检测时，报错。
- 我的Archery安装在内网，要把SQL提交到外网执行

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3d3cc15664f46a655b3c49b71d1892c4.png)
 

 
## 解决方案

```bash
docker exec -i -t archery bash
vi /opt/archery/sql/utils/ssh_tunnel.py
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fe61571fbbf506333ac124a37c387a4c.png)

```python
...省略...
    def get_ssh(self):
        """
        获取ssh映射的端口
        :param request:
        :return:
        """
        return "archery", self.server.local_bind_port  #修改这行代码
```



## 参考

- [https://github.com/hhyo/Archery/issues/1362](https://github.com/hhyo/Archery/issues/1362)
- [https://github.com/hhyo/Archery/wiki/FAQ](https://github.com/hhyo/Archery/wiki/FAQ)