from django.urls import path
from . import views


# 命名空间
app_name = 'leads'


# 路由
urlpatterns = [
    # 线索管理 列表 
    path('', views.index, name='index'),
    # 线索异步生成json
    path('get_data', views.get_data, name='get_data'),
    # 添加线索
    path('add_data', views.add_data, name='add_data'),
    # 删除线索
    path('delete_data/<int:lead_id>', views.delete_data, name='delete_data'),
    # 修改线索
    path('update_data/<int:lead_id>', views.update_data, name='update_data'),
]

