from django.db import models


# 创建部门表模型
class Department(models.Model):
    # 部门名称字段，最大长度为 30，不允许为空
    department_name = models.CharField(max_length=30, blank=False, null=False)
    # 部门编码字段，最大长度为 20，不允许为空，且要求唯一
    department_code = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        # 定义对象的字符串表示形式，方便在管理界面等地方显示
        return self.department_name
