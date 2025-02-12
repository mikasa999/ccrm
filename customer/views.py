from django.shortcuts import render, HttpResponse


# 客户列表
def customer_list(request):
    return render(request, "customer_list.html", {"title": "客户列表"})
