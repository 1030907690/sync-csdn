---
layout:					post
title:					"start-dfs datanode没启动起来，异常java.io.IOException: Incompatible clusterIDs in"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​


[zzq@weekend110 app]$ cat /home/zzq/app/hadoop/hadoop-2.4.1/data/dfs/data/current/VERSION
#Mon Oct 10 02:10:19 PDT 2016
storageID=DS-ae5abbe8-c187-4e58-b050-81b7def58776
clusterID=CID-18605df2-4c30-41ba-80dd-4127be0db4b4
cTime=0
datanodeUuid=45734385-9901-427c-98ee-c53496ea8f4a
storageType=DATA_NODE
layoutVersion=-55

今天启动Hadoop，执行完start-dfs.sh后，用jps查看进程，datenode没有启动成功



于是找到datanode的日志查看



意思已经很明显了是两个id不相等，在网上查了一下，网上说的是格式化，问题依旧没解决，而且这个办法在实际生产中并不科学，下面看一种比较好的解决办法，去修改clusterID让他们的值相等就可以了。

查看core-site.xml，找到存namenode元数据和datanode元数据的路径。



在这个路径/home/zzq/app/hadoop/hadoop-2.4.1/data下去找namenode和datanode的VERSION文件

[zzq@weekend110 app]$ cat /home/zzq/app/hadoop/hadoop-2.4.1/data/dfs/data/current/VERSION
#Mon Oct 10 02:10:19 PDT 2016
storageID=DS-ae5abbe8-c187-4e58-b050-81b7def58776
clusterID=CID-18605df2-4c30-41ba-80dd-4127be0db4b4
cTime=0
datanodeUuid=45734385-9901-427c-98ee-c53496ea8f4a
storageType=DATA_NODE
layoutVersion=-55
[zzq@weekend110 app]$ cat /home/zzq/app/hadoop/hadoop-2.4.1/data/dfs/name/current/VERSION
#Fri Oct 14 03:20:18 PDT 2016
namespaceID=681718397
clusterID=CID-a562d0d9-7063-47d8-b609-a2103a1a5b8a
cTime=0
storageType=NAME_NODE
blockpoolID=BP-1458349914-192.168.16.131-1476440418189
layoutVersion=-56
只需要把其中一个clusterID改成相同的就可以了
改了之后成功启动了



​