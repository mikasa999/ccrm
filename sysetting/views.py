from django.shortcuts import render, HttpResponse

# 系统设置 列表页
def sysetting_list(request):
    return render(request, "sysetting_list.html", {"title": "系统设置"})
