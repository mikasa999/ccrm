from django.shortcuts import render, HttpResponse
from .models import Cow
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from department.models import Department
from privileges.models import Privileges


"""
说明：要替换的内容
appName 替换为当前app的名称
ModelName 替换为当前app的名称，首字母大写
"""


# 页面标题
title = {
    "page_title": "员工列表",
    "page_heading": "员工",
    "modal_app_name": "cow",
    "modal_add_name": "cow_modal_add.html",
    "modal_update_name": "cow_modal_update.html",
    "modal_fetch_ajax_js_name": "cow_fetch_ajax_js.html"
}


def index(request):
    # 查询所有部门和权限
    departments = Department.objects.all()
    privileges = Privileges.objects.all()
    context = {
        'departments': departments,
        'privileges': privileges,
        **title
    }
    return render(request, "cow_index.html", context)


# 获取数据库数据，返回json数据
def get_data(request):
    results = Cow.objects.all()
    data = []

    for result in results:
        # 获取部门名称和权限名称
        department_name = result.cow_department.department_name if result.cow_department else None
        privileges_name = result.cow_privileges.privileges_name if result.cow_privileges else None

        data.append({
            'cow_id': result.id,
            'cow_employee_name': result.cow_employee_name,
            'cow_department': department_name,  # 使用部门名称
            'cow_privileges': privileges_name,  # 使用权限名称
            'cow_leads_total': result.cow_leads_total,
            'cow_follow_up_count': result.cow_follow_up_count,
            'cow_customer_count': result.cow_customer_count,
            'cow_returned_to_public_count': result.cow_returned_to_public_count,
            'cow_deal_count': result.cow_deal_count,
            'cow_first_deal_total_amount': result.cow_first_deal_total_amount,
            'cow_total_deal_amount': result.cow_total_deal_amount,
            'username': result.username,
        })
    return JsonResponse({'results': data})


# 新增
@csrf_exempt
def add_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cow_employee_name = data.get('cow_employee_name')
        cow_department_code = data.get('cow_department')  # 传入部门代码
        cow_privileges_code = data.get('cow_privileges')  # 传入权限代码
        username = data.get('username')
        password = data.get('password')

        # 如果密码为空，使用默认值
        if not password:
            password = '123456'

        try:
            # 根据部门代码获取部门实例
            department = Department.objects.get(department_code=cow_department_code)
            # 根据权限代码获取权限实例
            privileges = Privileges.objects.get(privileges_code=cow_privileges_code)

            # 创建 Cow 实例并保存
            Cow.objects.create(
                cow_employee_name=cow_employee_name,
                cow_department=department,
                cow_privileges=privileges,
                username=username,
                password=password
            )
            return JsonResponse({'status': 'success'})
        except Department.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Department does not exist'})
        except Privileges.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Privileges does not exist'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 删除
def delete_data(request, cow_id):
    if request.method == 'POST':
        try:
            results = Cow.objects.get(id=cow_id)
            results.delete()
            return JsonResponse({'status': 'success'})
        except Cow.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})