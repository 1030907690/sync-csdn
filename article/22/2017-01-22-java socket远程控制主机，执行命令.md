---
layout:					post
title:					"java socket远程控制主机，执行命令"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
socket server服务端代码

package com.core.servers;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashSet;

/**
 * @author zzq
 *服务端
 */
public class Servers extends Thread {
	
	Socket socket ;
	
	//使用该集合是用于存储ip地址的。
	static HashSet<String> ips = new HashSet<String>();
	
	public  Servers(Socket socket) {
		this.socket = socket;
	}
	
	@Override
	public void run() {
		try {
			String ip = socket.getInetAddress().getHostAddress();   // socket.getInetAddress() 获取对方的IP地址
			if(ips.add(ip)){
				System.out.println("恭喜"+ip+"同学成功连接，当前下载的人数是："+ ips.size());
			}
		    DataInputStream in = new DataInputStream(socket.getInputStream());
            System.out.println(in.readUTF());//这里 打印的是客户端发送的第0个writeUTF，搞了好久才发现这个问题
            String exeResult = exeCmd(in.readUTF());//这里是第一个 就是输入的cmd
            DataOutputStream out = new DataOutputStream(socket.getOutputStream());
            out.writeUTF("返回执行结果： "   + exeResult + " \t Goodbye!");
			socket.close();
		}catch (IOException e) {
			e.printStackTrace();
		}
	}
	public static void main(String[] args) throws IOException {
		//建立tcp的服务 ,并且要监听一个端口
		ServerSocket serverSocket  = new ServerSocket(9090);//9090端口号
		System.out.println("等待客户端连接....");
		while(true){
			//不停的接受用户的链接。
			Socket socket = serverSocket.accept();
			new Servers(socket).start();
		}
	}
	
	 /**
     * @param commandStr
     * @return 
     * 调用dos命令
     */
    public static String exeCmd(String commandStr) {  
        BufferedReader br = null;  
        try {  
        	StringBuilder sb = new StringBuilder();  
	            Process p = Runtime.getRuntime().exec(commandStr);  
            br = new BufferedReader(new InputStreamReader(p.getInputStream()));  
            String line = null;  
            while ((line = br.readLine()) != null) {  
                sb.append(line + "\n");  
            }  
	         //   System.out.println(sb.toString());  
        	sb.append(commandStr);
           return sb.toString();
        } catch (Exception e) {  
            return null;
        }   
        finally  
        {  
            if (br != null)  
            {  
                try {  
                    br.close();  
                } catch (Exception e) {  
                    e.printStackTrace();  
                }  
            }  
        }  
    }  
}
client代码

package com.core.client;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;

/**
 * @author zzq
 *客户端
 */
public class Client {
	  public static void main(String [] args) throws UnknownHostException  
      {  
         InetAddress serverName = InetAddress.getLocalHost();//这是ip地址，建议写配置文件  
         int port = 9090;//这是端口  
         try  
         {  
           Socket client = null;
           while (true) {  
            client = new Socket(serverName, port);  
            System.out.println("................请输入命令..................");  
            Scanner sc = new Scanner(System.in);  
            String cmdStr = sc.nextLine();  
            OutputStream outToServer = client.getOutputStream();  
            DataOutputStream out = new DataOutputStream(outToServer);  
            out.writeUTF("\n");  
            out.writeUTF(cmdStr);  
            client.shutdownOutput();  
            InputStream inFromServer = client.getInputStream();  
            DataInputStream in = new DataInputStream(inFromServer);  
            System.out.println(" 读取服务器返回" + in.readUTF());  
            client.close();  
           }  
         }catch(IOException e)  
         {  
            e.printStackTrace();  
         }  
      } 
}

可以多客户端,运行效果







​