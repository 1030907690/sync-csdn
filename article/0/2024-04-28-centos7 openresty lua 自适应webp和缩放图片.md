---
layout:					post
title:					"centos7 openresty lua 自适应webp和缩放图片"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
##  背景
- 缩小图片体积，提升加载速度，节省流量。

## 效果图
- 参数格式 ： ?image_process=format,webp/resize,p_20
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ebf288b0284c7d9e707c798c345b44a8.png)


![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4f1d30ce6670b123f1ccb0864b82b5ff.png)


## 准备
### 安装`cwebp`等命令，转换文件格式

```
yum install  libwebp-devel libwebp-tools
```
### 安装`ImageMagick`，压缩文件

```
yum install  ImageMagick
```
### 下载Lua API 操控ImageMagick的依赖包

 - 网址：[https://github.com/leafo/magick](https://github.com/leafo/magick)，到Releases下载，解压后得到如下：
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fa66df15b8376467808279f0cbfb9a23.png)
- 复制`magick`包到`lualib`里，如下所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6e5ff64e02c1452edce69209ea9fa947.png)

## 代码

- 修改conf文件，添加如下内容。

```
      location ~ \.(jpe?g|png|gif)$ {
  		     add_header Access-Control-Allow-Origin *;
              add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
               add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
               content_by_lua_file /usr/local/openresty/nginx/conf/lua/image-convert.lua;
        }
```

- 创建`/usr/local/openresty/nginx/conf/lua/image-convert.lua` 文件。添加一下内容。

```lua



local originalFile = ngx.var.request_filename
 

local image_process = ngx.var.arg_image_process
-- local image_process = ngx.req.get_uri_args()["image_process"]

function fileExists(name)
  local f=io.open(name,"r")
  if f~=nil then io.close(f) return true else return false end
end

function tryServeFile(name, contentType)
    if fileExists(name) then
        local f = io.open(name, "rb")
        local content = f:read("*all")
        f:close()
        if contentType ~= "" then
            ngx.header["Content-Type"] = contentType
        end
        ngx.print(content)
        return true
    end
    return false
end

function serveFileOr404(name, contentType)
    if not tryServeFile(name, contentType) then
        ngx.exit(404)
    end
end


function ratioZip(originalFile,ratioFile) 
	if not fileExists(ratioFile) then
		local ratio_num = string.match(image_process, "%d+")
		local magick = require("magick")
		local img = assert(magick.load_image(originalFile))
		local r_num = tonumber(ratio_num) / 100
		local w = img:get_width() * r_num
		local h = img:get_height() * r_num
		img:destroy()
		
		local size_str = tostring(math.floor(w)) .. "x" .. tostring(math.floor(h))
		magick.thumb(originalFile, size_str , ratioFile)
	end
		

end

function outputWebp(originalFile,commandExe)
	 
	local newFile = originalFile .. ".converted.webp"
	local headers = ngx.req.get_headers()
	if headers ~= nil and headers["accept"] ~= nil and string.find(headers["accept"], "image/webp") ~= nil then
		if not tryServeFile(newFile, "image/webp") then
			 os.execute(commandExe .. " -q 80 " .. originalFile .. " -o " .. newFile);
			 serveFileOr404(originalFile, "image/webp")
		end
	elseif image_process ~= nil and string.find(image_process, "webp") ~= nil then
		if not tryServeFile(newFile, "image/webp") then
			 os.execute(commandExe .. " -q 80 " .. originalFile .. " -o " .. newFile);
			 serveFileOr404(originalFile, "image/webp")
		end
	else
		serveFileOr404(originalFile, "")
	end

end

function zipAndWebp(originalFile,commandExe)

	
	
	--ngx.header["Content-Type"] = "text/html; charset=UTF-8"
    --ngx.say("imgp ",image_process,string.find(image_process, "resize")," 比例 ",number)
    local ratio_num = nil
    if image_process ~= nil and string.find(image_process, "resize") ~= nil then
		ratio_num = string.match(image_process, "%d+")
    end
   
	-- ngx.say("imgp ",ratio_num)
	 
	-- 是否要压缩
	if  ratio_num ~= nil and tonumber(ratio_num) > 0 then
		local ratioFile = originalFile .. ratio_num
		ratioZip(originalFile,ratioFile) 
		outputWebp(ratioFile,commandExe)
	else
		outputWebp(originalFile,commandExe)
	end
	
	
	
	
end

 
if string.find(originalFile, ".png") ~= nil then
   
   zipAndWebp(originalFile,"cwebp")
elseif string.find(originalFile, ".jpg") ~= nil then
	 zipAndWebp(originalFile,"cwebp")
elseif string.find(originalFile, ".jpeg") ~= nil then
	 zipAndWebp(originalFile,"cwebp")
elseif string.find(originalFile, ".gif") ~= nil then
	 outputWebp(originalFile,"gif2webp")
else 
	serveFileOr404(originalFile, "")
end

```
- 参数格式

```
?image_process=format,webp/resize,p_20
```



## 参考
- [https://blog.rexskz.info/use-openresty-to-optimize-image-size-with-avif-and-webp.html](https://blog.rexskz.info/use-openresty-to-optimize-image-size-with-avif-and-webp.html)
- [https://blog.csdn.net/F_angT/article/details/90073211](https://blog.csdn.net/F_angT/article/details/90073211)
- [https://www.jianshu.com/p/b14c89b57493](https://www.jianshu.com/p/b14c89b57493)