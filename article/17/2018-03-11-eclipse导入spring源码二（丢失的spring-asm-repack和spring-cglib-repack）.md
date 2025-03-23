---
layout:					post
title:					"eclipse导入spring源码二（丢失的spring-asm-repack和spring-cglib-repack）"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 在上一篇[eclipse导入spring源码一](http://blog.csdn.net/baidu_19473529/article/details/79518337) 中已经完成一部分了，但是整个项目代码依然有报错:
![这里写图片描述](https://img-blog.csdn.net/20180311175251999?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

- 很明显的错误，就是找不到jar(spring-asm-repack-5.0.1.jar和spring-cglib-repack-3.1.jar)包,查看源文件的确没有这2个包。那么怎么得到这2个包呢？我找过maven仓库也没找到,最后终于知道了**可以通过jar命令编译spring-core包得到这2个jar**

###编译生成spring-asm-repack-5.0.1.jar和spring-cglib-repack-3.1.jar

- 到这个网站下载spring的lib压缩包[http://repo.springsource.org/libs-release-local/org/springframework/spring/](http://repo.springsource.org/libs-release-local/org/springframework/spring/) 我下载的是和源码对应的spring-framework-3.2.18.RELEASE-dist.zip   

- 解压spring-framework-3.2.18.RELEASE-dist.zip  到spring-framework-3.2.18.RELEASE-dist\spring-framework-3.2.18.RELEASE\libs路径下找到spring-core-3.2.18.RELEASE.jar

- 再把spring-core-3.2.18.RELEASE.jar用压缩工具解压出来：

![这里写图片描述](https://img-blog.csdn.net/20180311180512855?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

- 然后cmd到这个目录下执行命令：

```
jar cvf spring-cglib-repack-3.1.jar org\springframework\cglib
```

生成spring-cglib-repack-3.1.jar

![这里写图片描述](https://img-blog.csdn.net/20180311180739779?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

-  同样的执行命令：

```
jar cvf spring-asm-repack-5.0.4.jar org\springframework\asm
```
生成spring-asm-repack-5.0.4.jar
![这里写图片描述](https://img-blog.csdn.net/20180311180955467?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

- 好了现在这2个jar都有了，放到spring-core项目里面build\libs路径下,如果没有这个路径就新建一个。

 - 现在就不报错了
 ![这里写图片描述](https://img-blog.csdn.net/2018031118152696?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

- 接下来改一下class的输出路径,换成直接bin为class输出路径，写一点代码测试一下spring-beans工程。

![这里写图片描述](https://img-blog.csdn.net/20180311181921194?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)


新建beans.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns="http://www.springframework.org/schema/beans"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
     http://www.springframework.org/schema/beans/spring-beans-4.0.xsd">

    <bean id="myTestBean" class="test.MyTestBean">
    <property name="name" value="zhangsan"></property>
    </bean>
</beans>
```

MyTestBean.java

```


package test;


/**
 * 
 * @author Administrator
 */
public class MyTestBean {
	
	private String name;

	
	public String getName() {
		return name;
	}

	
	public void setName(String name) {
		this.name = name;
	}
	
	

}

```

测试类Test.java：

```


package test;

import org.springframework.beans.factory.xml.XmlBeanFactory;
import org.springframework.core.io.ClassPathResource;

/**
 * 
 * @author Administrator
 */
public class Test {
	
	public static void main(String[] args) {
	    /**
	     * 用XmlBeanFactory这个方式获得bean,现在已经不用这个方式了
	     */
	        XmlBeanFactory xmlBeanFactory = new XmlBeanFactory(new ClassPathResource("beans.xml"));
	        MyTestBean myTestBean = (MyTestBean) xmlBeanFactory.getBean("myTestBean");
	        System.out.println( myTestBean+ "---"+ myTestBean.getName());
	}

}

```

运行结果和目录结构：
![这里写图片描述](https://img-blog.csdn.net/20180311182651803?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

到此spring的基础beans模块已经可以成功运行了。