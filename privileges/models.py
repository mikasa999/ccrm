from django.db import models


# 创建权限表模型
class Privileges(models.Model):
    # 权限名称字段，最大长度为 20，不允许为空
    privileges_name = models.CharField(max_length=20, blank=False, null=False)
    # 权限编码字段，最大长度为 20，不允许为空，且要求唯一
    privileges_code = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        # 定义对象的字符串表示形式，方便在管理界面等地方显示
        return self.privileges_name
