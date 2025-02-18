from django.db import models
from department.models import Department  # 假设部门模型在 department 应用中
from privileges.models import Privileges  # 引入权限模型


class Cow(models.Model):
    # 员工姓名，最大长度为 20 个字符，不能为空
    cow_employee_name = models.CharField(max_length=20, verbose_name='员工姓名')
    # 所属部门，使用外键关联到 Department 模型，当部门被删除时，将员工的部门设置为 NULL
    cow_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='所属部门', to_field='department_code')
    # 权限，使用外键关联到 Privilege 模型，当权限被删除时，将员工的权限设置为 NULL
    cow_privileges = models.ForeignKey(Privileges, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='权限', to_field='privileges_code')
    # 线索总量，使用正整数类型存储
    cow_leads_total = models.PositiveIntegerField(default=0, verbose_name='线索总量')
    # 跟进数量，使用正整数类型存储
    cow_follow_up_count = models.PositiveIntegerField(default=0, verbose_name='跟进数量')
    # 客户数量，使用正整数类型存储，默认值为 0
    cow_customer_count = models.PositiveIntegerField(default=0, verbose_name='客户数量')
    # 回退公海数量，使用正整数类型存储
    cow_returned_to_public_count = models.PositiveIntegerField(default=0, verbose_name='回退公海数量')
    # 成交笔数，使用正整数类型存储
    cow_deal_count = models.PositiveIntegerField(default=0, verbose_name='成交数量')
    # 首单成交总额，使用 Decimal 类型存储，最多保留0位小数
    cow_first_deal_total_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0,
                                                      verbose_name='首单成交总额')
    # 成交总额，使用 Decimal 类型存储，最多保留0位小数
    cow_total_deal_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='成交总额')

    def __str__(self):
        return self.cow_employee_name

    class Meta:
        verbose_name = '员工'
        verbose_name_plural = '员工'
