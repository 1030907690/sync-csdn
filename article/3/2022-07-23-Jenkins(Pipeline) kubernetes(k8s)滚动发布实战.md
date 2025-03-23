---
layout:					post
title:					"Jenkins(Pipeline) kubernetes(k8s)滚动发布实战"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 之前写过[Jenkins kubernetes(k8s)滚动发布实战](https://blog.csdn.net/baidu_19473529/article/details/125890186)，使用的是`Jenkins 自由风格`，本篇使用`Pipeline`实现滚动发布。

## 开始前的准备
- 与[Jenkins kubernetes(k8s)滚动发布实战](https://blog.csdn.net/baidu_19473529/article/details/125890186)相同，就不赘述了。
## 第一次创建应用
- 与[Jenkins kubernetes(k8s)滚动发布实战](https://blog.csdn.net/baidu_19473529/article/details/125890186)相同，就不赘述了。


## 操作Jenkins

- 怎么下载、运行Jenkins就不赘述了，可以参考拙作[gitlab+jenkins自动发布到Tomcat](https://blog.csdn.net/baidu_19473529/article/details/106139890)。
- Jenkins配置maven、jdk、git等等同样可以参考拙作[gitlab+jenkins自动发布到Tomcat](https://blog.csdn.net/baidu_19473529/article/details/106139890)。

- 下面直接创建`Pipeline`项目。进入配置。

### General
- 这块填下描述就可以了。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/55b97fb612b0893c64aa090cd6f1d960.png)

### 流水线
- 重点是这里`Pipeline script`。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a4e4f748b222db4bf62ec13e474fff40.png)


- `Pipeline script`内容如下（因为我是公共仓库,不需要认证，克隆仓库步骤不必使用`credentialsId`）。

```bash
pipeline {
    agent any
    tools {
        maven 'maven3.6' 
    }
    stages {
        stage('开始') {
            steps {
                echo '开始 '
            }
        }
        
     stage('克隆项目') {
        steps {
        git branch: 'main',
        url: 'https://github.com/1030907690/spring-boot-kubernetes.git'
        sh 'pwd'
        sh "ls -lat"
        }
     }
        
       stage('构建') {
          steps {
            sh 'mvn clean package -DskipTests'
            sh 'echo tag  ${BUILD_TAG}'
            sh 'cp src/main/resources/Dockerfile target'
            sh 'cd target && docker build -t spring-boot-kubernetes:${BUILD_TAG} .'
        
      
          }
        }
        
        stage('滚动更新') {
          steps {
            sh 'kubectl set image  deployment/spring-boot-kubernetes-deployment  spring-boot-kubernetes=spring-boot-kubernetes:${BUILD_TAG} --record'
            sh 'kubectl get pod -o wide'
            sh 'kubectl rollout status deployment/spring-boot-kubernetes-deployment'
            sh 'kubectl get pod -o wide'
      
          }
        }
        
    }
    post {
        success {
            echo '更新成功'
                   
        }

        always {
            echo 'goodbye'
        }
    }
}

```

## Jenkins构建
- 下面就可以使用`Build Now`一键发布最新的应用。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d96e2bead72e59cd122b7ddccfc3cbd0.png)
- 可以查看构建历史，如果有错误的时候，方便排查错误。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/72fa9644d88fbc82fb0802b3bc58fd14.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7f4bd22e01a3775b48ca05999b07b12e.png)
- 如果你不想点Build Now，也可以使用Webhook，可以参考拙作[gitlab+jenkins自动发布到Tomcat](https://blog.csdn.net/baidu_19473529/article/details/106139890)。

## 扩展
- 流水线定义，支持多种，还可以使用`Pipeline script from SCM`，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/08b48600186d5a561dc3be26ddcafafc.png)

- 我们可以把`Jenkinsfile`写在项目中，一并提交到远程仓库，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/77da2c557d02627b9c79a21f3b958e15.png)
- Jenkins的配置修改后如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/12ca57e3c5b9a46592e6ed84c0c18e0a.png)
- 还有因为已经指定了仓库，`Jenkinsfile`中克隆项目的步骤可以注释了。

```
  //stage('克隆项目') {
  //   steps {
  //   git branch: 'main',
  //   url: 'https://github.com/1030907690/spring-boot-kubernetes.git'
  //       sh 'pwd'
  //       sh "ls -lat"
  //     }
  //   }
```
## 小结
- `自由风格`能应对绝大部分场景，`Pipeline`感觉`可视化`体验更好，以代码的形式实现，更容易`细粒度`控制，适用于复杂的场景，同时学习成本高一点。

