from django.urls import path
from . import views


# 命名空间
app_name = 'leads'


# 路由
urlpatterns = [
    # 线索池
    path('', views.index, name='index'),
    # 不带参数的 URL 模式
    path('get_data/', views.get_data, name='get_data'),
    # 保留带参数的 URL 模式，以支持搜索功能
    path('get_data/<str:leads_search_content>/', views.get_data, name='get_data_search'),
    # 线索池添加线索
    path('add_data', views.add_data, name='add_data'),
    # 线索池删除线索
    path('delete_data/<int:lead_id>', views.delete_data, name='delete_data'),
    # 线索池修改线索
    path('update_data/<int:lead_id>', views.update_data, name='update_data'),
    # 认领线索
    path('claim/', views.claim, name='claim'),
    # 认领线索异步生成json
    path('claim_get_data', views.claim_get_data, name='claim_get_data'),
    # 保留带参数的 URL 模式，以支持搜索功能
    path('claim_get_data/<str:leads_search_content>/', views.claim_get_data, name='claim_get_data_search'),
    # 认领按钮点击
    path('claim_leads/', views.claim_leads, name='claim_leads'),
    # 退回线索按钮点击
    path('send_back_leads/', views.send_back_leads, name='send_back_leads'),
    # 线索认领左侧面板-》线索详情部分
    path('canvas_leads_data/<int:lead_id>', views.canvas_leads_data, name='canvas_leads_data'),
    # 面板跟进添加
    path('canvas_proceeding_add/', views.canvas_proceeding_add, name='canvas_proceeding_add'),
    # 侧面板加载跟进信息
    path('canvas_proceeding_data/<int:lead_id>', views.canvas_proceeding_data, name='canvas_proceeding_data'),
]

