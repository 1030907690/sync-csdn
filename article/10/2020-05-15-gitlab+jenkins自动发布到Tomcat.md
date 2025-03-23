---
layout:					post
title:					"gitlab+jenkins自动发布到Tomcat"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
### CI&CD的价值和为什么要用CI&CD
>- 持续集成（Continuous Integration, CI）是一种软件开发实践。在持续集成中，团队成员
频繁集成他们的工作成果，一般每人每天至少集成一次，也可以多次。每次集成会经过自动
构建（包括静态扫描、安全扫描、自动测试等过程）的检验，以尽快发现集成错误。许多团
队发现这种方法可以显著减少集成引起的问题，并可以加快团队合作软件开发的速度。
>-   持续交付（Continuous Delivery）是指频繁地将软件的新版本交付给质量团队或者用户，
以供评审，如果评审通过，代码就进入生产阶段。
>- 持续部署（Continuous Deployment）是持续交付的下一步，指的是代码通过评审以后，
自动部署到生产环境中。
>- 通过上面的定义我们不难发现，持续突出的就是一个"快"字，商业软件的快速落地需求推
进了软件工程的发展。可持续的、快速迭代的软件过程是当今主流开发规约。尤其在互联网
亍业，快速响应即是生命线。从一个想法到产品落地都处在冲锋的过程中，机会稍纵即逝。
响应用户反馈也是万分敏捷，早晨的反馈在当天就会上线发布，快得让用户感觉倍受重视。
"快"已经成为商业竞争力。这一切都要求企业具备快速响应的能力，这正是推动持续集成、
丫续交付、持续部署的动力。
> - 说到底就是快速交付价值，从工程上、管理上、组织上、工具上来提高效率，打造可靠的、快速的产品(项目)交付过程。
### CI&CD技术栈
>- 一般持续集成工具中以Jenkins使用最为广泛，由Jenkins来作业化持续集成过程；利用GitLab
来管理程序版本;利用Gerrit来做代码审核；利用Sonar进行代码质量扫描；利用JUnit进行
单元测试;利用Docker compose来构建镜像；利用Docker来部署容器；利用Kubemetes、
Rancher等进行服务编排。

- 以上内容大部分摘抄自《持续集成与持续部署实践》
### 我的环境
|名称|版本|文档或下载地址|
|---|---|---|
|Jenkins|2.222.3  |[https://www.jenkins.io/](https://www.jenkins.io/)|
|tomcat|  8.5.20| [https://tomcat.apache.org/](https://tomcat.apache.org/)|
|maven|  3.6.3  | [https://maven.apache.org/](https://maven.apache.org/)|
|jdk|  1.8.144  | [https://www.oracle.com/](https://www.oracle.com/)|
|gitlab CE|  docker版本最新版  | [https://docs.gitlab.com/omnibus/docker/](https://docs.gitlab.com/omnibus/docker/) |
 
 
### 安装和配置gitlab、jdk、maven、Tomcat、Jenkins
- gitlab安装我写了一键脚本(考虑到可能无法直接下载文件，我把地址发一下[https://github.com/1030907690/public-script/tree/master/docker](https://github.com/1030907690/public-script/tree/master/docker))

```bash
wget https://github.com/1030907690/public-script/raw/master/docker/install-docker.sh
wget https://raw.githubusercontent.com/1030907690/public-script/master/docker/install-gitlab.sh
sh install-docker.sh
sh install-gitlab.sh
```

- jdk、maven、Tomcat的安装配置不再赘述了
- maven最好换成国内源，还有记得改下`<localRepository>`标签对的值

```bash
    <mirror>
          <id>nexus-aliyun</id>
          <mirrorOf>central</mirrorOf>
          <name>Nexus aliyun</name>
          <url>http://maven.aliyun.com/nexus/content/groups/public</url>
      </mirror>

```

- Tomcat需要改下配置conf/tomcat-users.xml配置；配置好后就把Tomcat运行起来；这是为了Jenkins发布到Tomcat

```xml
<role rolename="tomcat"/>
<role rolename="role1"/>
<role rolename="manager-script"/>
<role rolename="manager-jmx"/>
<role rolename="manager-status "/>
<role rolename="manager-gui"/>
<user username="tomcat" password="tomcat" roles="manager-gui,role1,tomcati,manager-script,manager-jmx,manager-status"/>

```

- Jenkins运行可以docker、可以用Tomcat之类的，我是直接java命令运行的(官网有介绍的)；这里如果写的8080与Tomcat默认端口冲突了，记得修改Tomcat的端口

```bash
java -jar jenkins.war --httpPort=8080
```
- 第一次运行它会要求输入`initialAdminPassword`文件的内容，具体路径页面会提示，比如linux的是`/root/.jenkins/secrets/initialAdminPassword`在`用户目录下.jenkins文件夹里`。
- 然后安装插件、创建用户
- 后面就能进入Jenkins主界面了(这里2个项目是我之前就创建过的，下面的内容就是这2个项目)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/72f3e67210c4c3a5e8b6dcbcbaaab67f.png)

- 下一步配置Jenkins，点击全局工具配置
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ac371a6406d497bd4b005f2d125ea95b.png)
- 配置maven、jdk、maven；一般不选自动安装，太慢
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c06a34031ec9eceefdd8503d1ea63dec.png)
- 如果没有git，比如centos，执行 `yum install git -y` 即可
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/388d3d0141a361a1152270980fcbedf6.png)
- 配置了这些保存，大部分的场景都够用了。
- 下一步安装插件，如果初始化Jenkins时，选择了安装推荐插件，这时候要安装的插件就比较少了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/09f4097ce22fb7846290ba0565c076d4.png)
- 点击进去，选择可安装选择`Generic Webhook Trigger Plugin`，`Deploy to container Plugin`
	- `Deploy to container Plugin` 是发布到Tomcat需要的插件
	- `Generic Webhook Trigger Plugin` 是触发构建需要的插件


### 构建项目
- 点击新建Item一般都是构建一个自由风格的项目
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/42e41c90e01c1ccc6fa721bfff3e802f.png)
- 填写描述和git地址，认证凭证(即拉取代码的帐号密码)，![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f1182ee71f7bfa3f18973400cc2fe77d.png)

- 这里我早已准备好了一个git项目，简单的servlet程序；源代码在这里[https://github.com/1030907690/simple-servlet-web/](https://github.com/1030907690/simple-servlet-web/)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b5ba3e862b0f36b55601c902e51974e4.png)
- 构建
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/671fa38e33afa7c66925966351f94e3f.png)
- 保存
- 下一步测试构建是否成功，点击`Build Now左边的图标`
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b7092909e1fea8eef403ff80a75d532f.png)
 - 点击控制台输出查看日志![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ffe19711cbf0ac468631c8eddb2bc1f6.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6fd9b365b978ff47e181559141a7a227.png)
- 此时查看工作空间，已经有了war包
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/240c26f07220f576a51368fe6afc3f03.png)

- 下一步依然到配置，现在要实现发布到Tomcat，选择构建后操作->`Deploy war/ear to a container`；我Tomcat的端口改成了8081，为了不与Jenkins冲突，帐号密码是前面配置tomcat-users.xml里；context path是访问路径；WAR/EAR files填工作空间相对路径
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7e704f8042f9ba0ec365751692ccfd34.png)
- 再点击一次`Build Now`就能看到效果了
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/411d88162c23c841f695325477c814bf.png)

### 结合webhook构建项目
- 这次由手动换成自动，一个里程碑的版本所以我再建了个项目来演示；其他配置和前面的一样，点击配置
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7c5a7b644e6bb30375e0c1df58601adb.png)
- 勾选`Generic Webhook Trigger`，写个token
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1259dfc726a3e6ec24c119db7e4fbc61.png)
- 点击保存
```bash
#JENKINS_URL换成自己的Jenkins地址
http://JENKINS_URL/generic-webhook-trigger/invoke/invoke?token=simple
```
- 然后修改下项目提交，再直接访问这个地址，它会自动构建
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/81e6e70ebc85d4cc6f2f24ce6816493a.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a0a35876c9f947da630007dff095efc1.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0ab5838ffa2a04b9db239f7e77050e59.png)
- 下一步就交个gitlab去触发这个url
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/43fe70ab4a3eea349a440a76bbffdad1.png)
- 填入url后，点击Add webhook
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a0ea444247949b69ccee5ac5a71e558b.png)
- 现在再来测试下，修改下程序，再提交上去。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a6b6e0162134cf206688898aab54f436.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/12723e91e7652e74ddfcb7b96398429e.png)
- 测试结果成功

### 总结
- 上面只是粗浅的介绍了下Jenkins的使用，并且目前直接使用tomcat运行程序的方式比较过时了；不过万变不离其宗，Jenkins足够灵活，有了上面的粗浅知识，还是能快速进阶的;部署jar等也是类似的。如果文章有问题的地方希望您能指出，感谢您的观看。
