from django.contrib import admin
from django.urls import path, include

# 命名空间
app_name = 'website'

# 路由
urlpatterns = [
    # 后台管理
    path("admin/", admin.site.urls),
    # 线索管理
    path("leads/", include("leads.urls")),
    # 部门管理
    path("department/", include("department.urls")),
    # 权限管理
    path("privileges/", include("privileges.urls")),
    # 员工管理
    path("cow/", include("cow.urls")),
    # 订单
    path("orders/", include("orders.urls")),
    # 客户
    path("customer/", include("customer.urls")),
    # 产品
    path("product/", include("product.urls")),
    # 业务
    path("business/", include("business.urls")),
    # 来源
    path("channel/", include("channel.urls")),
    # 咨询组件
    path("component/", include("component.urls")),
    # 跟进状态
    path("proceeding/", include("proceeding.urls")),
    # 登录
    path("login/", include("login.urls")),
]


