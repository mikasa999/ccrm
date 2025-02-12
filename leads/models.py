from django.db import models


class Lead(models.Model):
    # 联系人
    contact_person = models.CharField(max_length=20)
    # 电话
    contact_phone = models.CharField(max_length=20)
    # 产品
    product_name = models.CharField(max_length=20)
    # 业务
    business_name = models.CharField(max_length=20)
    # 线索创建时间
    lead_creation_time = models.DateTimeField()
    # 线索分配时间
    lead_allocation_time = models.DateTimeField(null=True, blank=True)
    # 部门
    department_name = models.CharField(max_length=20)
    # 线索来源
    source_name = models.CharField(max_length=20)
    # 联络工具
    contact_tool = models.CharField(max_length=20)
    # 咨询内容
    consultation_content = models.TextField()
    # 线索负责人
    cow_name = models.CharField(max_length=20)
    # 跟进状态
    follow_status = models.CharField(max_length=50)
    # 最新跟进记录
    follow_new_record = models.TextField()
    # 最新跟进时间
    follow_new_time = models.DateTimeField()
    # 线索编号，字符串类型，最大长度为 20，唯一约束
    leads_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Lead: {self.contact_person} - {self.product_name}"
