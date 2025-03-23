---
layout:					post
title:					"SparkStreaming例子"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
我用的是spark1.6.3这是sparkStreaming的官方文档http://spark.apache.org/docs/1.6.3/streaming-programming-guide.html

概述：

Spark streaming是Spark核心API的一个扩展，它对实时流式数据的处理具有可扩展性、高吞吐量、可容错性等特点。我们可以从kafka、flume、Twitter、 ZeroMQ、Kinesis等源获取数据，也可以通过由 高阶函数map、reduce、join、window等组成的复杂算法计算出数据。最后，处理后的数据可以推送到文件系统、数据库、实时仪表盘中。事实上，你可以将处理后的数据应用到Spark的机器学习算法、 图处理算法中去。



在内部，它的工作原理如下图所示。Spark Streaming接收实时的输入数据流，然后将这些数据切分为批数据供Spark引擎处理，Spark引擎将数据生成最终的结果数据。



Spark Streaming支持一个高层的抽象，叫做离散流(discretized stream)或者DStream，它代表连续的数据流。DStream既可以利用从Kafka, Flume和Kinesis等源获取的输入数据流创建，也可以 在其他DStream的基础上通过高阶函数获得。在内部，DStream是由一系列RDDs组成。

代码：SparkStreamingTest.scala

package Test2

import org.apache.spark.{HashPartitioner, SparkConf}
import org.apache.spark.streaming.dstream.ReceiverInputDStream
import org.apache.spark.streaming.{Seconds, StreamingContext}

/**
  * Created by zhouzhongqing on 2017/2/8 0008.
  */
object SparkStreamingTest {
  def main(args: Array[String]): Unit = {

    // Create a local StreamingContext with two working thread and batch interval of 1 second.
    // The master requires 2 cores to prevent from a starvation scenario.
    val conf = new SparkConf().setMaster("local[2]").setAppName("NetworkWordCount");
    val ssc = new StreamingContext(conf, Seconds(5));//批次处理间隔时间5秒
    ssc.checkpoint("d:/ck");//记录点，记录上次执行到什么地方
    // Create a DStream that will connect to hostname:port, like localhost:8090
    //获取数据
    val dStream: ReceiverInputDStream[String] = ssc.socketTextStream("192.168.16.130",8090);

    //(hello,Seq<1,1,1>,10)
    val updateFunc = ( iterator: Iterator[(String ,Seq[Int],Option[Int])]) => {
      iterator.map(t =>(t._1, t._2.sum + t._3.getOrElse(0)))//次数累加
    };

    //以DStream中的数据进行按key做reduce操作，然后对各个批次的数据进行累加
    val result = dStream.flatMap(_.split(" ")).map((_, 1)).updateStateByKey(updateFunc,
      new HashPartitioner(ssc.sparkContext.defaultParallelism),true);
    result.print();
    ssc.start()             // Start the computation
    ssc.awaitTermination()  // Wait for the computation to terminate
    // nc -lk 8090

  }
}
运行：

先在在主机上安装nc

yum -y install nc

启动程序

输入数据：



查看结果


 



​