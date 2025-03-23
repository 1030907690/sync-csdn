---
layout:					post
title:					"Kotlin java.lang.abstractmethoderror Error:Kotlin: [Internal Error] java.lang.IllegalStateException:"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 具体异常:

```
 Error:Kotlin: [Internal Error] java.lang.IllegalStateException: The provided plugin org.jetbrains.kotlin.scripting.compiler.plugin.ScriptingCompilerConfigurationComponentRegistrar is not compatible with this version of compiler at org.jetbrains.kotlin.cli.jvm.compiler.KotlinCoreEnvironment.<init>(KotlinCoreEnvironment.kt:181) at 
```

- 这是kotlin插件版本问题，`在idea 工具中File->Settings->Plugins输入Kotlin,点击Browse repositories去升级`