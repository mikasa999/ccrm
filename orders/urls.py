from django.urls import path
from . import views

# 命名空间
app_name = "orders"

#路由
urlpatterns = [
    # 订单列表
    path("", views.orders_list, name="orders_list"),
]