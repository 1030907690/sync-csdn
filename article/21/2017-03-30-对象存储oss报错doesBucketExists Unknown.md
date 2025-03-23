---
layout:					post
title:					"对象存储oss报错doesBucketExists Unknown"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
当第二次去调用时报错，原因是我封装的java api问题

   public static OSSClient ossClient = null;
不能封装为静态的

正确的应该是这样

    /**
     * 上传
     * uploadType 上传类型
     * 
     * directoryPath 保存到oss的绝对路径
     * 
     * contentOrPath 内容或者是地址
     * */
    public static void upload(String uploadType,String directoryPath,String contentOrPath){
    	
    	OSSClient oss_Client = new OSSClient(endpoint, accessKeyId, accessKeySecret);
    	new AliyunOSSClient().createBucket(oss_Client);
    	// Object是否存在
    	boolean found = oss_Client.doesObjectExist(bucketName,directoryPath );
    	if(found)return;
    	if(AliyunOSSClient.STIRNGPYTE.equals(uploadType)){    		// 上传字符串
    		oss_Client.putObject(bucketName, directoryPath, new ByteArrayInputStream(contentOrPath.getBytes()));
    	}else if(AliyunOSSClient.FILEPYTE.equals(uploadType)){// 上传本地文件
    		oss_Client.putObject(bucketName,directoryPath , new File(contentOrPath));
    	}else if (AliyunOSSClient.NETWORKTYTE.equals(uploadType)){//上传网络流
			try {
				InputStream inputStream = new URL(contentOrPath).openStream();
				oss_Client.putObject(bucketName, directoryPath, inputStream);
			} catch (MalformedURLException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
    		
    	}
    	oss_Client.shutdown();

    }

写在里面

​