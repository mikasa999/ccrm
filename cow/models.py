from django.db import models


# 创建员工表模型
class Cow(models.Model):
    # 员工名称字段，最大长度为 20，不允许为空
    cow_name = models.CharField(max_length=20, blank=False, null=False)
    # 所属部门名称字段，最大长度为 30，不允许为空
    department_name = models.CharField(max_length=30, blank=False, null=False)
    # 所属权限名称字段，最大长度为 20，不允许为空
    privileges_name = models.CharField(max_length=20, blank=False, null=False)
    # 领取线索总量字段，用于统计历史共领取的线索总数，默认为 0
    receive_leads_total = models.IntegerField(default=0)
    # 员工编码字段，最大长度为 20，不允许为空，且要求唯一
    cow_code = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        # 定义对象的字符串表示形式，方便在管理界面等地方显示
        return self.cow_name
