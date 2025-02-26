from django.urls import path
from . import views

# 命名空间
app_name = "login"

urlpatterns = [
    # 首页
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
]