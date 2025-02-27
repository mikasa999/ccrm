from django.shortcuts import render, HttpResponse, redirect
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
from leads.models import Leads, LeadFollowUpRecord
import secrets
import string
from login.views import required_privilege
import datetime
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site


# 一个随机生成20位字符串的函数
def generate_secure_random_string(length=20):
    # 定义包含所有字母（大小写）和数字的字符集
    all_characters = string.ascii_letters + string.digits
    # 使用secrets模块从字符集中随机选择字符，组成指定长度的字符串
    random_string = ''.join(secrets.choice(all_characters) for _ in range(length))
    return random_string


# 手机号码字符串中间4位替换*
def hide_middle_four_digits(phone_number):
    # 检查输入的手机号码长度是否为 11 位
    if len(phone_number) == 11:
        # 截取手机号码的前 3 位
        start = phone_number[:3]
        # 中间 4 位替换为 ****
        middle = '****'
        # 截取手机号码的后 4 位
        end = phone_number[-4:]
        # 拼接替换后的手机号码
        new_phone_number = start + middle + end
        return new_phone_number
    else:
        # 如果手机号码长度不是 11 位，直接返回原号码
        return phone_number


@required_privilege('super_admin', 'admin', 'user')
def index(request):
    # 页面标题
    title = {
        "page_title": "线索池列表",
        "page_heading": "线索池",
        "modal_app_name": "leads",
        "modal_add_name": "leads_modal_add.html",
        "modal_update_name": "leads_modal_update.html",
        "modal_fetch_ajax_js_name": "leads_fetch_ajax_js.js"
    }

    # 查询所有外键关联的模型，问下豆包这里是干啥的？
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


@required_privilege('super_admin', 'admin', 'user')
def get_data(request, leads_search_content=None):
    # 根据session存储的权限以及部门来筛选不同的内容进行展示
    privileges = request.session.get('privileges')
    department_code = request.session.get('department_code')

    # 基础查询集，筛选 lead_status=1
    base_query = Leads.objects.filter(lead_status=1).order_by('-id')

    if privileges:
        if privileges == 'super_admin':
            if leads_search_content is not None:
                # 超级管理员有搜索内容
                results = base_query.filter(contact_phone__icontains=leads_search_content)
            else:
                # 超级管理员无搜索内容
                results = base_query
        elif privileges in ['admin', 'user']:
            # 筛选本部门的线索
            department_query = base_query.filter(department_name=department_code)
            if leads_search_content is not None:
                # 管理员或用户有搜索内容
                results = department_query.filter(contact_phone__icontains=leads_search_content)
            else:
                # 管理员或用户无搜索内容
                results = department_query
        else:
            # 权限类型不合法
            return JsonResponse({'error': 'Invalid privilege type'}, status=400)
    else:
        # 未获取到权限信息
        return JsonResponse({'error': 'Privilege information not found'}, status=400)

    # 分页逻辑
    page_number = request.GET.get('page', 1)
    paginator = Paginator(results, 3)  # 每页显示 10 条记录
    page_obj = paginator.get_page(page_number)

    # 获取绝对路径
    current_site = get_current_site(request)
    absolute_url = f"http://{current_site.domain}"

    data = []
    for result in page_obj:
        # 获取部门名称和权限名称
        product_name = result.product_name.product_name if result.product_name else None
        business_name = result.business_name.business_name if result.business_name else None
        department_name = result.department_name.department_name if result.department_name else None
        channel_name = result.channel_name.channel_name if result.channel_name else None
        component_name = result.component_name.component_name if result.component_name else None
        cow_name = result.cow_name.cow_employee_name if result.cow_name else None
        proceeding_name = result.proceeding_name.proceeding_name if result.proceeding_name else None
        consultation_content = f"{result.consultation_content[:20]}..." if result.consultation_content else '-'
        consultation_content_complete = result.consultation_content if result.consultation_content else '-'
        contact_phone = hide_middle_four_digits(result.contact_phone)

        data.append({
            'lead_id': result.id,
            'contact_person': result.contact_person,
            'contact_phone': contact_phone,
            'product_name': product_name,
            'business_name': business_name,
            # 这个字段存储的是对象格式的时间，需要用strftime('%Y-%m-%d %H:%M:%S')转换为字符串格式
            'lead_creation_time': result.lead_creation_time.strftime('%Y-%m-%d %H:%M'),
            'lead_allocation_time': result.lead_allocation_time,
            'department_name': department_name,
            'channel_name': channel_name,
            'component_name': component_name,
            'consultation_content': consultation_content,
            'consultation_content_complete': consultation_content_complete,
            'cow_name': cow_name,
            'proceeding_name': proceeding_name,
            'follow_new_record': result.follow_new_record,
            'follow_new_time': result.follow_new_time,
            'lead_code': result.lead_code,
            'absolute_url': absolute_url,
        })

    return JsonResponse({
        'results': data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'total_records': paginator.count,
    })


@required_privilege('super_admin')
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


@required_privilege('super_admin')
def update_data(request):
    pass


# 这里后面要改成假删除，lead_status==5 表示删除
@required_privilege('super_admin')
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


# 认领线索首页
@required_privilege('super_admin', 'admin', 'user')
def claim(request):
    proceeding = Proceeding.objects.all()
    # 页面标题
    title = {
        "page_title": "已认领线索列表",
        "page_heading": "已认领线索",
        "modal_app_name": "leads",
        "modal_add_name": "claim_modal_add.html",
        "modal_update_name": "claim_modal_update.html",
        "modal_fetch_ajax_js_name": "claim_fetch_ajax_js.js",
        "claim_canvas_proceeding": "claim_canvas_proceeding.html",
        "proceeding": proceeding,
    }
    return render(request, "claim_index.html", title)


@required_privilege('super_admin', 'admin', 'user')
def claim_get_data(request, leads_search_content=None):
    # 根据session存储的权限以及部门来筛选不同的内容进行展示
    privileges = request.session.get('privileges')
    department_code = request.session.get('department_code')
    username = request.session.get('username')

    # 基础查询集，筛选 lead_status=2 认领的线索
    base_query = Leads.objects.filter(lead_status=2).order_by('-id')

    if privileges:
        if privileges == 'super_admin':
            if leads_search_content is not None:
                # 超级管理员有搜索内容
                results = base_query.filter(contact_phone__icontains=leads_search_content)
            else:
                # 超级管理员无搜索内容
                results = base_query
        elif privileges == 'admin':
            # 筛选本部门的线索
            department_query = base_query.filter(department_name=department_code)
            if leads_search_content is not None:
                # 管理员或用户有搜索内容
                results = department_query.filter(contact_phone__icontains=leads_search_content)
            else:
                # 管理员或用户无搜索内容
                results = department_query
        elif privileges == 'user':
            # 筛选员工名下的线索
            department_query = base_query.filter(cow_name=username)
            if leads_search_content is not None:
                # 管理员或用户有搜索内容
                results = department_query.filter(contact_phone__icontains=leads_search_content)
            else:
                # 管理员或用户无搜索内容
                results = department_query
        else:
            # 权限类型不合法
            return JsonResponse({'error': 'Invalid privilege type'}, status=400)
    else:
        # 未获取到权限信息
        return JsonResponse({'error': 'Privilege information not found'}, status=400)

    # 分页逻辑
    page_number = request.GET.get('page', 1)
    paginator = Paginator(results, 3)  # 每页显示 10 条记录
    page_obj = paginator.get_page(page_number)

    data = []
    for result in page_obj:
        # 获取部门名称和权限名称
        product_name = result.product_name.product_name if result.product_name else None
        business_name = result.business_name.business_name if result.business_name else None
        department_name = result.department_name.department_name if result.department_name else None
        channel_name = result.channel_name.channel_name if result.channel_name else None
        component_name = result.component_name.component_name if result.component_name else None
        cow_name = result.cow_name.cow_employee_name if result.cow_name else None
        proceeding_name = result.proceeding_name.proceeding_name if result.proceeding_name else None
        consultation_content = f"{result.consultation_content[:10]}..." if result.consultation_content else '-'
        follow_new_record = f"{result.follow_new_record[:10]}..." if result.follow_new_record else '-'
        follow_new_time = result.follow_new_time.strftime('%Y-%m-%d %H:%M') if result.follow_new_time else '-'

        data.append({
            'lead_id': result.id,
            'contact_person': result.contact_person,
            'contact_phone': result.contact_phone,
            'product_name': product_name,
            'business_name': business_name,
            'lead_creation_time': result.lead_creation_time.strftime('%Y-%m-%d %H:%M'),
            'lead_allocation_time': result.lead_allocation_time.strftime('%Y-%m-%d %H:%M'),
            'department_name': department_name,
            'channel_name': channel_name,
            'component_name': component_name,
            'consultation_content': consultation_content,
            'cow_name': cow_name,
            'proceeding_name': proceeding_name,
            'follow_new_record': follow_new_record,
            'follow_new_time': follow_new_time,
        })

    return JsonResponse({
        'results': data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'total_records': paginator.count
    })


# 线索认领按钮点击，ajax传来的checkbox数据处理
@required_privilege('super_admin', 'admin', 'user')
def claim_leads(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lead_ids = data.get('lead_ids', [])
            username = request.session.get('username')

            if not username:
                return JsonResponse({'success': False, 'message': '用户未登录。'})

            for lead_id in lead_ids:
                try:
                    lead = Leads.objects.get(id=lead_id)
                    lead.cow_name = Cow.objects.get(username=username)
                    # 插入领取线索的时间
                    lead.lead_allocation_time = datetime.datetime.now()
                    # 线索状态标记为2，表示已经被领取
                    lead.lead_status = 2
                    lead.save()
                except Leads.DoesNotExist:
                    continue

            return JsonResponse({'success': True, 'message': '线索认领成功。'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': '无效的请求方法。'})


# 退回线索到线索池逻辑，只能7天内退回
@required_privilege('super_admin', 'admin')
def send_back_leads(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lead_ids = data.get('lead_ids', [])
            username = request.session.get('username')

            if not username:
                return JsonResponse({'success': False, 'message': '用户未登录。'})

            for lead_id in lead_ids:
                try:
                    lead = Leads.objects.get(id=lead_id)
                    lead.cow_name = None
                    # 插入领取线索的时间
                    lead.lead_allocation_time = datetime.datetime.now()
                    # 线索状态标记为1，转换成新线索
                    lead.lead_status = 1
                    lead.save()
                except Leads.DoesNotExist:
                    continue

            return JsonResponse({'success': True, 'message': '退回线索池成功。'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': '无效的请求方法。'})


# 展示侧面板的线索信息
@required_privilege('super_admin', 'admin', 'user')
def canvas_leads_data(request, lead_id):
    try:
        # 使用 get 方法获取单个模型实例
        result = Leads.objects.get(id=lead_id)

        # 获取外键关联字段的值
        business_name = result.business_name.business_name if result.business_name else None
        cow_name = result.cow_name.cow_employee_name if result.cow_name else None
        username = result.cow_name.username if result.cow_name else '-'
        proceeding_name = result.proceeding_name.proceeding_name if result.proceeding_name else '-'
        consultation_content = result.consultation_content if result.consultation_content else '-'

        # 处理日期字段，确保不为空再进行格式转换
        lead_creation_time = result.lead_creation_time.strftime('%Y-%m-%d %H:%M') if result.lead_creation_time else None
        lead_allocation_time = result.lead_allocation_time.strftime(
            '%Y-%m-%d %H:%M') if result.lead_allocation_time else None

        data = {
            "results": [
                {
                    'contact_person': result.contact_person,
                    'contact_phone': result.contact_phone,
                    'business_name': business_name,
                    'lead_creation_time': lead_creation_time,
                    'lead_allocation_time': lead_allocation_time,
                    'consultation_content': consultation_content,
                    'cow_name': cow_name,
                    'username': username,
                    'proceeding_name': proceeding_name,
                }
            ]
        }
        return JsonResponse(data)
    except Leads.DoesNotExist:
        # 处理记录不存在的情况
        return JsonResponse({'results': []}, status=404)
    except Exception as e:
        # 处理其他异常
        return JsonResponse({'error': str(e)}, status=500)


# 插入canvas面板提交过来的跟进信息
@required_privilege('super_admin', 'admin', 'user')
def canvas_proceeding_add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        follow_up_person = data.get('follow_up_person')
        follow_up_content = data.get('follow_up_content')

        # 这个获取的是跟进状态，不是跟进人名字，别搞错。
        proceeding_name = data.get('proceeding_name')

        # 这里判断一下，防止proceeding_name 和 follow_up_content 填写错误或者为空
        if proceeding_name == 'proceeding-error' or proceeding_name == '' or follow_up_content == '':
            return JsonResponse({'status': 'error', 'message': '跟进状态未填写或者跟进内容为空！'})

        try:
            # 根据代码获取实例
            lead = Leads.objects.get(id=lead_id)
            follow_up_person = Cow.objects.get(username=follow_up_person)
            follow_up_content = follow_up_content

            # 这个跟进状态编码是插入到leads模型中的，上面的是插入到LeadFollowUpRecord 这个跟进纪录模型中的
            proceeding_name = Proceeding.objects.get(proceeding_code=proceeding_name)

            # 创建实例并保存跟进内容到跟进内容表模型LeadFollowUpRecord
            LeadFollowUpRecord.objects.create(
                lead=lead,
                follow_up_person=follow_up_person,
                follow_up_content=follow_up_content,
            )

            # 更新线索所表中的线索跟进状态字段
            results = Leads.objects.get(id=lead_id)
            results.proceeding_name = proceeding_name
            results.follow_new_time = datetime.datetime.now()
            results.follow_new_record = follow_up_content
            results.save()

            return JsonResponse({'status': 'success', 'message': '跟进信息添加成功！'})
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


# 展示侧面板的跟进信息
@required_privilege('super_admin', 'admin', 'user')
def canvas_proceeding_data(request, lead_id):
    lead_id = lead_id
    results = LeadFollowUpRecord.objects.filter(lead=lead_id)
    data = []

    for result in results:
        # 获取部门名称和权限名称
        follow_up_person = result.follow_up_person.cow_employee_name if result.follow_up_person else None
        follow_up_time = result.follow_up_time if result.follow_up_time else None
        follow_up_content = result.follow_up_content if result.follow_up_content else None

        data.append({
            'follow_up_person': follow_up_person,
            'follow_up_time': follow_up_time.strftime('%Y-%m-%d %H:%M'),
            'follow_up_content': follow_up_content,
        })
    return JsonResponse({'results': data})


# 线索详情页首页
@required_privilege('super_admin', 'admin', 'user')
def detail(request):
    username = request.session.get('username')
    privileges = request.session.get('privileges')

    if not username:
        return redirect('login:index')

    # 先获取查询参数code，然后获得当天lead_code所在的结果集
    lead_code = request.GET.get('code')
    leads_result = Leads.objects.get(lead_code=lead_code)

    if leads_result.lead_status == 1 and (privileges == 'admin' or privileges == 'user'):
        # 情况1，如果线索还未被领取过，状态1，且只有管理员和员工可以通过打开这个页面领取。
        # 存入线索领取人名字，这里是外键Cow模型的username
        leads_result.cow_name = Cow.objects.get(username=username)
        # 插入领取线索的时间
        leads_result.lead_allocation_time = datetime.datetime.now()
        # 线索状态标记为2，表示已经被领取
        leads_result.lead_status = 2
        leads_result.save()
    if leads_result.lead_status == 2 and privileges == 'user':
        # 情况2，状态2说明已经领取过了，要么是user，要么是admin，这里只让user可以覆盖领取，admin则没有权限。
        # 先获取一下表中的cow_name=>username
        cow_name = leads_result.cow_name.username
        if cow_name != username:
            # 意思就是user可以覆盖admin，admin不能覆盖user
            # 存入线索领取人名字，这里是外键Cow模型的username
            leads_result.cow_name = Cow.objects.get(username=username)
            # 插入领取线索的时间
            leads_result.lead_allocation_time = datetime.datetime.now()
            leads_result.save()

    # 页面标题
    title = {
        "page_title": "线索详情",
        "page_heading": "线索详情",
        "modal_app_name": "leads",
        "leads_result": leads_result,
    }
    return render(request, "detail_index.html", title)
