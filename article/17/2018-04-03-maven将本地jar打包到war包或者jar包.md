---
layout:					post
title:					"maven将本地jar打包到war包或者jar包"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
###本地jar打包到war：
   - 这里比如支付宝的jar maven仓库没有,从本地导入：
   

```
<dependency>
        <groupId>alipay-sdk-java20180104135026</groupId>
          <artifactId>alipay-sdk-java20180104135026</artifactId>
          <version>20180104135026</version>
          <scope>system</scope>
          <systemPath>${basedir}/alipay-sdk-java20180104135026.jar</systemPath> <!-- ${basedir} 是当前项目里的路径和pom.xml同级的路径-->
</dependency>

```

- 然后在`<build>  -> <plugins>`里面增加这么一段代码 如果lib不放在/WEB-INF/lib可使用此配置 将本地jar打包到war包里 `注意：如果上面systemPath路径是这样写的${basedir}/src/main/webapp/WEB-INF/lib/alipay-sdk-java20180104135026.jar,就是把jar包直接放在WEB-INF/lib里面的,一般不用写下面的这段代码，不然会有2个这样的包都打包在WEB-INF/lib里面。`

```
<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-dependency-plugin</artifactId>
	<version>2.10</version>
	<executions>
		<execution>
			<id>copy-dependencies</id>
			<phase>compile</phase>
			<goals>
				<goal>copy-dependencies</goal>
			</goals>
			<configuration>
				<outputDirectory>${project.build.directory}/${project.build.finalName}/WEB-INF/lib</outputDirectory>
				<includeScope>system</includeScope>
			</configuration>
		</execution>
	</executions>
</plugin>
```




###本地jar打包到jar：
- 需要上面的2个配置,并且需要把包的路径写入jar包里面`META-INF/MANIFEST.MF`文件 Class-Path,否则会报java.lang.ClassNotFoundException, 这就要指定mainClass和manifestEntries->Class-Path

```
			<plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>2.6</version>
                <configuration>
                    <archive>
                        <manifest>
                            <addClasspath>true</addClasspath>
                            <classpathPrefix>lib/</classpathPrefix>
                            <mainClass>com.xx.xxx.start.Application</mainClass> <!-- 运行jar的main class  -->
                        </manifest>
                        <!-- 添加本地的jar -->
                        <manifestEntries>
                            <Class-Path>lib/class-util-1.0.jar lib/pool-executor-1.0.jar</Class-Path> <!-- 这个>lib/class-util-1.0.jar 路径是已经被打包到target/lib里的,多个包用空格隔开就可以了 -->
                        </manifestEntries>
                    </archive>
                </configuration>
            </plugin>
```