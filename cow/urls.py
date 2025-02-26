from django.urls import path
from . import views

# 命名空间
app_name = 'cow'

# 路由
urlpatterns = [
    # 员工管理 列表
    path('', views.index, name='index'),
    # json异步生成
    path('get_data', views.get_data, name='get_data'),
    # 添加员工
    path('add_data', views.add_data, name='add_data'),
    # 删除员工
    path('delete_data/<int:cow_id>', views.delete_data, name='delete_data'),
    # 修改员工普通信息
    path('update_data/<int:cow_id>', views.update_data, name='update_data'),
    # 修改密码
    path('update_password_data/<int:cow_id>', views.update_password_data, name='update_password_data')
]