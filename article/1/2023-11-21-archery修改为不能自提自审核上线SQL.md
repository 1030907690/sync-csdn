---
layout:					post
title:					"archery修改为不能自提自审核上线SQL"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 背景
- 我和同事都可以提交上线SQL，但是不能自己提交的SQL自己去审核通过。
- 目前的情况是可以自提自审。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1106858f814de8f106834c0e4815e9a6.png)
## 修改代码
- 找到`/opt/archery/sql/utils/workflow_audit.py`文件

```python
...省略...
     # 判断用户当前是否是可审核
    @staticmethod
    def can_review(user, workflow_id, workflow_type):
        audit_info = WorkflowAudit.objects.get(
            workflow_id=workflow_id, workflow_type=workflow_type
        )
        group_id = audit_info.group_id
        result = False
        # 只有待审核状态数据才可以审核
        if audit_info.current_status == WorkflowDict.workflow_status["audit_wait"]:
            try:
                auth_group_id = Audit.detail_by_workflow_id(
                    workflow_id, workflow_type
                ).current_audit
                audit_auth_group = Group.objects.get(id=auth_group_id).name
            except Exception:
                raise Exception("当前审批auth_group_id不存在，请检查并清洗历史数据")
            if (
                    auth_group_users([audit_auth_group], group_id)
                            .filter(id=user.id)
                            .exists()
                    or user.is_superuser == 1
            ):
                if workflow_type == 1:
                    if user.has_perm("sql.query_review"):
                        result = True
                elif workflow_type == 2:
                    if user.has_perm("sql.sql_review"):
                        result = True
                elif workflow_type == 3:
                    if user.has_perm("sql.archive_review"):
                        result = True

        if group_id in [1, 2]:    # 增加
            create_user = audit_info.create_user  # 增加
            if create_user == user.username:  # 增加
                result = False   # 增加
        return result
... 省略...
```

- `group_id` 是资源组ID
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/90727494ddc057f8744a23eba8be9c5e.png)
- 我这边使用docker运行，把·workflow_audit.py·文件替换就好。运行以下命令。
```bash
docker cp workflow_audit.py archery:/opt/archery/sql/utils/
```


-  然后重启
```bash
docker restart archery
```

## 效果
- 现在我自己的帐户就没有审批自己提交SQL的权限了，如下图所示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ab0b49e2764da5c57dd6c796342df8c9.png)
- 登录别人的账号有审核的权限，如下图所示。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7cf3d44dcaa55b6b219a7c4aaa2f57d0.png)

## 参考
- [https://blog.csdn.net/line_on_database/article/details/123847361](https://blog.csdn.net/line_on_database/article/details/123847361)   非常感谢这位大佬