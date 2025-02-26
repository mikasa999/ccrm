from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from cow.models import Cow
import datetime


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            cow = Cow.objects.get(username=username)
            # 使用 check_password 方法验证密码
            if check_password(password, cow.password):
                messages.success(request, '登录成功！')

                # 设置会话
                request.session['user_id'] = cow.id
                request.session['username'] = cow.username
                request.session['privileges'] = cow.cow_privileges.privileges_code
                request.session['department'] = cow.cow_department.department_name
                request.session['department_code'] = cow.cow_department.department_code
                request.session['employee_name'] = cow.cow_employee_name

                # 这块目前好像没啥用，后面改进一下，设置会话过期时间为 1 个月（按秒计算）,
                one_month = 30 * 24 * 60 * 60
                request.session.set_expiry(one_month)

                response = redirect('leads:index')

                # 设置 Cookie, 这块目前来看没啥用
                # expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
                # response.set_cookie('user_id', cow.id, expires=expires)
                # response.set_cookie('username', cow.username, expires=expires)

                return response
            else:
                messages.error(request, '密码错误，请重试。')
        except Cow.DoesNotExist:
            messages.error(request, '用户名不存在，请重试。')

    return render(request, 'login_index.html')


# 退出登录的视图函数
def logout_view(request):
    # 清空会话
    request.session.flush()
    # 清空相关的 Cookie
    response = redirect('login:index')  # 重定向到登录页面，这里的 'login:index' 要根据实际情况修改
    response.delete_cookie('user_id')
    response.delete_cookie('username')
    return response


# 创建权限验证装饰器
def required_privilege(*privileges):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user_privilege = request.session.get('privileges')
            if user_privilege and user_privilege in privileges:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, '你没有权限访问该页面')
                # 获取上一页的 URL
                referer = request.META.get('HTTP_REFERER')
                if referer:
                    return redirect(referer)
                else:
                    # 如果没有上一页信息，重定向到默认页面（这里以登录页面为例）
                    return redirect('login:index')
        return wrapper
    return decorator
