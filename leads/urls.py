from django.urls import path
from . import views


# 命名空间
app_name = 'leads'


# 路由
urlpatterns = [
    # 线索管理 列表 
    path('list/', views.leads_list, name='leads_list'),
    # 线索管理 详情
    path('detail/<int:id>', views.leads_detail, name='leads_detail'),
    # 线索管理 编辑
    path('edit/<int:id>', views.leads_edit, name='leads_edit'),
    # 线索管理 删除
    path('delete/<int:id>', views.leads_delete, name='leads_delete'),
]

