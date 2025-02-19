from django.shortcuts import render, HttpResponse
from .models import Cow
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from department.models import Department
from product.models import Product
from business.models import Business
from channel.models import Channel
from component.models import Component
from cow.models import Cow
from proceeding.models import Proceeding
from leads.models import Leads
import secrets
import string


# 一个随机生成20位字符串的函数
def generate_secure_random_string(length=20):
    # 定义包含所有字母（大小写）和数字的字符集
    all_characters = string.ascii_letters + string.digits
    # 使用secrets模块从字符集中随机选择字符，组成指定长度的字符串
    random_string = ''.join(secrets.choice(all_characters) for _ in range(length))
    return random_string


# 页面标题
title = {
    "page_title": "线索池列表",
    "page_heading": "线索池",
    "modal_app_name": "leads",
    "modal_add_name": "leads_modal_add.html",
    "modal_update_name": "leads_modal_update.html",
    "modal_fetch_ajax_js_name": "leads_fetch_ajax_js.html"
}


def index(request):
    # 查询所有外键关联的模型，用于 get_data() 读取
    department = Department.objects.all()
    product = Product.objects.all()
    business = Business.objects.all()
    channel = Channel.objects.all()
    component = Component.objects.all()
    cow = Cow.objects.all()
    proceeding = Proceeding.objects.all()

    context = {
        'department': department,
        'product': product,
        'business': business,
        'channel': channel,
        'component': component,
        'cow': cow,
        'proceeding': proceeding,
        **title
    }
    return render(request, "leads_index.html", context)


def get_data(request):
    results = Leads.objects.all()
    data = []

    for result in results:
        if result.lead_status == 1:  # 线索状态=1，则是新线索
            # 获取部门名称和权限名称
            product_name = result.product_name.product_name if result.product_name else None
            business_name = result.business_name.business_name if result.business_name else None
            department_name = result.department_name.department_name if result.department_name else None
            channel_name = result.channel_name.channel_name if result.channel_name else None
            component_name = result.component_name.component_name if result.component_name else None
            cow_name = result.cow_name.cow_employee_name if result.cow_name else None
            proceeding_name = result.proceeding_name.proceeding_name if result.proceeding_name else None

            data.append({
                'lead_id': result.id,
                'contact_person': result.contact_person,
                'contact_phone': result.contact_phone,
                'product_name': product_name,
                'business_name': business_name,
                'lead_creation_time': result.lead_creation_time,
                'lead_allocation_time': result.lead_allocation_time,
                'department_name': department_name,
                'channel_name': channel_name,
                'component_name': component_name,
                'consultation_content': result.consultation_content,
                'cow_name': cow_name,
                'proceeding_name': proceeding_name,
                'follow_new_record': result.follow_new_record,
                'follow_new_time': result.follow_new_time,
            })
    return JsonResponse({'results': data})


def add_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        contact_person = data.get('contact_person')
        contact_phone = data.get('contact_phone')
        product_name = data.get('product_name')
        business_name = data.get('business_name')
        department_name = data.get('department_name')
        channel_name = data.get('channel_name')
        component_name = data.get('component_name')
        consultation_content = data.get('consultation_content')
        lead_code = generate_secure_random_string()

        try:
            # 根据代码获取实例
            product_name = Product.objects.get(product_code=product_name)
            business_name = Business.objects.get(business_code=business_name)
            department_name = Department.objects.get(department_code=department_name)
            channel_name = Channel.objects.get(channel_code=channel_name)
            component_name = Component.objects.get(component_code=component_name)

            # 创建实例并保存
            Leads.objects.create(
                contact_person=contact_person,
                contact_phone=contact_phone,
                product_name=product_name,
                business_name=business_name,
                department_name=department_name,
                channel_name=channel_name,
                component_name=component_name,
                consultation_content=consultation_content,
                lead_code=lead_code,
            )
            return JsonResponse({'status': 'success'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product does not exist'})
        except Business.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Business does not exist'})
        except Department.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Department does not exist'})
        except Channel.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Channel does not exist'})
        except Component.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Component does not exist'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def update_data(request):
    pass


def delete_data(request, lead_id):
    if request.method == 'POST':
        try:
            results = Leads.objects.get(id=lead_id)
            results.delete()
            return JsonResponse({'status': 'success'})
        except Leads.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'app not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


