from django.shortcuts import render, HttpResponse


# 仪表盘页面
def dashboard_list(request):
    return HttpResponse("仪表盘页面")
