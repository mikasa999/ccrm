from django.urls import path
from . import views

"""
说明：要替换的内容
app_name
"""

# 命名空间
app_name = 'product'

urlpatterns = [
    # 权限 列表页
    path("", views.index, name='index'),
    # 该路径访问获取部门数据库内容的json格式，用于ajax局部刷新页面列表数据。
    path('get_data/', views.get_data, name='get_data'),
    # 新增：添加部门
    path('add_data/', views.add_data, name='add_data'),
    # 新增：修改部门
    path('update_data/<int:arguments_id>/', views.update_data, name='update_data'),
    # 新增：删除部门
    path('delete_data/<int:arguments_id>/', views.delete_data, name='delete_data'),
]