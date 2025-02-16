from django.db import models


"""
说明：要替换的内容
component 替换为当前app的名称
Component 替换为当前app的名称，首字母大写
"""


class Component(models.Model):  # 修改点，这里替换模型名字为当前app名字，首字母大写
    # 名称字段，最大长度为 20，不允许为空
    component_name = models.CharField(max_length=20, blank=False, null=False)
    # 编码字段，最大长度为 20，不允许为空，且要求唯一
    component_code = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        # 定义对象的字符串表示形式，方便在管理界面等地方显示
        return self.component_name
