from django.shortcuts import render, HttpResponse
from .models import Business
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from login.views import required_privilege


"""
说明：要替换的内容
business 替换为当前app的名称
Business 替换为当前app的名称，首字母大写
"""


# 页面标题
title = {
    "page_title": "业务列表",
    "page_heading": "业务",
    "appName": "business",
}


@required_privilege('super_admin', 'admin', 'user')
# 权限列表页
def index(request):
    return render(request, "business_index.html", title)


@required_privilege('super_admin', 'admin', 'user')
# 获取数据库数据，返回json数据
def get_data(request):
    results = Business.objects.all()
    data = []
    for result in results:
        data.append({
            'business_id': result.id,
            'business_name': result.business_name,
            'business_code': result.business_code,
        })
    return JsonResponse({'results': data})


@required_privilege('super_admin', 'admin', 'user')
# 新增：添加
def add_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('field_name')
        code = data.get('field_code')
        try:
            Business.objects.create(business_name=name, business_code=code)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@required_privilege('super_admin', 'admin', 'user')
# 新增：修改权限
def update_data(request, arguments_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('field_name')
        code = data.get('field_code')
        try:
            results = Business.objects.get(id=arguments_id)
            results.business_name = name
            results.business_code = code
            results.save()
            return JsonResponse({'status': 'success'})
        except Business.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@required_privilege('super_admin', 'admin', 'user')
# 新增：删除权限
def delete_data(request, arguments_id):
    if request.method == 'POST':
        try:
            results = Business.objects.get(id=arguments_id)
            results.delete()
            return JsonResponse({'status': 'success'})
        except Business.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
