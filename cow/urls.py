from django.urls import path
from . import views

# 命名空间
app_name = 'cow'

# 路由
urlpatterns = [
    # 员工管理 列表
    path('', views.index, name='index'),
]