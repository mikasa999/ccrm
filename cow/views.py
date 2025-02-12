from django.shortcuts import render, HttpResponse

def cow_list(request):
    return render(request, "cow_list.html", {"title": "员工管理 列表"})
