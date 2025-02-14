from django.urls import path
from . import views


# 命名空间
app_name = 'department'


# 路由
urlpatterns = [
    # 部门列表
    path('', views.department_list, name='department_list'),
    # 部门添加
    path('add/', views.department_add, name='department_add'),
]

