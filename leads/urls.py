from django.urls import path
from . import views


# 命名空间
app_name = 'leads'


# 路由
urlpatterns = [
    # 线索管理 列表 
    path('', views.leads_list, name='leads_list'),
]

