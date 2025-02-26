from django.shortcuts import render, HttpResponse
from .models import ModelName
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


"""
说明：要替换的内容
appName 替换为当前app的名称
ModelName 替换为当前app的名称，首字母大写
"""


# 页面标题
title = {
    "page_title": "XX列表",
    "page_heading": "XX",
    "modal_app_name": "appName",
    "modal_add_name": "appName_modal_all.html",
    "modal_update_name": "appName_modal_update.html",
    "modal_fetch_ajax_js_name": "appName_fetch_ajax_js.html"
}


# 权限列表页
def index(request):
    return render(request, "appName_index.html", title)


# 获取数据库数据，返回json数据
def get_data(request):
    results = ModelName.objects.all()
    data = []
    for result in results:
        data.append({
            'appName_id': result.id,
            'appName_name': result.appName_name,
            'appName_code': result.appName_code,
        })
    return JsonResponse({'results': data})


# 新增：添加
def add_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('field_name')
        code = data.get('field_code')
        try:
            ModelName.objects.create(appName_name=name, appName_code=code)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 新增：修改权限
def update_data(request, arguments_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('field_name')
        code = data.get('field_code')
        try:
            results = ModelName.objects.get(id=arguments_id)
            results.appName_name = name
            results.appName_code = code
            results.save()
            return JsonResponse({'status': 'success'})
        except ModelName.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 新增：删除权限
def delete_data(request, arguments_id):
    if request.method == 'POST':
        try:
            results = ModelName.objects.get(id=arguments_id)
            results.delete()
            return JsonResponse({'status': 'success'})
        except ModelName.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
