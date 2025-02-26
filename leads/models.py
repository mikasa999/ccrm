from django.db import models
from department.models import Department
from product.models import Product
from business.models import Business
from channel.models import Channel
from component.models import Component
from cow.models import Cow
from proceeding.models import Proceeding


class Leads(models.Model):
    # 联系人
    contact_person = models.CharField(max_length=20, verbose_name='联系人')
    # 电话
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    # 产品
    product_name = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='产品', to_field='product_code')
    # 业务
    business_name = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='业务', to_field='business_code')
    # 线索创建时间
    lead_creation_time = models.DateTimeField(auto_now_add=True)
    # 线索首次领取时间，领取的时候填入
    lead_allocation_time = models.DateTimeField(null=True, blank=True)
    # 部门
    department_name = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name='部门', to_field='department_code')
    # 线索来源
    channel_name = models.ForeignKey(Channel, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='来源', to_field='channel_code')
    # 联络工具
    component_name = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='联络工具', to_field='component_code')
    # 咨询内容
    consultation_content = models.TextField(null=True, blank=True)
    # 线索负责人
    cow_name = models.ForeignKey(Cow, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='线索负责人', to_field='username')
    # 跟进状态
    proceeding_name = models.ForeignKey(Proceeding, on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name='跟进状态', to_field='proceeding_code')
    # 最新跟进记录
    follow_new_record = models.TextField(null=True, blank=True)
    # 最新跟进时间
    follow_new_time = models.DateTimeField(null=True, blank=True)
    # 线索编号，字符串类型，最大长度为 20，唯一约束
    lead_code = models.CharField(max_length=20, unique=True)
    # 新增无符号短整型线索状态字段，
    # 1表示新线索，2表示线索已经被认领，3表示退回公海，4表示多次领取的老线索，5表示删除
    # 超过规定时间比如1天就只能退回公海
    lead_status = models.PositiveSmallIntegerField(default=1, null=True, blank=True, verbose_name='线索状态')

    def __str__(self):
        return f"Lead: {self.contact_person} - {self.product_name}"


class LeadFollowUpRecord(models.Model):
    # 关联的线索
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE, related_name='follow_up_records', verbose_name='关联线索')
    # 跟进内容
    follow_up_content = models.TextField(verbose_name='跟进内容')
    # 跟进时间，自动记录创建时间
    follow_up_time = models.DateTimeField(auto_now_add=True, verbose_name='跟进时间')
    # 跟进人
    follow_up_person = models.ForeignKey(Cow, on_delete=models.SET_NULL, null=True, blank=True,
                                         verbose_name='跟进人', to_field='username')

    class Meta:
        verbose_name = '线索跟进记录'
        verbose_name_plural = '线索跟进记录'
        ordering = ['-follow_up_time']  # 按跟进时间倒序排列

    def __str__(self):
        return f"Follow-up for {self.lead.lead_code} at {self.follow_up_time}"
