---
layout:					post
title:					"storm启动报错Halting process: ("Error when processing an event")"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​

2016-11-22 08:50:39 o.a.z.ClientCnxn [INFO] EventThread shut down
2016-11-22 08:50:39 o.a.z.ZooKeeper [INFO] Session: 0x1588ccfba17000b closed
2016-11-22 08:50:39 o.a.c.f.i.CuratorFrameworkImpl [INFO] Starting
2016-11-22 08:50:39 o.a.z.ZooKeeper [INFO] Initiating client connection, connectString=weekend114:2181,weekend115:2181,weekend116:2181/storm sessionTimeout=20000 watcher=org.apache.curator.ConnectionState@730984
2016-11-22 08:50:39 o.a.z.ClientCnxn [INFO] Opening socket connection to server weekend115/192.168.16.139:2181. Will not attempt to authenticate using SASL (unknown error)
2016-11-22 08:50:39 o.a.z.ClientCnxn [INFO] Socket connection established to weekend115/192.168.16.139:2181, initiating session
2016-11-22 08:50:39 o.a.z.ClientCnxn [INFO] Session establishment complete on server weekend115/192.168.16.139:2181, sessionid = 0x2588ccf7328000c, negotiated timeout = 20000
2016-11-22 08:50:39 o.a.c.f.s.ConnectionStateManager [INFO] State change: CONNECTED
2016-11-22 08:50:39 o.a.c.f.s.ConnectionStateManager [WARN] There are no ConnectionStateListeners registered.
2016-11-22 08:50:39 b.s.d.supervisor [INFO] Starting supervisor with id da7b9967-0c53-4544-8937-d961d7c8f67c at host weekend116
2016-11-22 08:50:39 b.s.event [ERROR] Error when processing event
java.lang.RuntimeException: java.io.EOFException
	at backtype.storm.utils.Utils.deserialize(Utils.java:93) ~[storm-core-0.9.2-incubating.jar:0.9.2-incubating]
	at backtype.storm.utils.LocalState.snapshot(LocalState.java:45) ~[storm-core-0.9.2-incubating.jar:0.9.2-incubating]
	at backtype.storm.utils.LocalState.get(LocalState.java:56) ~[storm-core-0.9.2-incubating.jar:0.9.2-incubating]
	at backtype.storm.daemon.supervisor$sync_processes.invoke(supervisor.clj:207) ~[storm-core-0.9.2-incubating.jar:0.9.2-incubating]
	at clojure.lang.AFn.applyToHelper(AFn.java:161) [clojure-1.5.1.jar:na]
	at clojure.lang.AFn.applyTo(AFn.java:151) [clojure-1.5.1.jar:na]
	at clojure.core$apply.invoke(core.clj:619) ~[clojure-1.5.1.jar:na]
	at clojure.core$partial$fn__4190.doInvoke(core.clj:2396) ~[clojure-1.5.1.jar:na]
	at clojure.lang.RestFn.invoke(RestFn.java:397) ~[clojure-1.5.1.jar:na]
	at backtype.storm.event$event_manager$fn__2378.invoke(event.clj:39) ~[storm-core-0.9.2-incubating.jar:0.9.2-incubating]
	at clojure.lang.AFn.run(AFn.java:24) [clojure-1.5.1.jar:na]
	at java.lang.Thread.run(Thread.java:745) [na:1.7.0_79]
Caused by: java.io.EOFException: null
	at java.io.ObjectInputStream$PeekInputStream.readFully(ObjectInputStream.java:2325) ~[na:1.7.0_79]
	at java.io.ObjectInputStream$BlockDataInputStream.readShort(ObjectInputStream.java:2794) ~[na:1.7.0_79]
	at java.io.ObjectInputStream.readStreamHeader(ObjectInputStream.java:801) ~[na:1.7.0_79]
	at java.io.ObjectInputStream.<init>(ObjectInputStream.java:299) ~[na:1.7.0_79]
	at backtype.storm.utils.Utils.deserialize(Utils.java:88) ~[storm-core-0.9.2-incubating.jar:0.9.2-incubating]
	... 11 common frames omitted
2016-11-22 08:50:39 b.s.event [ERROR] Error when processing event
java.lang.RuntimeException: java.io.EOFException
	at backtype.storm.utils.Utils.deserialize(Utils.java:93) ~[storm-core-0.9.2-incubating.jar:0.9.2-incubating]
	at backtype.storm.utils.LocalState.snapshot(LocalState.java:45) ~[storm-core-0.9.2-incubating.jar:0.9.2-incubating]
	at backtype.storm.utils.LocalState.get(LocalState.java:56) ~[storm-core-0.9.2-incubating.jar:0.9.2-incubating]
	at backtype.storm.daemon.supervisor$mk_synchronize_supervisor$this__6330.invoke(supervisor.clj:307) ~[storm-core-0.9.2-incubating.jar:0.9.2-incubating]
	at backtype.storm.event$event_manager$fn__2378.invoke(event.clj:39) ~[storm-core-0.9.2-incubating.jar:0.9.2-incubating]
	at clojure.lang.AFn.run(AFn.java:24) [clojure-1.5.1.jar:na]
	at java.lang.Thread.run(Thread.java:745) [na:1.7.0_79]
Caused by: java.io.EOFException: null
	at java.io.ObjectInputStream$PeekInputStream.readFully(ObjectInputStream.java:2325) ~[na:1.7.0_79]
	at java.io.ObjectInputStream$BlockDataInputStream.readShort(ObjectInputStream.java:2794) ~[na:1.7.0_79]
	at java.io.ObjectInputStream.readStreamHeader(ObjectInputStream.java:801) ~[na:1.7.0_79]
	at java.io.ObjectInputStream.<init>(ObjectInputStream.java:299) ~[na:1.7.0_79]
	at backtype.storm.utils.Utils.deserialize(Utils.java:88) ~[storm-core-0.9.2-incubating.jar:0.9.2-incubating]
	... 6 common frames omitted
2016-11-22 08:50:39 b.s.util [INFO] Halting process: ("Error when processing an event")
原因是电脑突然断电，未正常退出storm所导致。

解决办法是删除storm配置文件中storm.local.dir所指向的目录中的supervisor和workers两个文件夹。

[zzq@weekend116 bin]$ sudo find / -name supervisor
[sudo] password for zzq: 
/home/zzq/storm-local/supervisor
/home/zzq/app/apache-storm-0.9.2-incubating/bin/storm-local/supervisor
[zzq@weekend116 bin]$ rm -rf /home/zzq/storm-local/supervisor
[zzq@weekend116 bin]$ rm -rf /home/zzq/app/apache-storm-0.9.2-incubating/bin/storm-local/supervisor
[zzq@weekend116 bin]$ sudo find / -name workers
[sudo] password for zzq: 
/home/zzq/storm-local/workers
[zzq@weekend116 bin]$ rm -rf /home/zzq/storm-local/workers
现在启动成功了：



​