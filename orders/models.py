from django.db import models


class Orders(models.Model):
    # 客户名称，字符串类型，最大长度为 40
    customer_name = models.CharField(max_length=40)
    # 成交日期，日期类型
    deal_date = models.DateField()
    # 联系人，字符串类型，最大长度为 20
    contact_person = models.CharField(max_length=20)
    # 联系电话，字符串类型，最大长度为 20
    contact_phone = models.CharField(max_length=20)
    # 归属部门，字符串类型，最大长度为 20
    department_name = models.CharField(max_length=20)
    # 负责人，字符串类型，最大长度为 20
    cow_name = models.CharField(max_length=20)
    # 订单金额，十进制类型，最大位数为 10，小数位数为 2
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # 产品类型，字符串类型，最大长度为 20
    product_name = models.CharField(max_length=20)
    # 业务类型，字符串类型，最大长度为 20
    business_name = models.CharField(max_length=20)
    # 线索来源，字符串类型，最大长度为 20
    source_name = models.CharField(max_length=20)
    # 线索创建日期，日期类型
    lead_creation_time = models.DateField()
    # 订单编号，字符串类型，最大长度为 20，唯一约束
    order_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        # 返回订单编号作为对象的字符串表示
        return self.order_number
