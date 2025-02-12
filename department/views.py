from django.shortcuts import render, HttpResponse

# 部门列表
department_list_content = {
    "page_title": "部门列表",
    "page_heading": "部门",
}


def department_list(request):
    return render(request, "department_list.html", department_list_content)
