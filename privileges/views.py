from django.shortcuts import render, HttpResponse
from .models import Privileges
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


"""
说明：要替换的内容
privileges 替换为当前app的名称
Privileges 替换为当前app的名称，首字母大写
"""


# 页面标题
title = {
    "page_title": "权限列表",
    "page_heading": "权限",
    "appName": "privileges",
}


# 权限列表页
def index(request):
    return render(request, "privileges_index.html", title)


# 获取数据库数据，返回json数据
def get_data(request):
    results = Privileges.objects.all()
    data = []
    for result in results:
        data.append({
            'privileges_id': result.id,
            'privileges_name': result.privileges_name,
            'privileges_code': result.privileges_code,
        })
    return JsonResponse({'results': data})


# 新增：添加
@csrf_exempt
def add_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('field_name')
        code = data.get('field_code')
        try:
            Privileges.objects.create(privileges_name=name, privileges_code=code)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 新增：修改权限
@csrf_exempt
def update_data(request, arguments_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('field_name')
        code = data.get('field_code')
        try:
            results = Privileges.objects.get(id=arguments_id)
            results.privileges_name = name
            results.privileges_code = code
            results.save()
            return JsonResponse({'status': 'success'})
        except Privileges.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 新增：删除权限
@csrf_exempt
def delete_data(request, arguments_id):
    if request.method == 'POST':
        try:
            results = Privileges.objects.get(id=arguments_id)
            results.delete()
            return JsonResponse({'status': 'success'})
        except Privileges.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
