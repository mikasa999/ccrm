from django.urls import path
from . import views


# 命名空间
app_name = 'department'


# 路由
urlpatterns = [
    # 部门列表
    path('', views.department_list, name='department_list'),
    # 该路径访问获取部门数据库内容的json格式，用于ajax局部刷新页面列表数据。
    path('get_department_data/', views.get_department_data, name='get_department_data')
]

