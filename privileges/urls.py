from django.urls import path
from . import views

# 命名空间
app_name = 'privileges'

urlpatterns = [
    # 权限 列表页
    path("", views.privileges_list, name='privileges_list'),
]