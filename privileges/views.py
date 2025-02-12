from django.shortcuts import render, HttpResponse


def privileges_list(request):
    return render(request, "privileges_list.html", {"title": "权限"})
