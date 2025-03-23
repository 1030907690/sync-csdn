---
layout:					post
title:					"ThreadLocal"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
####什么是ThreadLocal
>翻译过来中文意思就叫线程局部变量（thread local variable）,就是为每个线程都创建一个这样的变量(以ThreadLocal对象为键、任意对象为值的存储结构),这个变量被附带在线程上,每个线程之接相互隔离,互不干扰,该变量副本只能创建它的线程能使用。




####ThreadLocal应用场景
- 如下代码：

```
public class DBUtil {
     
    private static Connection connect = null;
     
    public static Connection getConnection() {
        if(connect == null){
            connect = DriverManager.getConnection();
        }
        return connect;
    }
     
    public static void close() {
        if(connect!=null){
            connect.close();
        }
    }
}
```

- 观察一下这段代码在单线程中使用是没有任何问题的，但是如果在多线程中使用呢？因为JDBC规范并未要求Connection自身一定是线程安全的，很显然，如果没有额外的协调时,在多线程中使用会存在线程安全问题：
  > (1):这里面的2个方法都没有进行同步，在多线程调用的情况下很可能在getConnection方法中会多次创建connect
  > (2):由于connect是共享变量，那么必然在调用connect的地方需要使用到同步来保障线程安全，因为很可能一个线程在使用connect进行数据库操作，而另外一个线程调用close方法关闭链接(就可能会报 No operations allowed after connection closed)。

- 所以出于线程安全的考虑，必须将这段代码的两个方法进行同步处理，并且在调用connect的地方需要进行同步处理,这样将会大大影响程序执行效率，因为一个线程在使用connect进行数据库操作的时候，其他线程只有等待。

- 还有再试想下这个connect对象到底需不需要同步？不管是谁来getConnection方法都是为了得到一个数据库的连接,其实这种场景是不需要同步的;那么我们既需要保证线程安全又不需要同步的话使用ThreadLocal还是比较合适的,多线程多实例,确保线程封闭性。

改造一下代码:

```
public class DBUtil {
     
  private static final ThreadLocal<Connection> conn = new ThreadLocal<>();

    public static Connection getConnection() {
        Connection con = conn.get();
        if (con == null) {
            try {
                Class.forName("com.mysql.jdbc.Driver");
                con = DriverManager.getConnection("url", "root", "root");
                conn.set(con);
            } catch (Exception e) {
                // ...
            }
        }
        return con;
    }


	public static void close() {
		Connection con = conn.get();
        if(con !=null){
            con.close();
        }
    }
}
```

这样子，每个线程都有自己的数据库连接（当然,正规的应用应该要加连接池限制资源之类的）,就不会产生那样的冲突了。还有由于在每个线程中都创建了副本，所以要考虑它对资源的消耗。


写的还比较粗糙,如果我的理解或者代码有不正确的地方,还望指正。