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


# 部门添加
@csrf_exempt
def department_add(request):
    if request.method == 'POST':
        try:
            department_name = request.POST.get('department_name')
            department_code = request.POST.get('department_code')

            # 检查 department_code 是否已经存在
            if Department.objects.filter(department_code=department_code).exists():
                return JsonResponse({'message': f"部门编码 {department_code} 已经存在，请选择其他编码。"}, status=400)

            Department.objects.create(department_name=department_name, department_code=department_code)
            return JsonResponse({'message': '部门添加成功！'}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'添加部门时出现错误: {str(e)}'}, status=500)
    return JsonResponse({'message': '无效的请求方法'}, status=405)
