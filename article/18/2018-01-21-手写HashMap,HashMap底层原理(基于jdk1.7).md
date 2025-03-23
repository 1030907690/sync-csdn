---
layout:					post
title:					"手写HashMap,HashMap底层原理(基于jdk1.7)"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
一、首先我们来看HashMap的数据结构和数据结构上面存储的数据对象类型

 HashMap是一个存储数据（封装了K ,V属性的对象）的集合,这个集合是 数组+链表类型的数据结构,存在上面 的数据对象就是封装了 K V对象

       

  解析：

1、HashMap首先初始化一个默认长度的数组

2、调用put保存数据时使用hashCode算法散列到数组的某个位置去存储(为避免散列的位置重复太多,还应该检查这个数组是否应该扩容)

        3、如果散列到的位置已经有数据了，会形成一个链表结构，新的数据会放前面(get区的时候就取得最新的一条)，旧的数据就压在下面

二、代码实现

1、定义一个接口

IMap.java 实现基本功能

 

package com.zzq.test.map;

/**

 * @author zhouzhongqing

 * 2017年11月10日22:57:09

 * map接口

 * */
public interface IMap<K, V> { 

	/**

	 * zhouzhongqing

	 * 2017年11月15日16:34:34

	 * 保存的方法

	 * @param k 键

	 * @param v 值

	 * @return V 返回插入的值

	 * */
	V put(K k,V v); 
	
	/**

	 * zhouzhongqing

	 * 2017年11月15日16:34:34

	 * 通过key得到value的方法

	 * @param k 键

	 * @return V 返回value

	 * */
	V get(K k);
	
	
	/**

	 * zhouzhongqing

	 * 2017年11月15日16:39:42

	 * 得到已使用的长度

	 * @return 返回已使用的长度

	 * */
	int getUseSize();
	
	/**

	 * zhouzhongqing

	 * 2017年11月15日16:39:42

	 * 得到当前的默认长度

	 * @return 返回当前的默认长度

	 * */
	int getDefaulLength();
	
	 public interface Entry<K,V>{
		 public K getKey();
		 public V getValue();
	 }
	 
}
2、定义实现类 

MyHashMap.java

package com.zzq.test.map;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.dom4j.IllegalAddException;


/**

 * @author zhouzhongqing

 * 2017年11月10日22:59:12

 * 自定义HashMap实现类

 * */
public class MyHashMap<K, V> implements IMap<K, V> {
	
	//默认的数组长度1 << 4 为 16

	/**

	 * 位移运算计算方法

	 *	1 % 2 = 1

	 * 把结果反过来为1

	 * (java中，整数默认就是int类型,也就是32位) 最后得 ：0000 0000 0000 0000 0000 0000 0000 0001  然后将结果向左移动4位得到: 0000 0000 0000 0000 0000 0000 0001 0000

	 * 最后将二进制转为十进制得 ： 16

	 * * */
	private static int defaulLength = 1 << 4;
	
	//增长因子

	private static double defaultAddSizeFactor = 0.75; 
	
	//已用数组的长度

	private int useSize;
	
	//Entry数组

	private Entry<K,V> [] table = null;
	
	public MyHashMap() {
		this(defaulLength,defaultAddSizeFactor);
	}
	
	/**

	 * 门面模式

	 * **/
	public MyHashMap(int length,double defaultAddSizeFactor){
		if(length <= 0 || defaultAddSizeFactor <= 0){
			throw new NullPointerException("MyHashMap error");
		}
		this.defaulLength = length;
		this.defaultAddSizeFactor = defaultAddSizeFactor;
		table = new Entry[defaulLength];
	}


	@Override
	public V put(K k, V v) {
		//判断是否应该扩容

		if(useSize > defaultAddSizeFactor * defaulLength){
			//超过了负载因子，扩容

			up2Size();
		}
		//通过自定义的hash算法得到数组中的一个位置

		int index = getIndex(k,table.length);
		Entry<K, V> entry = table[index];
		//如果散列到的位置还没有元素

		if(null == entry){ 
			table[index] = new Entry<K, V>(k, v, null);
			useSize++;
		}else if (null != entry ){
			//如果散列到的位置已经有了元素,把这个元素存为链表 next,把以前的entry元素放下面,新添加的元素在最顶上

			table[index] = new Entry<K, V>(k, v, entry);
		}
		return (V) table[index].getValue();
	}

	/**

	 * 通过自定义的hash算法得到一个介于数组长度defaulLength之间的位置

	 * */
	private int getIndex(K k, int length) {
		int m = length - 1;
		int index = hash(k.hashCode() & m);
		return index;
	}

	/***

	 * zhouzhongqing

	 * 2017年11月15日16:19:54

	 * 自定义hash算法 寻找散列位置

	 * @param hashCode

	 * */
	private int hash(int hashCode) {
		hashCode = hashCode^((hashCode>>>20)^(hashCode>>>12));
		return hashCode^((hashCode>>>7)^(hashCode>>>4));
	}

	/***

	 * zhouzhongqing

	 * 2017年11月15日16:30:51

	 * 扩容Entry数组

	 * */
	private void up2Size() {
		againHah();
	}

	private void againHah() {
		//将所有的数据全部遍历出来,如果是链表就递归遍历 放在list中

		List<Entry<K, V>> entryList = new ArrayList<MyHashMap<K, V>.Entry<K,V>>();
		for (int i = 0; i < table.length; i++) {
			//忽略为空的数组节点

			if(null == table[i]){
				continue;
			}
			foundEntryByNext(table[i],entryList);
		}
		
		
		if(entryList.size() > 0){
			useSize = 0;
			defaulLength = 2 * defaulLength;
			//已经达到扩容因子,为了减少散列位置的冲突(如果冲突很多,形成的链表必然很大,链表查询起来是非常慢的),数组的长度增加2倍

			table = new Entry[defaulLength];
			 
			for (Entry<K, V> entry : entryList) {
				if(entry.next != null){
					//所以的元素都在list中可以把entry下面的链表移除掉

					entry.next = null;
				}
				put(entry.getKey(), entry.getValue());
			}
		}
	}

 
	/***

	 * 递归将老table中的数据添加到list中

	 * **/
	private void foundEntryByNext(MyHashMap<K, V>.Entry<K, V> entry, List<MyHashMap<K, V>.Entry<K, V>> entryList) {
		if(entry != null && entry.next != null ){
			//如果这个entry是个链表并且还有下一个元素就递归调用得到下一个元素添加到list中

			entryList.add(entry);
			foundEntryByNext(entry.next, entryList);
		}else{
			//如果这个散列位置只有一个元素没有形成链表直接添加到list中就可以了

			entryList.add(entry);
		}
	}

	@Override
	public V get(K k) {
		//通过和put方法同样的hash算法得到位置

		int index = getIndex(k,table.length);
		if(table[index] == null){
			throw new NullPointerException("没有这个key");
		}
		Entry<K, V> entry = table[index];
	    return findValueByEqualKey(k,entry);
	}
	


	/***

	 * 递归得到map,如果是保存有重复的key取最新的一条元素

	 * **/
	private V findValueByEqualKey(K k, MyHashMap<K, V>.Entry<K, V> entry) {
		System.out.println(  " next : "+ (null == entry.next));
		if(k == entry.getKey() || k.equals(entry.getKey())){
			return entry.getValue();
		}else if(null != entry.next ){
			return findValueByEqualKey(k, entry.next);
		}
		return null;
	}
	
	@Override
	public int getUseSize() {
		return useSize;
	}


	@Override
	public int getDefaulLength() {
		return defaulLength;
	}




/***

 * 以链表的方式存储散列到有冲突的位置,把以前的entry元素放下面,新添加的元素在最顶上

 * */
class Entry<K,V> implements IMap.Entry<K, V>{

	K k;
	V v;
	Entry<K,V> next;
	
	public Entry(K k,V v,Entry<K,V> next) {
		this.k = k;
		this.v = v;
		this.next = next;
	}
	
	@Override
	public K getKey() {
		return k;
	}

	@Override
	public V getValue() {
		return v;
	}
	
}




public static void main(String[] args) {
	/*new MyHashMap().a();*/
	
}



/*	private  Map<String, Map<Integer, String>> map = new HashMap<>();*/

/*public void a(){

	Map<Integer,String > m2 = new HashMap<Integer, String>();

	m2.put(1,"2");

	map.put("test", m2);

	

	System.out.println(map);

	

	Map<Integer,String > m3 = map.get("test");

	m3.put(2, "test2");

	System.out.println(map);

}

*/
}
 3、测试类

package com.zzq.test.map;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;


/**

 * zhouzhongqing

 * 2017年11月15日16:17:18

 * 测试类

 * **/
public class Test {

	public static void main(String[] args) {
		IMap<String, Integer> map = new MyHashMap<>();
		for(int i = 0; i< 101 ;i++){			
			map.put("zs"+i, i);
		}
		System.out.println(map.get("zs100") + " useSize :" + map.getUseSize() + " defaulLength: " +map.getDefaulLength());
		
	}
}
测试结果：


  

userSize : 占用数组长度 18个   总的数据长度32个  

好了，一个精简版的HashMap就这样完成了

​