from django.shortcuts import render, HttpResponse
from login.views import required_privilege


# 客户列表
@required_privilege('super_admin', 'admin', 'user')
def customer_list(request):
    return render(request, "customer_list.html", {"title": "客户列表"})
