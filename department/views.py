from django.shortcuts import render, HttpResponse


def department_list(request):
    return render(request, "department_list.html", {"title": "部门 列表"})