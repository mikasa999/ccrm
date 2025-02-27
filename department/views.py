from django.shortcuts import render, HttpResponse
from .models import Department
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from login.views import required_privilege


"""
说明：要替换的内容
department 替换为当前app的名称
Department 替换为当前app的名称，首字母大写
"""


# 页面标题
title = {
    "page_title": "部门列表",
    "page_heading": "部门",
    "appName": "department",
}


# 权限列表页
@required_privilege('super_admin', 'admin', 'user')
def index(request):
    return render(request, "department_index.html", title)


# 获取数据库数据，返回json数据
@required_privilege('super_admin', 'admin', 'user')
def get_data(request):
    results = Department.objects.all()
    data = []
    for result in results:
        data.append({
            'department_id': result.id,
            'department_name': result.department_name,
            'department_code': result.department_code,
        })
    return JsonResponse({'results': data})


# 新增：添加
@required_privilege('super_admin', 'admin', 'user')
def add_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('field_name')
        code = data.get('field_code')
        try:
            Department.objects.create(department_name=name, department_code=code)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 新增：修改权限
@required_privilege('super_admin', 'admin', 'user')
def update_data(request, arguments_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('field_name')
        code = data.get('field_code')
        try:
            results = Department.objects.get(id=arguments_id)
            results.department_name = name
            results.department_code = code
            results.save()
            return JsonResponse({'status': 'success'})
        except Department.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 新增：删除权限
@required_privilege('super_admin', 'admin', 'user')
def delete_data(request, arguments_id):
    if request.method == 'POST':
        try:
            results = Department.objects.get(id=arguments_id)
            results.delete()
            return JsonResponse({'status': 'success'})
        except Department.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
