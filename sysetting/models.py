from django.db import models


# 创建产品表模型
class Product(models.Model):
    # 产品名称字段，最大长度为 30，不允许为空
    product_name = models.CharField(max_length=30, blank=False, null=False)
    # 产品编码字段，最大长度为 20，不允许为空，且要求唯一
    product_code = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        # 定义对象的字符串表示形式，方便在管理界面等地方显示
        return self.product_name


# 创建业务表模型
class Business(models.Model):
    # 业务名称字段，最大长度为 30，不允许为空
    business_name = models.CharField(max_length=30, blank=False, null=False)
    # 业务编码字段，最大长度为 20，不允许为空，且要求唯一
    business_code = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        # 定义对象的字符串表示形式，方便在管理界面等地方显示
        return self.business_name


# 创建线索来源表模型
class Source(models.Model):
    # 线索来源名称字段，最大长度为 30，不允许为空
    source_name = models.CharField(max_length=30, blank=False, null=False)
    # 线索来源编码字段，最大长度为 20，不允许为空，且要求唯一
    source_code = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        # 定义对象的字符串表示形式，方便在管理界面等地方显示
        return self.source_name


# 创建联络工具表模型
class Contact(models.Model):
    # 联系方式名称字段，最大长度为 30，不允许为空
    contact_tool = models.CharField(max_length=30, blank=False, null=False)
    # 联系方式编码字段，最大长度为 20，不允许为空，且要求唯一
    contact_code = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        # 定义对象的字符串表示形式，方便在管理界面等地方显示
        return self.contact_name


# 创建跟进状态表模型
class Follow(models.Model):
    # 跟进状态名称字段，最大长度为 30，不允许为空
    follow_status = models.CharField(max_length=30, blank=False, null=False)
    # 跟进状态编码字段，最大长度为 20，不允许为空，且要求唯一
    follow_code = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        # 定义对象的字符串表示形式，方便在管理界面等地方显示
        return self.follow_name
