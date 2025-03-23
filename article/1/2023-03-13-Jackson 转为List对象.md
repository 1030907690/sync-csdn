---
layout:					post
title:					"Jackson 转为List对象"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---


## 代码
### 第一种方法
```java
   @Test
    public void importProvince() throws IOException {

        String fileName = "C:\\Users\\Windows3\\Documents\\province.json";


        StringBuilder sb = new StringBuilder();
        // 转换成List<String>, 要注意java.lang.OutOfMemoryError: Java heap space
        List<String> lines = Files.readAllLines(Paths.get(fileName),
                StandardCharsets.UTF_8);
        lines.forEach(val -> sb.append(val));
        System.out.println(sb.toString());
		//objectMapperFace 是装饰器 里面是ObjectMapper 
        ObjectMapper objectMapper = objectMapperFace.getObjectMapper();
        List<Pos> posList = objectMapper.readValue(sb.toString(), getCollectionType(List.class,Pos.class));
        System.out.println(posList);


        int dictValue = 1;
 

        for (Pos pos : posList) {
            List<City> citys = pos.getCity();
            for (City city : citys) {
                for (String area : city.getArea()) {
                    System.out.println(area);
                }
            }
        }
    }

   /*
     * 获取泛型的Collection Type
     * @param collectionClass 泛型的Collection
     * @param elementClasses 元素类
     * @return JavaType Java类型
     * @since 1.0
     */
    public JavaType getCollectionType(Class<?> collectionClass, Class<?>... elementClasses) {
        return objectMapperFace.getObjectMapper().getTypeFactory().constructParametricType(collectionClass, elementClasses);
    }
```
### 第二种方法 

```java
  TypeReference<List<Pos>> typeReference = new TypeReference<List<Pos>>() {
        };
        ObjectMapper objectMapper = objectMapperFace.getObjectMapper();
        List<Pos> posList = objectMapper.readValue(sb.toString(), typeReference);
```

### 效果
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ef8591f377628e4500f20fdd614e7be5.png)


## 遇到的问题
- Jackson  from Array value (token `JsonToken.START_ARRAY`)
> JSON数据和实体的字段结构不一致导致的。我是因为city字段是数组，而实体写成了对象才报这个错。
- non-static inner classes like this can only by instantiated using default, no-argument constructor
> 出现在内部类中，类上要加`static`关键字。

