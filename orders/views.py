from django.shortcuts import render, HttpResponse
from login.views import required_privilege


# 订单列表
@required_privilege('super_admin', 'admin', 'user')
def orders_list(request):
    return render(request, "orders_list.html", {"title": "订单列表"})
