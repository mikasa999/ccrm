from django.shortcuts import render, HttpResponse
from .models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


"""
说明：要替换的内容
product 替换为当前app的名称
Product 替换为当前app的名称，首字母大写
"""


# 页面标题
title = {
    "page_title": "产品列表",
    "page_heading": "产品",
    "appName": "product",
}


# 权限列表页
def index(request):
    return render(request, "product_index.html", title)


# 获取数据库数据，返回json数据
def get_data(request):
    results = Product.objects.all()
    data = []
    for result in results:
        data.append({
            'product_id': result.id,
            'product_name': result.product_name,
            'product_code': result.product_code,
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
            Product.objects.create(product_name=name, product_code=code)
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
            results = Product.objects.get(id=arguments_id)
            results.product_name = name
            results.product_code = code
            results.save()
            return JsonResponse({'status': 'success'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 新增：删除权限
@csrf_exempt
def delete_data(request, arguments_id):
    if request.method == 'POST':
        try:
            results = Product.objects.get(id=arguments_id)
            results.delete()
            return JsonResponse({'status': 'success'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
