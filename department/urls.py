from django.urls import path
from . import views


# 命名空间
app_name = 'department'


# 路由
urlpatterns = [
    # 部门列表
    path('', views.department_list, name='department_list'),
    # 该路径访问获取部门数据库内容的json格式，用于ajax局部刷新页面列表数据。
    path('get_department_data/', views.get_department_data, name='get_department_data'),
    # 新增：添加部门
    path('add_department/', views.add_department, name='add_department'),
    # 新增：修改部门
    path('update_department/<int:department_id>/', views.update_department, name='update_department'),
    # 新增：删除部门
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),

]

