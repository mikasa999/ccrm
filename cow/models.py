from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from department.models import Department  # 部门模型
from privileges.models import Privileges  # 权限模型


class Cow(models.Model):
    # 员工姓名，最大长度为 20 个字符，不能为空
    cow_employee_name = models.CharField(max_length=20, verbose_name='员工姓名')
    # 所属部门，使用外键关联到 Department 模型，当部门被删除时，将员工的部门设置为 NULL
    cow_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='所属部门', to_field='department_code')
    # 权限，使用外键关联到 Privilege 模型，当权限被删除时，将员工的权限设置为 NULL
    cow_privileges = models.ForeignKey(Privileges, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='权限', to_field='privileges_code')
    # 邮箱字段，最大长度为 50 个字符，允许为空
    cow_email = models.EmailField(max_length=50, null=True, blank=True, verbose_name='邮箱')
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
    # 账号和密码字段
    username = models.CharField(max_length=30, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码')

    # _password_changed = False

    # # set_password 方法：借助 make_password 函数对明文密码进行加密，然后将加密后的密码存储到 password 字段。
    # def set_password(self, password):
    #     self.password = make_password(password)
    #     self._password_changed = True
    #
    # # check_password 方法：使用 check_password 函数验证输入的明文密码和存储的加密密码是否匹配。
    # def check_password(self, password):
    #     return check_password(password, self.password)
    #
    # # 在 save 方法里，先判断是新创建的实例，还是密码有变更。如果满足条件，就调用 set_password 方法对密码进行加密，然后再调用父类的 save 方法保存实例。
    # def save(self, *args, **kwargs):
    #     if not self.pk or self._password_changed:
    #         if not self._password_changed:
    #             self.set_password(self.password)
    #         self._password_changed = False
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.cow_employee_name

    class Meta:
        verbose_name = '员工'
        verbose_name_plural = '员工'
