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

# 获取部门数据库数据，并返回为JSON数据
def get_department_data(request):
    departments = Department.objects.all()
    data = []
    for department in departments:
        data.append({
            'id': department.id,
            'department_name': department.department_name,
            'department_code': department.department_code,
        })
    return JsonResponse({'departments': data})


# 新增：添加部门
@csrf_exempt
def add_department(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        department_name = data.get('department_name')
        department_code = data.get('department_code')
        try:
            Department.objects.create(department_name=department_name, department_code=department_code)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 新增：修改部门
@csrf_exempt
def update_department(request, department_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        department_name = data.get('department_name')
        department_code = data.get('department_code')
        try:
            department = Department.objects.get(id=department_id)
            department.department_name = department_name
            department.department_code = department_code
            department.save()
            return JsonResponse({'status': 'success'})
        except Department.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Department not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 新增：删除部门
@csrf_exempt
def delete_department(request, department_id):
    if request.method == 'POST':
        try:
            department = Department.objects.get(id=department_id)
            department.delete()
            return JsonResponse({'status': 'success'})
        except Department.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Department not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

