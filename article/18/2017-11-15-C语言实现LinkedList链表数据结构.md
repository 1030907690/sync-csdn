---
layout:					post
title:					"C语言实现LinkedList链表数据结构"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
####链表基本的就是一个数据域一个指针域，数据域存储你的数据，指针域就指向你下一个节点的内存地址。
示意图(画的很粗糙,请见谅)
![这里写图片描述](https://img-blog.csdn.net/20171115214721095?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYmFpZHVfMTk0NzM1Mjk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 - **链表的特点：**
	 - 增删快 (修改元素时，只需要改变指针域指向就可以了)
	 - 查询慢 (元素之前内存地址不连续，只能挨个挨个遍历查找)

###我们现在就来实现一个非循环单链表
- **首先写出链表的结构体：**

```
typedef struct Node{ //非循环单链表结构体
	int data; //数据区域

	Node * pNext; // 指针指向下一个节点

	
} NODE,*PNODE;
```

- **然后我们初始化出一个头结点**

```
 PNODE initLinkedList(){
	
	
	PNODE pHead = (PNODE)malloc(sizeof(NODE));//头结点不存放数据
	
	if( NULL == pHead ){
		printf("%s\n","动态分配内存失败，程序退出");
		exit(-1);
	}
	
	pHead->pNext = NULL;
	
	return pHead;
}
```

- **然后再是添加新节点的方法**

```
PNODE addElement(PNODE pTail,int val){
 
	PNODE pNew = (PNODE)malloc(sizeof(NODE)); //创建新节点
	if(NULL == pNew ){
		printf("%s\n","追加节点动态分配内存失败，退出程序");
		exit(-1);
	}

	
	pNew->data = val; //给新节点赋值
	pNew->pNext = NULL; //新节点的下一个节点为NULL
	pTail->pNext = pNew; // 将pNew节点挂在pTail后面
	length += 1;//节点有效个数加1
	
	return pNew;//返回最后一个节点
}

```

- **遍历链表**

```

bool isEmpty(PNODE pNode){

	if(NULL == pNode->pNext){
		printf("%s\n","pNode is null");
		return true;
	}

	return false;
}

void loopElement(PNODE pNode){
	if(isEmpty(pNode)){
		return;//为空直接返回
	}

	PNODE p = pNode->pNext;
	printf("%s\n","start loop");
	
	while(NULL != p){
		printf("%d\n",p->data);
		p = p->pNext;
	}
	
	printf("%s\n","end loop");
	
}
```

- **然后在加一个main方法测试**
	- 记得要加入这三个头文件运行

```
#include <stdio.h> /* 基础头文件*/
#include <malloc.h> /*动态分配内存头文件*/
#include <stdbool.h>  /*返回布尔值的头文件*/
```


```

int main(){
	printf("%s\n" ,"start");
	
	PNODE  pHead = initLinkedList();

	/*addElement start */
	
	PNODE node = addElement(pHead,1);//追加到pHead节点下
	PNODE node2 = addElement(node,2);//追加到node节点下
	PNODE node3 = addElement(node2,4);//......
	PNODE node4 = addElement(node3,3);//......
	
	/*addElement end */
	
	loopElement(pHead);

	printf("length: %d\n",length);
 
	
	printf("%s\n" ,"end");
	//getchar();
  return 0;	
}
```
此时一个非循环单链表的功能基本上有了，现在附上全部的代码：
LinkedList.c

```
#include <stdio.h> /* 基础头文件*/
#include <malloc.h> /*动态分配内存头文件*/
#include <stdbool.h>  /*返回布尔值的头文件*/


/***
*zhouzhongqing
*链表List
*2017年10月28日14:56:19
*/



typedef struct Node{ //非循环单链表结构体
	int data; //数据区域

	Node * pNext; // 指针指向下一个节点

	
} NODE,*PNODE;


PNODE last; //声明每次添加节点后的最后一个节点


	
int length; //节点有效个数

/***
*方法声明
**/

/**
*初始化，动态分配内存
**/
PNODE initLinkedList();

/***
*添加节点
**/
PNODE addElement(PNODE pTail,int val);

/***
*添加节点 使用声明最后一个节点的方式
**/
void addElementLast(PNODE pTail,int val);


/**
*遍历所有节点
**/
void loopElement(PNODE pNode);


/***
*测试添加节点
**/
PNODE addElementTest();


/**
*判断是否为空         空返回true 非空返回 false
*/
bool isEmpty(PNODE pNode);


/**
*排序 ,冒泡排序
**/
void sortList(PNODE pNODE);



/**
*检查输入的下标是否越界 越界返回false 否则为成功true
*/
bool checkElementIndex(int index);



/**
*通过下标获取节点 从0开始
**/
PNODE get(PNODE pNode,int index);





int main(){
	printf("%s\n" ,"start");
	
	PNODE  pHead = initLinkedList();

	/*addElement start */
	/*
	PNODE node = addElement(pHead,1);//追加到pHead节点下
	PNODE node2 = addElement(node,2);//追加到node节点下
	PNODE node3 = addElement(node2,4);//......
	PNODE node4 = addElement(node3,3);//......
	*/
	/*addElement end */
	

	/*addElementLast start */
	addElementLast(pHead,1);
	addElementLast(pHead,5);
	addElementLast(pHead,8);
	addElementLast(pHead,4);

	/*addElementLast end */


	//排序
	sortList(pHead);


 		
	
	loopElement(pHead);


	//get 
	//PNODE node = get(pHead,4);
	//printf("node->data : %d\n",node->data);

	
	printf("length: %d\n",length);
	
	
	
	//loopElement(addElement2());
	
	printf("%s\n" ,"end");
	//getchar();
  return 0;	
}




bool checkElementIndex(int index){
	 return index >= 0 && index < length;
}





void sortList(PNODE pNODE){
	if(isEmpty(pNODE)){
		return ;
	}

	int i,j,t;

	PNODE p,q;

	 for(i=0,p=pNODE->pNext;i<length-1;++i,p=p->pNext){
	 	printf("p->data-1 : %d,%d\n",p->data,p->data);
		for(j=i+1,q=p->pNext;j<length;++j,q=q->pNext) {
	 		printf("q->data-2 :%d,%d\n",q->data,q->data);
             if(p->data>q->data) {//类似于数组中的：a[i]>a[j]
             		//数据位置相互转换，大的p->data放在后面的位置 小的q->data放在前面的位置
                     t=p->data;//类似于数组中的：     t=a[i];
                     p->data=q->data;//类似于数组中的： a[i]=a[j];
                     q->data=t;//类似于数组中的：     a[j]=t;
            }
         }
	 }

	 //loopElement(pNODE);

}


PNODE get(PNODE pNode, int index){

	 if(isEmpty(pNode)){
		return NULL;
	 }
	 
	 if(!checkElementIndex(index)){
	 	printf("%s index = %d\n","index outOf bounds exception :" ,index);
		return NULL;
	 }
	
	 int i = 0;
     PNODE p = pNode;

     while(NULL!=p->pNext&&i<index)
     {
           p=p->pNext;
           ++i;
     }


	 PNODE q = p->pNext;
		
	return q;
}






bool isEmpty(PNODE pNode){

	if(NULL == pNode->pNext){
		printf("%s\n","pNode is null");
		return true;
	}

	return false;
}




void addElementLast(PNODE pTail,int val){
	if(NULL != last){
		pTail = last;
	//	printf("%s\n", "如果不是添加第一个数据节点pTail改为最后一个节点");
	}
 
	PNODE pNew = (PNODE)malloc(sizeof(NODE));//创建新节点
	if(NULL == pNew ){
		printf("%s\n","addElementJDK方法追加节点动态分配内存失败，退出程序");
		exit(-1);
	}

	pNew->data = val; //给新节点赋值
	pNew->pNext = NULL; //新节点的下一个节点为NULL
	pTail->pNext = pNew; // 将pNew节点挂在pTail后面
	length += 1;//节点有效个数加1
	
	last = pNew;//将节点置为最后一个节点，这个写法我参考的jdk7的LinkedList源码的基本思路
}



PNODE addElement(PNODE pTail,int val){
 
	PNODE pNew = (PNODE)malloc(sizeof(NODE)); //创建新节点
	if(NULL == pNew ){
		printf("%s\n","追加节点动态分配内存失败，退出程序");
		exit(-1);
	}

	
	pNew->data = val; //给新节点赋值
	pNew->pNext = NULL; //新节点的下一个节点为NULL
	pTail->pNext = pNew; // 将pNew节点挂在pTail后面
	length += 1;//节点有效个数加1
	
	return pNew;//返回最后一个节点
}


 

void loopElement(PNODE pNode){
	if(isEmpty(pNode)){
		return;//为空直接返回
	}

	PNODE p = pNode->pNext;
	printf("%s\n","start loop");
	
	while(NULL != p){
		printf("%d\n",p->data);
		p = p->pNext;
	}
	
	printf("%s\n","end loop");
	
}




 PNODE initLinkedList(){
	
	
	PNODE pHead = (PNODE)malloc(sizeof(NODE));//头结点不存放数据
	
	if( NULL == pHead ){
		printf("%s\n","动态分配内存失败，程序退出");
		exit(-1);
	}
	
	pHead->pNext = NULL;
	
	return pHead;
}



/**
*zhouzhongqing
*测试方法
*2017年10月31日14:01:32
**/

  PNODE addElementTest(){
	  
 
  
	   int len;//用来存放有效节点的个数
		  
	   int val = 1;//用来临时存放用户输入的节点的值
	   int val2 = 2;//用来临时存放用户输入的节点的值
	  //分配了一个不存放有效数据的头节点
	   PNODE  pHead = initLinkedList();
	   if(NULL==pHead)
	   {
				printf("分配失败，程序终止！\n");
				exit(-1);
	   }
	   PNODE pTail=pHead;
	   pTail->pNext=NULL;
	 
		PNODE pNew=(PNODE)malloc(sizeof(NODE));
		if(NULL==pNew)
		{
				 printf("分配失败，程序终止！\n");
				 exit(-1);
		}
		pNew->data=val;//挂
		pNew->pNext=NULL;
		pTail->pNext=pNew;
		pTail=pNew;
 		len++;
 
		
		 PNODE pNew2=(PNODE)malloc(sizeof(NODE));
		if(NULL==pNew2)
		{
				 printf("分配失败，程序终止！\n");
				 exit(-1);
		}
		pNew2->data=val2;//挂
		pNew2->pNext=NULL;
		pTail->pNext=pNew2;
		pTail=pNew;
		
		len++;
		
	 return pHead;
 }
 

```