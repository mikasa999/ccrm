from django.shortcuts import render, HttpResponse


# 订单列表
def orders_list(request):
    return render(request, "orders_list.html", {"title": "订单列表"})
