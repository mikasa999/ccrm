from django.urls import path
from . import views

# 命名空间
app_name = 'cow'

# 路由
urlpatterns = [
    # 员工管理 列表
    path('list/', views.cow_list, name='cow_list'),
]