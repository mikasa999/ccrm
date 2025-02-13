from django.shortcuts import render, HttpResponse, redirect
from .models import Department
from django.urls import reverse


# 部门列表
department_list_content = {
    "page_title": "部门列表",
    "page_heading": "部门",
}


# 部门列表
def department_list(request):
    return render(request, "department_list.html", department_list_content)


# 部门添加
def department_add(request):
    if request.method == 'post':
        department_name = request.POST.get('department_name')
        department_code = request.POST.get('department_code')
        Department.objects.create(department_name=department_name,department_code=department_code)
        return redirect('department:department_list')
        # 获取部门列表数据
    else:
        print('没有获取post值')
        return redirect('leads:leads_list')
