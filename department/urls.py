from django.urls import path
from . import views

# 命名空间
app_name = 'department'

# 路由
urlpatterns = [
    # 线索管理 列表 
    path('list/', views.department_list, name='department_list'),
]

