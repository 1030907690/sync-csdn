---
layout:					post
title:					"element ui table显示本地图片"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 背景：后端返回一个状态码，需要根据状态码显示对应的本地图片。
- 第一步：写column。
	- <font color="red">注意前面要加一截路径，比如这里../assets/</font>
```html
<el-table :data="tableData" border style="width: 80%"  >
...省略...
	<el-table-column prop="warningLevel" label="预警等级">
		   <!-- 图片的显示 -->
			 <template   slot-scope="scope">            
				 <el-image   :src="require('../assets/'+scope.row.warningLevel)"   /> 
			 </template> 
	</el-table-column>
...省略...
</el-table>

```

- 第二步：填充模拟数据。

```html
  var alarmMap = new Array();
  alarmMap[0] = "logo.png";
export default {
  data() {
    return {
      tableData: [
        {
          id: 1,
          hull: "目标船体",
          behavior: "行为类别",
          area: "行为区域",
          equipmentNmea: "监控设备名称",
          date: "发生时间",
          speed: "传速",
          duration: "已停留时长",
          warningLevel:  alarmMap[0]
        }
      ]
    };
  },
```
- 最终效果如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e5f579c20e2127b3448efd794e328185.png#pic_center)
