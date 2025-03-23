---
layout:					post
title:					"android上传图片到javaweb服务端，android+和struts2"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
客户端代码：

HttpAssist.java

package com.sevnce.apps.phone.modelall.actionall;


import java.io.BufferedReader;  
import java.io.DataOutputStream;  
import java.io.File;  
import java.io.FileInputStream;  
import java.io.IOException;  
import java.io.InputStream;  
import java.io.InputStreamReader;  
import java.io.OutputStream;  
import java.net.HttpURLConnection;  
import java.net.MalformedURLException;  
import java.net.URL;  
import java.util.UUID;  

import org.apache.http.HttpVersion;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.FileEntity;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.params.CoreProtocolPNames;
  
  
public class HttpAssist {  
    private static final String TAG = "uploadFile";  
    private static final int TIME_OUT = 10 * 10000000; // 超时时间  
    private static final String CHARSET = "utf-8"; // 设置编码  
    public static final String SUCCESS = "1";  
    public static final String FAILURE = "0";  
  
    public static String uploadFile(File file) {  
        String BOUNDARY = UUID.randomUUID().toString(); // 边界标识 随机生成  
        String PREFIX = "--", LINE_END = "\r\n";  
        String CONTENT_TYPE = "multipart/form-data"; // 内容类型  
        String RequestURL = "http://localhost:8080/phone/phone_account!updateUserInfo.do?userId=7&updateType=headPhoto";  
        try {  
            URL url = new URL(RequestURL);  
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();  
            conn.setReadTimeout(TIME_OUT);  
            conn.setConnectTimeout(TIME_OUT);  
            conn.setDoInput(true); // 允许输入流  
            conn.setDoOutput(true); // 允许输出流  
            conn.setUseCaches(false); // 不允许使用缓存  
            conn.setRequestMethod("POST"); // 请求方式  
            conn.setRequestProperty("Charset", CHARSET); // 设置编码  
            conn.setRequestProperty("connection", "keep-alive");  
            conn.setRequestProperty("Content-Type", CONTENT_TYPE + ";boundary="  
                    + BOUNDARY);  
            if (file != null) {  
                /** 
                 * 当文件不为空，把文件包装并且上传 
                 */  
                OutputStream outputSteam = conn.getOutputStream();  
  
                DataOutputStream dos = new DataOutputStream(outputSteam);  
                StringBuffer sb = new StringBuffer();  
                sb.append(PREFIX);  
                sb.append(BOUNDARY);  
                sb.append(LINE_END);  
                /** 
                 * 这里重点注意： name里面的值为服务器端需要key 只有这个key 才可以得到对应的文件 
                 * filename是文件的名字，包含后缀名的 比如:abc.png 
                 */  
  
                sb.append("Content-Disposition: form-data; name=\"headPhotoUrl\"; filename=\""  
                        + file.getName() + "\"" + LINE_END);  
                sb.append("Content-Type: application/octet-stream; charset="  
                        + CHARSET + LINE_END);  
                sb.append(LINE_END);  
                dos.write(sb.toString().getBytes());  
                InputStream is = new FileInputStream(file);  
                byte[] bytes = new byte[1024];  
                int len = 0;  
                while ((len = is.read(bytes)) != -1) {  
                    dos.write(bytes, 0, len);  
                }  
                is.close();  
                dos.write(LINE_END.getBytes());  
                byte[] end_data = (PREFIX + BOUNDARY + PREFIX + LINE_END)  
                        .getBytes();  
                dos.write(end_data);  
                dos.flush();  
                /** 
                 * 获取响应码 200=成功 当响应成功，获取响应的流 
                 */  
                int res = conn.getResponseCode();  
                if (res == 200) {  
                    return SUCCESS;  
                }  
            }  
        } catch (MalformedURLException e) {  
            e.printStackTrace();  
        } catch (IOException e) {  
            e.printStackTrace();  
        }  
        return FAILURE;  
    }  
    
    
    public static void main(String[] args) {
		File file = new File("C:/Users/sevnce/Desktop/QQ图片20170206211126.png");
		if(!file.exists()){
			System.out.println( "图片不存在");
		}
		HttpAssist.uploadFile(file);
	}
    
 
}  

Javaweb服务端代码：

	@Override
	public String uploadHeadPhoto(HttpServletRequest request) {
			// 文件保存目录路径
			String savePath = request.getSession().getServletContext().getRealPath("/") + "images/headPhoto/";

			// 文件保存目录URL
			String saveUrl = request.getContextPath() + "/images/headPhoto/";

			// 最大文件大小
			long maxSize = 1000000;
			// Struts2 请求 包装过滤器
			MultiPartRequestWrapper wrapper = (MultiPartRequestWrapper) request;
			// 获取上传文件名
			String fileName = wrapper.getFileNames("headPhotoUrl")[0];
			// 获得文件过滤器
			File file = wrapper.getFiles("headPhotoUrl")[0];
			// 得到上传文件的扩展名
			String fileExt = fileName.substring(fileName.lastIndexOf(".") + 1).toLowerCase();
			// 检查文件大小
			if (file.length() > maxSize) {
				return null;
			}

			// 检查目录
			File uploadDir = new File(savePath);
			if (!uploadDir.isDirectory()) {
//				ajaxPri(getError("上传目录不存在。"));
//				return null;
				uploadDir.mkdirs();
			}
			// 检查目录写入权限
			if (!uploadDir.canWrite()) {
				return null;
			}

			// 重构上传图片的名称
			SimpleDateFormat df = new SimpleDateFormat("yyyyMMddHHmmss");
			String newImgName = df.format(new Date()) + "_" + new Random().nextInt(1000) + "." + fileExt;

			// 设置 KE 中的图片文件地址
			String newFileName = request.getScheme() + "://" + request.getServerName() + ":" + request.getServerPort() + saveUrl + newImgName;

			byte[] buffer = new byte[1024];

			FileOutputStream fos = null;
			InputStream in = null;
			try {
				// 获取文件输出流
				fos = new FileOutputStream(savePath + newImgName);
				// 获取内存中当前文件输入流
				in = new FileInputStream(file);

				int num = 0;
				while ((num = in.read(buffer)) > 0) {
					fos.write(buffer, 0, num);
				}
			} catch (Exception e) {
				e.printStackTrace();
				return null;
			} finally {
				try {
					in.close();
					fos.close();
				} catch (Exception e) {
					e.printStackTrace();
				}
			}

			return "/images/headPhoto/" + newImgName;
	}
调用直接传个request过来就行了

​