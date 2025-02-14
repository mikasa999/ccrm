from django.shortcuts import render, HttpResponse, redirect
from .models import Department
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# 部门列表
department_list_content = {
    "page_title": "部门列表",
    "page_heading": "部门",
}


# 部门列表
def department_list(request):
    return render(request, "department_list.html", department_list_content)

