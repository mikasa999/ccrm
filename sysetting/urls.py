from django.urls import path
from . import views

# 命名空间
app_name = "sysetting"
# 路由
urlpatterns = [
    # 系统设置 列表
    path("list/", views.sysetting_list, name="sysetting_list")
]