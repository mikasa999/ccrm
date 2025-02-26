from django.urls import path
from . import views

# 命名空间
app_name = "customer"

# 路由
urlpatterns = [
    # 客户管理 列表
    path("", views.customer_list, name="customer_list"),
]
