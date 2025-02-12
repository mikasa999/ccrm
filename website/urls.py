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
    # 系统设置
    path("sysetting/", include("sysetting.urls")),
    # 订单
    path("orders/", include("orders.urls")),
    # 客户
    path("customer/", include("customer.urls")),
    
]


