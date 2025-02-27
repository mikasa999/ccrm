from django.shortcuts import render, HttpResponse
from .models import Component
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from login.views import required_privilege


"""
说明：要替换的内容
component 替换为当前app的名称
Component 替换为当前app的名称，首字母大写
"""


# 页面标题
title = {
    "page_title": "咨询组件列表",
    "page_heading": "咨询组件",
    "appName": "component",
}


# 权限列表页
@required_privilege('super_admin', 'admin', 'user')
def index(request):
    return render(request, "component_index.html", title)


# 获取数据库数据，返回json数据
@required_privilege('super_admin', 'admin', 'user')
def get_data(request):
    results = Component.objects.all()
    data = []
    for result in results:
        data.append({
            'component_id': result.id,
            'component_name': result.component_name,
            'component_code': result.component_code,
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
            Component.objects.create(component_name=name, component_code=code)
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
            results = Component.objects.get(id=arguments_id)
            results.component_name = name
            results.component_code = code
            results.save()
            return JsonResponse({'status': 'success'})
        except Component.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 新增：删除权限
@required_privilege('super_admin', 'admin', 'user')
def delete_data(request, arguments_id):
    if request.method == 'POST':
        try:
            results = Component.objects.get(id=arguments_id)
            results.delete()
            return JsonResponse({'status': 'success'})
        except Component.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
