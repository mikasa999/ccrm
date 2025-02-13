from django.urls import path
from . import views


# 命名空间
app_name = "dashboard"

# 路由
urlpatterns = [
    # 仪表盘页面
    path("list/", views.dashboard_list, name="dashboard_list")
]